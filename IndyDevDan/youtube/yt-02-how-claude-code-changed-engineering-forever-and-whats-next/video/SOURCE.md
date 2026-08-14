# Video source

- URL: https://www.youtube.com/watch?v=6fCqj4xFCZI
- ID: 6fCqj4xFCZI
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-02-how-claude-code-changed-engineering-forever-and-whats-next.mp4" "https://www.youtube.com/watch?v=6fCqj4xFCZI"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
