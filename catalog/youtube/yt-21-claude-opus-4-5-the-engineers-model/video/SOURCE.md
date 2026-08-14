# Video source

- URL: https://www.youtube.com/watch?v=3kgx0YxCriM
- ID: 3kgx0YxCriM
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-21-claude-opus-4-5-the-engineers-model.mp4" "https://www.youtube.com/watch?v=3kgx0YxCriM"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
