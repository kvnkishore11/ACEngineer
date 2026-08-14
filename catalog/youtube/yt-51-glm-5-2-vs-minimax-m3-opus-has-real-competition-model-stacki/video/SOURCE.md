# Video source

- URL: https://www.youtube.com/watch?v=cFYdiynrxpQ
- ID: cFYdiynrxpQ
- Local mp4: download with:

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 \
  -o "yt-51-glm-5-2-vs-minimax-m3-opus-has-real-competition-model-stacki.mp4" "https://www.youtube.com/watch?v=cFYdiynrxpQ"
```

Or re-run: `python3 build_video_folder.py --batch … --download-video`
