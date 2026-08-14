# Video source

- URL: https://www.youtube.com/watch?v=haUfb1ievTE
- ID: haUfb1ievTE
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-56-my-super-simple-software-factory-for-agentic-engineers.mp4" "https://www.youtube.com/watch?v=haUfb1ievTE"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
