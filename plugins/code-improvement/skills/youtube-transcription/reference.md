# YouTube Transcription Reference

## Troubleshooting

### Common Issues

| Error | Solution |
|-------|----------|
| 404: Video not found | Verify video ID, check if public |
| No captions available | System auto-switches to audio |
| Audio download timeout | Increase timeout, check network |
| Language not supported | Use fallback language |

### Fallback Strategies

1. **Method**: Captions → Audio processing
2. **Language**: Preferred → English → Any available
3. **Quality**: ASR captions → Audio processing
4. **Service**: Primary STT → Backup service

---

## Debug Mode

```python
transcribe_youtube_video(
    video_id="VIDEO_ID",
    debug=True,
    save_intermediate=True
)
```

### Debug Information
- Video metadata retrieval status
- Caption availability and quality
- Audio download progress
- Cache hit/miss rates

---

## Validation Checklist

- [ ] Video ID parsing works correctly
- [ ] Caption extraction handles multiple languages
- [ ] Audio fallback activates when needed
- [ ] Timestamps are accurate
- [ ] Output formats are consistent
- [ ] Error messages are helpful

---

## Dependencies

- `google-api-python-client`: YouTube API access
- `whisper`: Speech-to-text processing
- `yt-dlp`: Audio extraction
- `pydub`: Audio format conversion

---

## Security

- No API keys required for basic caption extraction
- Temporary files are securely cleaned up
- No long-term storage without explicit consent

---

## Best Practices

### Method Selection
- Always try captions first for speed/accuracy
- Use audio processing for translation
- Consider source language and desired output

### Quality Assurance
- Review transcript quality indicators
- Verify speaker identification for multi-speaker content
- Check timestamp accuracy

### Performance
- Use caching for repeated requests
- Process videos in batches
- Monitor API rate limits
