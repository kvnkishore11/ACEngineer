"""Long-lived mlx-vlm runner subprocess.

Started by `MLXRunner` in `_harness.py`. Loads a model exactly once, then
serves an unbounded sequence of generate() requests over JSON-lines stdio.

Protocol:
    - On startup, prints {"event": "ready"} on stdout once `load()` returns.
    - Reads JSON requests one per line on stdin:
        {"prompt": "...", "max_tokens": 4096, "audio": "/path.wav"?, "image": "/path.png"?}
        {"cmd": "exit"}
    - Writes one JSON response per request on stdout:
        {"event": "result", "prefill_tok_s": ..., "decode_tok_s": ...,
         "prompt_tokens": ..., "gen_tokens": ..., "wall_time_s": ..., "text": "..."}
    - On any exception, prints {"event": "error", "detail": "..."} and exits.

This must be invoked with `.mlx-venv/bin/python` so mlx-vlm is importable.
"""

from __future__ import annotations

import json
import sys
import time
import traceback


def emit(obj: dict) -> None:
    print(json.dumps(obj), flush=True)


def main() -> int:
    if len(sys.argv) < 2:
        emit({"event": "error", "detail": "usage: _mlx_runner.py <model_path>"})
        return 2

    model_path = sys.argv[1]

    try:
        from mlx_vlm import load, generate
    except Exception as e:
        emit({"event": "error", "detail": f"import mlx_vlm failed: {e}"})
        return 2

    try:
        model, processor = load(model_path)
    except Exception as e:
        emit({"event": "error", "detail": f"load() failed: {e}\n{traceback.format_exc()}"})
        return 2

    emit({"event": "ready"})

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            emit({"event": "error", "detail": f"bad request json: {e}"})
            continue

        if req.get("cmd") == "exit":
            return 0

        try:
            prompt = req["prompt"]
            max_tokens = int(req.get("max_tokens", 4096))
            audio = req.get("audio")
            image = req.get("image")

            # Build the chat-template content
            if audio and image:
                content = [
                    {"type": "image", "url": image},
                    {"type": "audio", "url": audio},
                    {"type": "text", "text": prompt},
                ]
            elif audio:
                content = [
                    {"type": "audio", "url": audio},
                    {"type": "text", "text": prompt},
                ]
            elif image:
                content = [
                    {"type": "image", "url": image},
                    {"type": "text", "text": prompt},
                ]
            else:
                content = prompt

            chat_prompt = processor.apply_chat_template(
                [{"role": "user", "content": content}],
                tokenize=False,
                add_generation_prompt=True,
            )

            kwargs: dict = {}
            if audio:
                kwargs["audio"] = [audio]
            if image:
                kwargs["image"] = [image]

            t0 = time.perf_counter()
            output = generate(
                model, processor, chat_prompt,
                max_tokens=max_tokens,
                verbose=False,
                **kwargs,
            )
            wall = time.perf_counter() - t0

            text = output.text if hasattr(output, "text") else str(output)
            prompt_tps = float(getattr(output, "prompt_tps", 0) or 0)
            gen_tps = float(getattr(output, "generation_tps", 0) or 0)
            prompt_tokens = int(getattr(output, "prompt_tokens", 0) or 0)
            gen_tokens = int(getattr(output, "generation_tokens", 0) or 0)

            emit({
                "event": "result",
                "prefill_tok_s": round(prompt_tps, 1),
                "decode_tok_s": round(gen_tps, 1),
                "prompt_tokens": prompt_tokens,
                "gen_tokens": gen_tokens,
                "wall_time_s": round(wall, 3),
                "text": text,
            })
        except Exception as e:
            emit({
                "event": "error",
                "detail": f"generate() failed: {e}\n{traceback.format_exc()}",
            })
            # Don't exit — caller may try another request

    return 0


if __name__ == "__main__":
    sys.exit(main())
