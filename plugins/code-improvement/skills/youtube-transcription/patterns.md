# YouTube Transcription Patterns

## Caption Extraction (Primary)

**When to use:**
- Video has available captions
- Need fastest processing
- Original language transcript is acceptable

**Process:**
1. Check for caption availability
2. Filter by language preference
3. Select human-generated over ASR when available
4. Extract and format transcript

**Quality indicators:**
- Human-generated: `kind='captions'`
- Auto-generated: `kind='asr'`

---

## Audio Processing (Fallback)

**When to use:**
- No captions available
- Need different language than source
- Require audio quality improvements

**Process:**
1. Extract video metadata
2. Download audio stream
3. Convert to optimal format (16kHz, mono)
4. Apply speech-to-text processing
5. Generate structured transcript

---

## Configuration

```yaml
# Audio processing defaults
sample_rate: 16000
channels: 1
format: "wav"

# Transcription defaults
language: "en"
output_format: "segments"
include_timestamps: true
```

---

## Programmatic Usage

```python
from tools.youtube_transcriber import transcribe_youtube_video

# Simple transcription
result = transcribe_youtube_video("VIDEO_ID")

# With options
result = transcribe_youtube_video(
    video_id="VIDEO_ID",
    method="captions",  # or "audio"
    language="en",
    output_format="text"
)
```

---

## Output Formats

### Segmented Text
```
[0:00:00] Speaker 1: Welcome to our tutorial.
[0:00:05] Speaker 1: Today we'll explore...
```

### JSON Structure
```json
{
  "video_id": "VIDEO_ID",
  "method": "captions",
  "segments": [
    {"start": "00:00:00", "text": "Welcome..."}
  ]
}
```

---

## Performance Optimization

### Caching
- Caption cache: 24 hours
- Metadata cache: 1 hour
- Audio cache: Temporary with auto-cleanup

### Batch Processing
```python
for video_id in video_ids:
    result = transcribe_youtube_video(video_id, use_cache=True)
```
