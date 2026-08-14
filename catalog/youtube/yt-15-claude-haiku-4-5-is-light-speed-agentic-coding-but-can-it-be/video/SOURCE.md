# Video source

- URL: https://www.youtube.com/watch?v=aA9KP7QIQvM
- ID: aA9KP7QIQvM
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-15-claude-haiku-4-5-is-light-speed-agentic-coding-but-can-it-be.mp4" "https://www.youtube.com/watch?v=aA9KP7QIQvM"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
