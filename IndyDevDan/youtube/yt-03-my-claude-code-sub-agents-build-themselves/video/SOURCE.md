# Video source

- URL: https://www.youtube.com/watch?v=7B2HJr0Y68g
- ID: 7B2HJr0Y68g
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-03-my-claude-code-sub-agents-build-themselves.mp4" "https://www.youtube.com/watch?v=7B2HJr0Y68g"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
