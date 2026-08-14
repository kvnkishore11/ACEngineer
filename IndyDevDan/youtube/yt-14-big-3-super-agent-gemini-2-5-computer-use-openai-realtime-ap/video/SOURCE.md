# Video source

- URL: https://www.youtube.com/watch?v=Ur3TJm0BckQ
- ID: Ur3TJm0BckQ
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-14-big-3-super-agent-gemini-2-5-computer-use-openai-realtime-ap.mp4" "https://www.youtube.com/watch?v=Ur3TJm0BckQ"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
