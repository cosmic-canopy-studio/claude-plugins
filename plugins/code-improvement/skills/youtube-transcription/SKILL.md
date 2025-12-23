---
name: youtube-transcription
description: Transcribe YouTube videos using captions or audio processing (project) - transcribing video, extracting transcript, YouTube transcription, audio processing, speech to text
when_to_use: transcribing video, extracting transcript, YouTube transcription, audio processing, speech to text
---

# YouTube Transcription

Extract transcripts from YouTube videos using a hierarchical approach:
1. **Primary**: Caption extraction (fast, accurate when available)
2. **Fallback**: Audio processing with Whisper

## Quick Start

```bash
# Transcribe a YouTube video
/yt-transcribe https://www.youtube.com/watch?v=VIDEO_ID
```

## Method Selection

| Method | When to Use | Advantages |
|--------|-------------|------------|
| Captions | Video has captions | Instant, accurate, low cost |
| Audio | No captions available | Works with any video |

## Core Components

- `youtube-transcriber` agent: Orchestrates workflow
- `audio-processor` agent: Handles audio extraction
- `/yt-transcribe` command: Direct transcription

## Output Formats

- **Text**: Plain transcript
- **Segments**: Timestamped segments with speakers
- **JSON**: Structured data with metadata

## Error Handling

System automatically falls back:
1. Captions → Audio processing
2. Preferred language → English → Any available

See [patterns.md](patterns.md) for detailed configuration.
See [reference.md](reference.md) for troubleshooting.
