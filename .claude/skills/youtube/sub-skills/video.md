# Video Sub-Skill

This sub-skill analyses one public YouTube video from a pasted URL or ID: what it is about, how it performed against its own channel, and what the creator can borrow as inspiration. It works from public metadata only, so it describes patterns and signals, never proven causes.

## Inputs Required

- **Video URL or ID** (required)
- **Creator's niche, channel size and goal** (optional): if known, tailor the inspiration section to them. If not, analyse the video anyway and ask for them at the end. Don't block on them.

## Reference Files to Load

- `references/algorithm-guide.md`
- `references/seo-playbook.md`

## Parallel Agents

Not required. Execute sequentially.

## Step-by-Step Execution

1. Run `python execution/fetch_video.py "<URL or ID>"` (about 4 quota units). Never ask for or print an API key; in a cloud session the agent proxy attaches it.
2. If it errors, report the error plainly (not public, deleted, bad URL, quota) and stop. Don't invent data.
3. **Topic**: from the title, description, tags and chapters (timestamps in the description), state the topic, angle, format (tutorial, review, list, story, comparison…) and target viewer.
4. **Packaging**: title structure and length, description (hook line, links, chapters, hashtags), tag usage. Compare against `references/seo-playbook.md`. Describe the thumbnail only from its URL if you can view it; otherwise skip.
5. **Performance**: report views, likes, comments, like and comment rate, views per day, views per subscriber and `views_vs_channel_median`. Interpret with care:
   - Above 3× the channel median = clear outlier for that channel; 1–3× = above usual; below 1× = under usual.
   - A video only days old hasn't settled; a years-old video has had time to accumulate.
   - The median comes from recent uploads, which may differ in format (e.g. Shorts vs long-form) from this video. Say so if `possibly_short` differs from the norm.
   - Missing likes or comments mean the creator hid them.
6. **Inspiration**: give 3–5 transferable patterns (angle, format, title structure, length, topic gap) and 3 original video ideas for the creator's niche that use those patterns without copying the video. Label each pattern as an observation from metadata, not a proven reason for success.
7. Offer a next step: `/youtube competitor` to see whether the pattern repeats across the niche, or `/youtube ideate` to build on it.

## Output Template

```markdown
## Video Analysis: [Title]

**Channel**: [Name] · [Subscribers] subscribers
**Published**: [Date] ([N] days ago) · **Duration**: [H:MM:SS] [· likely a Short]
**URL**: [URL]

### 1. Topic and Angle
[Topic, angle, format, target viewer]

### 2. Performance (public data)

| Metric | Value | Context |
|--------|-------|---------|
| Views | [N] | [N]× channel median of [M] (last [K] uploads) |
| Views per day | [N] | |
| Likes | [N] ([X]% of views) | |
| Comments | [N] ([X]% of views) | |
| Views per subscriber | [N] | |

[2–3 sentences on what this suggests, with the caveats that apply]

### 3. Packaging
- **Title**: [observations]
- **Description**: [observations]
- **Tags**: [list or "none set"]

### 4. Patterns Worth Borrowing
1. [Pattern] — [why it may have helped; observation, not proof]

### 5. Original Ideas for Your Channel
1. **[Working title]** — [one-line angle]

### Limits of This Analysis
Public data only: no CTR, impressions, retention, traffic sources or revenue, and no transcript. These numbers show how the video performed, not why.

### Next Steps
[Suggested follow-up sub-skill]
```
