# Video source

- URL: https://www.youtube.com/watch?v=p0mrXfwAbCg
- ID: p0mrXfwAbCg
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-17-the-one-agent-to-rule-them-all-advanced-agentic-coding.mp4" "https://www.youtube.com/watch?v=p0mrXfwAbCg"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
