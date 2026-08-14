# Video source

- URL: https://www.youtube.com/watch?v=Kf5-HWJPTIE
- ID: Kf5-HWJPTIE
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-09-elite-context-engineering-with-claude-code.mp4" "https://www.youtube.com/watch?v=Kf5-HWJPTIE"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
