# Video source

- URL: https://www.youtube.com/watch?v=_vpNQ6IwP9w
- ID: _vpNQ6IwP9w
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-36-the-library-meta-skill-how-i-distribute-private-skills-agent.mp4" "https://www.youtube.com/watch?v=_vpNQ6IwP9w"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
