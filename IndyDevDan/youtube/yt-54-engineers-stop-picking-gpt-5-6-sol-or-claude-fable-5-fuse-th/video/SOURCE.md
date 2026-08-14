# Video source

- URL: https://www.youtube.com/watch?v=AQl5Q-0l7FQ
- ID: AQl5Q-0l7FQ
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-54-engineers-stop-picking-gpt-5-6-sol-or-claude-fable-5-fuse-th.mp4" "https://www.youtube.com/watch?v=AQl5Q-0l7FQ"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
