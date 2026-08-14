// full-bar-editor.ts
// Replace Pi's input editor with a full-width visual status bar.
// Run with: pi -e /tmp/pi-input-bar-overwrite/full-bar-editor.ts

import { CustomEditor } from "@mariozechner/pi-coding-agent";

function truncateAscii(text: string, width: number): string {
  if (width <= 0) return "";
  if (text.length <= width) return text;
  if (width <= 1) return text.slice(0, width);
  return text.slice(0, width - 1) + "…";
}

function fullWidthAsciiBar(width: number, left: string, center: string, right: string): string {
  if (width <= 0) return "";

  // Keep this ASCII/simple-width for reliability. Apply ANSI styling only after
  // the raw line has been padded to exactly `width` cells.
  const minGap = " ";
  const fixedRight = right;
  const fixedCenter = center;

  let availableForLeft = width - fixedCenter.length - fixedRight.length - minGap.length * 2;
  if (availableForLeft < 0) availableForLeft = 0;

  const safeLeft = truncateAscii(left, availableForLeft);
  let raw = safeLeft + minGap + fixedCenter + minGap + fixedRight;

  if (raw.length > width) raw = truncateAscii(raw, width);
  if (raw.length < width) raw = raw + " ".repeat(width - raw.length);

  return raw;
}

class FullBarEditor extends CustomEditor {
  render(width: number): string[] {
    const raw = fullWidthAsciiBar(
      width,
      " PI DISPLAY MODE ",
      " INPUT DISABLED ",
      " EXTERNAL CONTROL ONLY "
    );

    // Full-row ANSI styling. Because `raw` is already padded to width, the
    // background spans the whole editor row.
    const bgPurple = "\x1b[48;5;57m";
    const fgWhite = "\x1b[38;5;231m";
    const bold = "\x1b[1m";
    const reset = "\x1b[0m";

    return [`${bgPurple}${fgWhite}${bold}${raw}${reset}`];
  }

  handleInput(data: string): void {
    // Preserve extension shortcuts.
    if (this.onExtensionShortcut?.(data)) return;

    // Preserve paste-image shortcut if configured.
    if (this.keybindings.matches(data, "app.clipboard.pasteImage")) {
      this.onPasteImage?.();
      return;
    }

    // Preserve Escape / interrupt.
    if (this.keybindings.matches(data, "app.interrupt")) {
      if (!this.isShowingAutocomplete()) {
        const handler = this.onEscape ?? this.actionHandlers.get("app.interrupt");
        if (handler) {
          handler();
          return;
        }
      }
      super.handleInput(data);
      return;
    }

    // Preserve Ctrl+D / exit when empty.
    if (this.keybindings.matches(data, "app.exit")) {
      if (this.getText().length === 0) {
        const handler = this.onCtrlD ?? this.actionHandlers.get("app.exit");
        if (handler) handler();
      }
      return;
    }

    // Preserve other app-level actions, such as model switch shortcuts.
    for (const [action, handler] of this.actionHandlers) {
      if (
        action !== "app.interrupt" &&
        action !== "app.exit" &&
        this.keybindings.matches(data, action)
      ) {
        handler();
        return;
      }
    }

    // Swallow all normal typing/Enter/etc. This is not an input field anymore.
  }
}

export default function (pi: any) {
  pi.on("session_start", async (_event: any, ctx: any) => {
    if (!ctx.hasUI) return;

    ctx.ui.setEditorComponent((tui: any, theme: any, keybindings: any) => {
      return new FullBarEditor(tui, theme, keybindings, {});
    });

    ctx.ui.setStatus("full-bar-editor", "input replaced by visual bar");
  });

  // Defense-in-depth: if a prompt somehow gets submitted by non-extension
  // keyboard interaction, block it.
  pi.on("input", async (event: any, ctx: any) => {
    if (event.source === "extension") return { action: "continue" };
    ctx.ui.notify("Input field is disabled; this row is a visual bar.", "warning");
    return { action: "handled" };
  });

  pi.on("session_shutdown", async (_event: any, ctx: any) => {
    if (!ctx?.hasUI) return;
    ctx.ui.setEditorComponent(undefined);
  });
}
