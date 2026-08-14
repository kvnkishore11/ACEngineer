# Video source

- URL: https://www.youtube.com/watch?v=u5GkG71PkR0
- ID: u5GkG71PkR0
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-28-the-claude-code-feature-senior-engineers-keep-missing.mp4" "https://www.youtube.com/watch?v=u5GkG71PkR0"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
