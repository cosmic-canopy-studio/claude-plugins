---
name: youtube-transcription
description: Comprehensive YouTube video transcription system with dual-method approach (captions and audio processing)
---

# YouTube Transcription System

## Overview

The YouTube transcription system provides a comprehensive solution for extracting high-quality transcripts from YouTube videos using a hierarchical approach:

1. **Primary Method**: Direct caption extraction (fastest and most accurate when available)
2. **Fallback Method**: Audio processing with speech-to-text conversion

## Core Components

### Tools

- `youtube_transcriber.py`: Main transcription tool with dual extraction methods
- `audio_processor.py`: Audio downloading and processing utilities
- `cleanup.py`: Maintenance and cache management

### Agents

- `youtube-transcriber`: Orchestrates the transcription workflow
- `audio-processor`: Handles audio-specific operations

### Commands

- `/yt-transcribe`: Direct transcription command with optional URL parameter

## Usage

### Basic Transcription

```bash
# Transcribe a YouTube video
/yt-transcribe https://www.youtube.com/watch?v=RivViRdBlII

# Transcribe the test video (default example)
/yt-transcribe
```

### Programmatic Usage

```python
from tools.youtube_transcriber import transcribe_youtube_video

# Simple transcription
result = transcribe_youtube_video("RivViRdBlII")

# Transcription with options
result = transcribe_youtube_video(
    video_id="RivViRdBlII",
    method="captions",  # or "audio"
    language="en",
    output_format="text"
)
```

## Method Selection Hierarchy

### 1. Caption Extraction (Preferred)

**When to use:**
- Video has available captions
- Need fastest processing
- Original language transcript is acceptable

**Advantages:**
- Near-instant processing
- 100% accurate to original captions
- Preserves speaker identification
- Includes timing information
- Lower computational cost

**Process:**
1. Check for caption availability
2. Filter by language preference
3. Select human-generated over ASR when available
4. Extract and format transcript

### 2. Audio Processing (Fallback)

**When to use:**
- No captions available
- Need different language than source
- Require audio quality improvements

**Advantages:**
- Works with any YouTube video
- Can translate to different languages
- Better handling of poor quality captions
- More control over output format

**Process:**
1. Extract video metadata
2. Download audio stream
3. Convert to optimal format (16kHz, mono)
4. Apply speech-to-text processing
5. Generate structured transcript

## Configuration

### Default Settings

```yaml
# Audio processing defaults
sample_rate: 16000
channels: 1
bitrate: "64k"
format: "wav"

# Transcription defaults
language: "en"
fallback_language: "en-US"
output_format: "segments"
include_timestamps: true
max_retries: 3
```

### Quality Considerations

#### Caption Quality Indicators
- **Human-generated**: `kind='captions'`
- **Auto-generated**: `kind='asr'`
- **Language codes**: `lang='en'` vs `lang='en-us'`

#### Audio Quality Factors
- Original audio bitrate
- Background noise levels
- Speaker clarity
- Multiple speakers

## Output Formats

### 1. Plain Text

```
This is a sample transcript of the YouTube video content.
The text flows continuously without timestamps.
```

### 2. Segmented Text

```
[0:00:00] Speaker 1: Welcome to our tutorial on YouTube transcription.
[0:00:05] Speaker 1: Today we'll explore different methods...
[0:00:12] Speaker 2: Let me start by explaining the benefits...
```

### 3. JSON Structure

```json
{
  "video_id": "RivViRdBlII",
  "title": "Video Title",
  "duration": "PT5M30S",
  "method": "captions",
  "language": "en",
  "segments": [
    {
      "start": "00:00:00.000",
      "duration": "5.234",
      "text": "Welcome to our tutorial...",
      "speaker": null
    }
  ]
}
```

## Error Handling

### Common Issues and Solutions

#### 1. Video Not Found
```
Error: 404: Video not found
Solution: Verify video ID is correct and video is public
```

#### 2. No Captions Available
```
Status: No captions available, falling back to audio processing
Solution: System automatically switches to audio extraction
```

#### 3. Audio Download Timeout
```
Error: Audio download timeout
Solution: Increase timeout in config or check network connection
```

