# Video source

- URL: https://www.youtube.com/watch?v=-WBHNFAB0OE
- ID: -WBHNFAB0OE
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-27-agent-threads-how-to-ship-like-boris-cherny-ralph-wiggum-in.mp4" "https://www.youtube.com/watch?v=-WBHNFAB0OE"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
