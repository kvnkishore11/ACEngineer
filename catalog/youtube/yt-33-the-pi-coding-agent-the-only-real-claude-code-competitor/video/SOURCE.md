# Video source

- URL: https://www.youtube.com/watch?v=f8cfH5XX-XU
- ID: f8cfH5XX-XU
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-33-the-pi-coding-agent-the-only-real-claude-code-competitor.mp4" "https://www.youtube.com/watch?v=f8cfH5XX-XU"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