#### 4. Transcription Service Error
```
Error: Speech-to-text service unavailable
Solution: Retry with exponential backoff or use captions only
```

#### 5. Language Not Supported
```
Error: Language code 'xx' not supported
Solution: Use fallback language or available caption languages
```

### Fallback Strategies

1. **Method Fallback**: Captions → Audio processing
2. **Language Fallback**: Preferred language → English → Any available
3. **Quality Fallback**: ASR captions → Audio processing
4. **Service Fallback**: Primary STT service → Backup service

## Performance Optimization

### Caching

- **Caption cache**: Stores extracted captions for 24 hours
- **Metadata cache**: Caches video information for 1 hour
- **Audio cache**: Temporary storage with automatic cleanup

### Batch Processing

```python
# Process multiple videos efficiently
video_ids = ["RivViRdBlII", "another_id", "third_id"]
for video_id in video_ids:
    result = transcribe_youtube_video(video_id, use_cache=True)
```

### Resource Management

- Automatic cleanup of temporary audio files
- Memory-efficient streaming for large videos
- Configurable concurrent processing limits

## Integration Examples

### With Claude Code Commands

```bash
# Quick transcription with default settings
/yt-transcribe

# Specific video with options
/yt-transcribe https://youtube.com/watch?v=RivViRdBlII --format json --language en

# Transcribe and analyze
/yt-transcribe | /analyze-content
```

### With Other Tools

```python
# Combine with content analysis
transcript = transcribe_youtube_video(video_id)
summary = summarize_text(transcript['segments'])
keywords = extract_keywords(transcript['full_text'])
```

## Best Practices

### 1. Method Selection
- Always try captions first for speed and accuracy
- Use audio processing for translation or quality improvements
- Consider the source language and desired output language

### 2. Error Prevention
- Validate video IDs before processing
- Check video duration for very long content
- Monitor available disk space for audio downloads

### 3. Quality Assurance
- Review transcript quality indicators
- Verify speaker identification for multi-speaker content
- Check timestamp accuracy for synchronized content

### 4. Performance Considerations
- Use caching for repeated requests
- Process videos in batches for efficiency
- Monitor API rate limits for transcription services

## Troubleshooting Guide

### Debug Mode

```python
# Enable debug logging
transcribe_youtube_video(
    video_id="RivViRdBlII",
    debug=True,
    save_intermediate=True
)
```

### Common Debug Information

- Video metadata retrieval status
- Caption availability and quality
- Audio download progress
- Transcription service response times
- Cache hit/miss rates

## Test Cases

### Test Video: `RivViRdBlII`

```bash
# Expected behavior for test video
/yt-transcribe RivViRdBlII
# Should return transcript with method='captions'
# Language should be 'en'
# Duration approximately 5 minutes
```

### Validation Checklist

- [ ] Video ID parsing works correctly
- [ ] Caption extraction handles multiple languages
- [ ] Audio fallback activates when needed
- [ ] Timestamps are accurate
- [ ] Output formats are consistent
- [ ] Error messages are helpful
- [ ] Cache improves performance
- [ ] Cleanup prevents disk space issues

## Future Enhancements

1. **Multi-language support**: Simultaneous transcription in multiple languages
2. **Speaker diarization**: Advanced speaker identification and labeling
3. **Real-time processing**: Live transcription during streaming
4. **Custom vocabularies**: Industry-specific terminology recognition
5. **Quality scoring**: Automated assessment of transcript accuracy
6. **Integration hooks**: Direct integration with content analysis tools

## Security and Privacy

- No API keys required for basic caption extraction
- Audio processing respects content privacy
- Temporary files are securely cleaned up
- No long-term storage of content without explicit consent

## Dependencies

- `python-dotenv`: Environment variable management
- `google-api-python-client`: YouTube API access
- `whisper`: Speech-to-text processing
- `yt-dlp`: Audio extraction
- `pydub`: Audio format conversion

## Version History

- v1.0: Initial implementation with caption and audio methods
- v1.1: Added caching and cleanup utilities
- v1.2: Enhanced error handling and fallback strategies
- v1.3: Performance optimizations and batch processing