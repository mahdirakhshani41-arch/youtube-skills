# Using the YouTube skill in this repository

`.claude/skills/youtube/` is the working copy Claude Code loads as the `youtube` skill.
`skills/claude-youtube/` is the upstream original; leave it unchanged so the tests and
upstream merges keep working.

## Scope

Public YouTube research only. No OAuth, YouTube Studio analytics (CTR, impressions,
retention, traffic sources, revenue), transcript downloads, or DataForSEO.

## API key

In cloud sessions the YouTube Data API key is a Network secret: the agent proxy attaches
it as `X-Goog-Api-Key` to `www.googleapis.com` and `youtube.googleapis.com`. Never ask for,
print, or save the key, and never set `YOUTUBE_API_KEY` in cloud sessions. Check status
with `python3 .claude/skills/youtube/execution/utils/youtube_auth.py --check api_key`.

## Setup

The SessionStart hook (`.claude/hooks/session-start.sh`) installs
`.claude/skills/youtube/requirements.txt` in cloud sessions. To install by hand:
`python3 -m pip install -r .claude/skills/youtube/requirements.txt`.

## Usage

- **Analyze a video**: paste a video URL ("analyze this as inspiration for my channel"),
  or `/youtube video <url>`. Runs `execution/fetch_video.py` (~4 quota units).
- **Competitor research**: `/youtube competitor` with your niche and competitor handles.
  Each search costs 100 units of the 10,000 daily quota; channel lookups ~5–16.
- **Channel data**: `/youtube analyze @handle` for public channel and upload stats.
- **Original ideas**: `/youtube ideate`, ideally after a competitor run or video analysis.

Metadata shows how a video performed, not why. Present patterns as observations.
