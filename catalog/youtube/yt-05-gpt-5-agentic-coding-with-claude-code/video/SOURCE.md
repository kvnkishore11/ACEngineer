# Video source

- URL: https://www.youtube.com/watch?v=tcZ3W8QYirQ
- ID: tcZ3W8QYirQ
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-05-gpt-5-agentic-coding-with-claude-code.mp4" "https://www.youtube.com/watch?v=tcZ3W8QYirQ"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
