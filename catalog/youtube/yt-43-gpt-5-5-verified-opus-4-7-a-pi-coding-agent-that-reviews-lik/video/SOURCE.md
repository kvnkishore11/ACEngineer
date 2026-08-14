# Video source

- URL: https://www.youtube.com/watch?v=EnXKysJNz_8
- ID: EnXKysJNz_8
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-43-gpt-5-5-verified-opus-4-7-a-pi-coding-agent-that-reviews-lik.mp4" "https://www.youtube.com/watch?v=EnXKysJNz_8"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
