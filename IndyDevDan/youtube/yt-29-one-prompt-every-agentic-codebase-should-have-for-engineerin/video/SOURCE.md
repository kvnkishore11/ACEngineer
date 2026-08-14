# Video source

- URL: https://www.youtube.com/watch?v=3_mwKbYvbUg
- ID: 3_mwKbYvbUg
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-29-one-prompt-every-agentic-codebase-should-have-for-engineerin.mp4" "https://www.youtube.com/watch?v=3_mwKbYvbUg"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
