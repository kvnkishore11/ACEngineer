# Video source

- URL: https://www.youtube.com/watch?v=V5IhsHEHXOg
- ID: V5IhsHEHXOg
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-20-i-gave-gemini-3-pro-its-own-computer-its-official-claude-cod.mp4" "https://www.youtube.com/watch?v=V5IhsHEHXOg"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
