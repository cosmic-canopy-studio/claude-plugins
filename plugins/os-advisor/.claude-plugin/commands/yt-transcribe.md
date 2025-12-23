---
description: Transcribe YouTube videos using captions API or Whisper audio transcription
model: sonnet
---

# YouTube Transcription

Extract transcripts from YouTube videos with automatic language detection and intelligent fallback between captions and audio transcription.

## Quick Start

```bash
# Basic usage with video URL
/yt-transcribe "https://www.youtube.com/watch?v=VIDEO_ID"

# With YouTube video ID only
/yt-transcribe "VIDEO_ID"

# Save to specific file
/yt-transcribe "VIDEO_ID" --output "transcript.md"

# Force audio transcription (skip captions)
/yt-transcribe "VIDEO_ID" --audio

# Specify language for better accuracy
/yt-transcribe "VIDEO_ID" --languages en
```

## Usage

```bash
/yt-transcribe <VIDEO_ID_OR_URL> [OPTIONS]
```

### Required Arguments

- `VIDEO_ID_OR_URL`: YouTube video ID or full URL

### Options

- `--output, -o FILE`: Save transcript to file (default: print to console)
- `--format, -f FORMAT`: Output format (markdown, json, text) - default: markdown
- `--audio`: Force audio transcription even if captions available
- `--whisper-model MODEL`: Whisper model size (tiny, base, small, medium, large) - default: small
- `--languages LANG [LANG ...]`: Preferred language codes (default: en)
- `--auto-captions`: Prefer auto-generated captions over manual ones
- `--openai-api-key KEY`: OpenAI API key (or set OPENAI_API_KEY env var)
- `--verbose, -v`: Show detailed processing information
- `--help, -h`: Show this help message

## Examples

### Basic Transcription

```bash
/yt-transcribe "https://www.youtube.com/watch?v=VIDEO_ID"
```

Outputs transcript to console with automatic language detection.

### Save to File with Formatting

```bash
/yt-transcribe "VIDEO_ID" --output "lecture_notes.md" --format markdown
```

Creates a nicely formatted markdown file with the transcript.

### Force Audio Transcription

```bash
/yt-transcribe "VIDEO_ID" --audio --whisper-model medium --languages en
```

Uses Whisper medium model for English audio transcription, bypassing captions.

### Multiple Language Preferences

```bash
/yt-transcribe "VIDEO_ID" --languages en es fr
```

Tries English first, then Spanish, then French captions.

## Output Formats

### Markdown (default)
Formatted with headers, paragraphs, and proper spacing for readability.

### JSON
Structured data with metadata, timestamps, and confidence scores.

### Text
Plain text transcript with speaker labels and paragraphs.

## Processing Pipeline

1. **Video Validation**: Check video availability and permissions
2. **Captions Attempt**: Try YouTube captions API first (fastest method)
3. **Audio Fallback**: Download and transcribe audio if captions unavailable
4. **Language Detection**: Auto-detect or use specified language
5. **Quality Processing**: Clean and format the transcript
6. **Output Generation**: Format according to requested output type

## Model Selection Guide

**Whisper Models:**
- `tiny`: Fastest, basic accuracy (~32MB)
- `base`: Good balance of speed and accuracy (~142MB)
- `small`: Better accuracy for clear audio (~466MB) - **Default**
- `medium`: High accuracy for most content (~1.5GB)
- `large`: Best accuracy, slowest (~3GB)

## Troubleshooting

### Common Issues

**Video not accessible:**
- Check if video is public or unlisted
- Verify video ID is correct
- Try with full URL instead of just ID

**Poor transcription quality:**
- Specify the correct language with `--languages`
- Try a larger Whisper model with `--whisper-model`
- Use `--audio` if captions seem incorrect

**Slow processing:**
- Use smaller Whisper model (`base` or `tiny`)
- Use `--verbose` to see processing steps

### Error Messages

- `Video unavailable`: Video is private, deleted, or region-restricted
- `No captions available`: Video has no captions, use `--audio`
- `Transcription failed`: Audio processing error, try different model
- `Model download failed`: Network or disk space issue

## Integration

Uses the shared YouTube transcription toolkit at `~/tools/youtube-transcriber/`.

---

cd ~/tools/youtube-transcriber && uv run python youtube_transcriber.py $*
