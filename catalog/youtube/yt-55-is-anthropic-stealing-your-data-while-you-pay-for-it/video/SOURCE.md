# Video source

- URL: https://www.youtube.com/watch?v=qh4vLlit97I
- ID: qh4vLlit97I
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-55-is-anthropic-stealing-your-data-while-you-pay-for-it.mp4" "https://www.youtube.com/watch?v=qh4vLlit97I"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
