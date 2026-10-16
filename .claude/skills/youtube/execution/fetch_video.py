"""
Fetch public metadata and statistics for a single video via YouTube Data API v3.

Also fetches the channel's subscriber count and its recent uploads as a
baseline, so the video's views can be compared to what the channel usually gets.
Public data only: no CTR, impressions, retention, traffic sources, or revenue.

Input: video ID or URL (watch, youtu.be, shorts, live, embed)
Output: JSON with video metadata, statistics, derived ratios, and channel baseline

Usage:
    python execution/fetch_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    python execution/fetch_video.py dQw4w9WgXcQ --baseline 20
    python execution/fetch_video.py dQw4w9WgXcQ --no-baseline
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_channel_data import fetch_recent_videos
from utils.quota_tracker import check_quota, consume_quota
from utils.youtube_auth import get_data_api_service


def parse_video_id(raw: str) -> str | None:
    """Extract an 11-character video ID from a URL or bare ID."""
    raw = raw.strip()
    if re.fullmatch(r"[\w-]{11}", raw):
        return raw
    match = re.search(
        r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|live/|embed/)|youtu\.be/)([\w-]{11})",
        raw,
    )
    return match.group(1) if match else None


def iso_duration_seconds(duration: str | None) -> int | None:
    """Convert an ISO 8601 duration (PT1H2M3S) to seconds."""
    if not duration:
        return None
    match = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not match:
        return None
    d, h, m, s = (int(x) if x else 0 for x in match.groups())
    return d * 86400 + h * 3600 + m * 60 + s


def format_seconds(total: int) -> str:
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch public data for one YouTube video")
    parser.add_argument("video", help="Video URL or ID")
    parser.add_argument(
        "--baseline",
        type=int,
        default=10,
        help="Recent channel uploads to use as a baseline (default: 10)",
    )
    parser.add_argument("--no-baseline", action="store_true", help="Skip the channel baseline")
    args = parser.parse_args()

    video_id = parse_video_id(args.video)
    if not video_id:
        print(json.dumps({"error": f"Not a YouTube video URL or ID: {args.video}"}), file=sys.stderr)
        sys.exit(1)

    quota = check_quota("videos.list", 4)
    if not quota.get("can_execute", True):
        print(json.dumps({"error": quota["error"]}), file=sys.stderr)
        sys.exit(1)

    service, error = get_data_api_service()
    if error:
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

    response = (
        service.videos().list(part="snippet,statistics,contentDetails", id=video_id).execute()
    )
    consume_quota("videos.list")
    items = response.get("items", [])
    if not items:
        print(
            json.dumps({"error": f"Video not found or not public: {video_id}"}), file=sys.stderr
        )
        sys.exit(1)

    v = items[0]
    snippet = v.get("snippet", {})
    stats = v.get("statistics", {})
    content = v.get("contentDetails", {})

    # Hidden like/comment counts are absent from the response; keep them as null.
    views = int(stats["viewCount"]) if "viewCount" in stats else None
    likes = int(stats["likeCount"]) if "likeCount" in stats else None
    comments = int(stats["commentCount"]) if "commentCount" in stats else None
    seconds = iso_duration_seconds(content.get("duration"))

    published = snippet.get("publishedAt")
    days_live = None
    if published:
        published_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
        days_live = max((datetime.now(timezone.utc) - published_dt).total_seconds() / 86400, 1 / 24)

    video = {
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": snippet.get("title"),
        "description": snippet.get("description", ""),
        "channel_title": snippet.get("channelTitle"),
        "channel_id": snippet.get("channelId"),
        "published_at": published,
        "duration_seconds": seconds,
        "duration": format_seconds(seconds) if seconds is not None else None,
        "views": views,
        "likes": likes,
        "comments": comments,
        "tags": snippet.get("tags", []),
        "category_id": snippet.get("categoryId"),
        "default_language": snippet.get("defaultLanguage")
        or snippet.get("defaultAudioLanguage"),
        "live_broadcast_content": snippet.get("liveBroadcastContent"),
        "thumbnail": (
            snippet.get("thumbnails", {}).get("maxres")
            or snippet.get("thumbnails", {}).get("high", {})
        ).get("url"),
    }

    derived: dict[str, Any] = {
        "days_since_upload": round(days_live, 1) if days_live else None,
        "views_per_day": round(views / days_live) if views is not None and days_live else None,
        "like_rate_pct": round(likes / views * 100, 2) if likes is not None and views else None,
        "comment_rate_pct": (
            round(comments / views * 100, 3) if comments is not None and views else None
        ),
        # The API has no Shorts flag; 3 minutes is the current Shorts length limit.
        "possibly_short": seconds is not None and seconds <= 180,
    }

    channel: dict[str, Any] = {}
    if not args.no_baseline and video["channel_id"]:
        ch_resp = (
            service.channels()
            .list(part="statistics,contentDetails", id=video["channel_id"])
            .execute()
        )
        consume_quota("channels.list")
        ch_items = ch_resp.get("items", [])
        if ch_items:
            ch_stats = ch_items[0].get("statistics", {})
            hidden = ch_stats.get("hiddenSubscriberCount", False)
            subs = None if hidden else int(ch_stats.get("subscriberCount", 0))
            channel = {
                "subscriber_count": subs,
                "total_views": int(ch_stats.get("viewCount", 0)),
                "video_count": int(ch_stats.get("videoCount", 0)),
            }
            if subs and views is not None:
                derived["views_per_subscriber"] = round(views / subs, 2)

            uploads = ch_items[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
            if uploads and args.baseline > 0:
                recent = [r for r in fetch_recent_videos(service, uploads, args.baseline) if r["video_id"] != video_id]
                if recent:
                    median_views = statistics.median(r["views"] for r in recent)
                    channel["baseline"] = {
                        "recent_uploads_compared": len(recent),
                        "median_views": round(median_views),
                        "note": "Recent uploads of all ages and formats; newer videos have had less time to gather views.",
                    }
                    if median_views and views is not None:
                        derived["views_vs_channel_median"] = round(views / median_views, 2)

    result = {
        "video": video,
        "derived": derived,
        "channel": channel,
        "fetched_at": datetime.now().isoformat(),
        "note": "Public data only. CTR, impressions, retention, traffic sources and revenue "
        "are not available, so these numbers show what happened, not why.",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
