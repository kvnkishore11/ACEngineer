# Video source

- URL: https://www.youtube.com/watch?v=00Y-p62sk0s
- ID: 00Y-p62sk0s
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-41-my-m5-max-gemma-4-mlx-local-stack-this-kills-model-providers.mp4" "https://www.youtube.com/watch?v=00Y-p62sk0s"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
