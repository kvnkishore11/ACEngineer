# Video source

- URL: https://www.youtube.com/watch?v=LOazLNQnB80
- ID: LOazLNQnB80
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-35-mac-mini-agents-openclaw-is-a-nightmare-use-these-skills-ins.mp4" "https://www.youtube.com/watch?v=LOazLNQnB80"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
