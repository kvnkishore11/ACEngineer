# Embed Text in Pi's Input Field Border

How to put status text, labels, or hints directly *into* the editor's top or bottom border line — not in a separate widget.

## The approach: `fitBorder()` + `CustomEditor`

You can't splice into the per-character-ANSI dashes from `super.render()`. Build a fresh border line instead, using the `fitBorder` helper from Pi's official `border-status-editor.ts` example.

## Complete extension

```ts
import { CustomEditor, type ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { truncateToWidth, visibleWidth } from "@mariozechner/pi-tui";

// ── fitBorder: embed text into a border line ──────────────────────
function fitBorder(
  left: string,
  right: string,
  width: number,
  border: (text: string) => string,
  fill: (text: string) => string = border,
): string {
  if (width <= 0) return "";
  if (width === 1) return border("─");
  let leftText = left;
  let rightText = right;
  const fixedWidth = 2;
  const minimumGap = 3;
  while (
    fixedWidth + visibleWidth(leftText) + visibleWidth(rightText) + minimumGap > width &&
    visibleWidth(rightText) > 0
  ) {
    rightText = truncateToWidth(rightText, Math.max(0, visibleWidth(rightText) - 1), "");
  }
  while (
    fixedWidth + visibleWidth(leftText) + visibleWidth(rightText) + minimumGap > width &&
    visibleWidth(leftText) > 0
  ) {
    leftText = truncateToWidth(leftText, Math.max(0, visibleWidth(leftText) - 1), "");
  }
  const gapWidth = Math.max(
    0,
    width - fixedWidth - visibleWidth(leftText) - visibleWidth(rightText),
  );
  return `${border("─")}${leftText}${fill("─".repeat(gapWidth))}${rightText}${border("─")}`;
}

// ── CustomEditor with border text ─────────────────────────────────
class BorderTextEditor extends CustomEditor {
  render(width: number): string[] {
    const lines = super.render(width);
    if (lines.length < 2) return lines;

    const thm = ctx.ui.theme;
    const bc = (s: string) => this.borderColor(s);

    // Top border: label centered-left
    lines[0] = fitBorder(thm.fg("accent", " ✦ My Label ✦ "), "", width, bc);

    // Bottom border: status on left, hint on right
    lines[lines.length - 1] = fitBorder(
      thm.fg("muted", " ◌ idle "),
      thm.fg("dim", " enter to send "),
      width,
      bc,
    );

    return lines;
  }
}

// ── Extension entry point ─────────────────────────────────────────
export default function (pi: ExtensionAPI) {
  pi.on("session_start", (_event, ctx) => {
    if (!ctx.hasUI) return;
    ctx.ui.setEditorComponent(
      (tui, theme, keybindings) => new BorderTextEditor(tui, theme, keybindings),
    );
  });

  pi.on("session_shutdown", (_event, ctx) => {
    ctx?.ui?.setEditorComponent(undefined);
  });
}
```

## What you see

```
── ✦ My Label ✦ ───────────────────────────────────────────────
  [cursor]
── ◌ idle ──────────────────────────────────── enter to send ───
```

## Key points

| Thing | Detail |
|-------|--------|
| `this.borderColor(s)` | Available in any `CustomEditor` — wraps text in the editor's border ANSI color |
| `fitBorder` | Builds the whole border fresh; don't try to splice into `super.render()` dashes |
| Narrow terminals | Graceful — truncates right text first, then left, down to nothing |
| Scroll indicators | `fitBorder` overwrites them; if your editor scrolls, incorporate `─── ↑ N more ───` into your label text |
| `ctx.ui.theme` | Use the closure-captured theme for content colors (`fg()`); `this.borderColor` handles border dashes |
| `truncateToWidth` | Always wrap final lines; Pi crashes on width overflow |
| Restore | Pass `undefined` to `setEditorComponent()` to get the default editor back |

## Width safety

Pi **crashes** if any rendered line exceeds terminal width. The pattern above is safe because `fitBorder` always truncates to fit. If you append status text manually, use:

```ts
// SAFE: concat then truncate
lines[last] = truncateToWidth(lines[last]! + " ◌ idle", width);

// UNSAFE: ANSI-length compensation math is fragile and will break
lines[last] = truncateToWidth(lines[last]!, width - visibleWidth(idle) + ansiLen, "") + idle;
```
