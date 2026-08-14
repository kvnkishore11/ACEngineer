# Video source

- URL: https://www.youtube.com/watch?v=M30gp1315Y4
- ID: M30gp1315Y4
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-38-one-agent-is-not-enough-agentic-coding-beyond-claude-code.mp4" "https://www.youtube.com/watch?v=M30gp1315Y4"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
