# How to Hide Pi's Input Bar and Overwrite It With a Visual Bar

This shows how to keep the **full headed Pi TUI** visible while replacing the normal editor/input field with a **single full-width visual status bar**.

The important API is:

```ts
ctx.ui.setEditorComponent(...)
```

The important rendering rule is:

```ts
render(width: number): string[] {
  return [oneFullWidthLine];
}
```

If you want the editor to disappear entirely, return `[]`.

If you want to overwrite it with a visual row/bar, return exactly one string in the array:

```ts
return [barLine];
```

---

## Run the example

From this temp folder:

```bash
okey
pi -e /tmp/pi-input-bar-overwrite/full-bar-editor.ts
```

Or from anywhere:

```bash
okey
pi -e /tmp/pi-input-bar-overwrite/full-bar-editor.ts
```

The normal Pi TUI will open, but the input editor row will be replaced by a full-width visual bar that says:

```text
PI DISPLAY MODE    INPUT DISABLED    EXTERNAL CONTROL ONLY
```

Direct typing is swallowed. The row is not a real input field anymore.

---

## Mental model

Pi's interactive layout normally contains a default `CustomEditor` component. That component renders the bordered input field and handles typed text.

This extension swaps that editor component:

```ts
ctx.ui.setEditorComponent((tui, theme, keybindings) => {
  return new FullBarEditor(tui, theme, keybindings, {});
});
```

`FullBarEditor` still extends Pi's `CustomEditor`, but its `render()` method draws a status bar instead of the input box.

The default editor might render something like:

```text
╭────────────────────────╮
│ type here              │
╰────────────────────────╯
```

This custom editor renders one row instead:

```text
 PI DISPLAY MODE             INPUT DISABLED             EXTERNAL CONTROL ONLY 
```

With ANSI background styling applied across the full row.

---

## Fully working extension

Save as:

```text
/tmp/pi-input-bar-overwrite/full-bar-editor.ts
```

Then run:

```bash
pi -e /tmp/pi-input-bar-overwrite/full-bar-editor.ts
```

```ts
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
```

---

## The key parts

### 1. Replace the editor

```ts
ctx.ui.setEditorComponent((tui, theme, keybindings) => {
  return new FullBarEditor(tui, theme, keybindings, {});
});
```

Pi calls this factory with:

```ts
tui, theme, keybindings
```

Those are passed into the `CustomEditor` constructor.

---

### 2. Render one full-width line

```ts
render(width: number): string[] {
  const raw = fullWidthAsciiBar(width, " PI DISPLAY MODE ", " INPUT DISABLED ", " EXTERNAL CONTROL ONLY ");
  return [`\x1b[48;5;57m\x1b[38;5;231m\x1b[1m${raw}\x1b[0m`];
}
```

The returned array has exactly one string, so the editor area becomes one row tall.

The raw string is padded to exactly `width` before the background color is applied, so the color spans the whole row.

---

### 3. Swallow normal input

The extension intentionally does **not** call `super.handleInput(data)` for normal printable input.

That means typing letters does not mutate an invisible editor buffer.

```ts
// Swallow all normal typing/Enter/etc. This is not an input field anymore.
```

---

### 4. Preserve operational shortcuts

The custom editor still forwards important Pi controls:

- extension shortcuts
- paste-image shortcut
- Escape / interrupt
- Ctrl+D / exit
- other registered app actions

That is why the example extends `CustomEditor` instead of implementing a bare editor object.

---

## If you want the bar to disappear entirely

Change:

```ts
return [styledBar];
```

to:

```ts
return [];
```

That hides the editor visually instead of overwriting it with a bar.

---

## Important caveat

This replaces what the editor draws. Pi may still reserve the editor's layout slot, but the normal input box is gone. Returning one line gives you a deliberate visual status bar in that slot. Returning zero lines makes it visually empty.
