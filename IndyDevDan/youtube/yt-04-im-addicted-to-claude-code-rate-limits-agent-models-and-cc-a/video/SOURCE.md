# Video source

- URL: https://www.youtube.com/watch?v=SSbqXzRsC6s
- ID: SSbqXzRsC6s
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-04-im-addicted-to-claude-code-rate-limits-agent-models-and-cc-a.mp4" "https://www.youtube.com/watch?v=SSbqXzRsC6s"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
