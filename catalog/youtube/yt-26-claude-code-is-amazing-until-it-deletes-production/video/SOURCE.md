# Video source

- URL: https://www.youtube.com/watch?v=VqDs46A8pqE
- ID: VqDs46A8pqE
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-26-claude-code-is-amazing-until-it-deletes-production.mp4" "https://www.youtube.com/watch?v=VqDs46A8pqE"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
