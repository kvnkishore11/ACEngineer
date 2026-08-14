# Available Tools

TypeScript function prototype signatures for all tools available in this session.

```ts
// Reads the contents of a file; supports text files and images (jpg, png, gif, webp).
// Text output is truncated to 2000 lines or 50KB — use offset/limit for large files.
function read(
  path: string,    // Relative or absolute path to the file to read
  offset?: number, // Line number to start reading from (1-indexed)
  limit?: number,  // Maximum number of lines to read
): FileContents;

// Executes a bash command in the current working directory.
// Returns stdout and stderr; output truncated to last 2000 lines or 50KB.
function bash(
  command: string,   // The bash command to execute
  timeout?: number,  // Optional timeout in seconds
): CommandOutput;

// Edits a file by replacing an exact text match with new text.
// oldText must match exactly (including whitespace) — use for surgical edits.
function edit(
  path: string,      // Path to the file to edit (relative or absolute)
  oldText: string,   // Exact text to find and replace (must match exactly)
  newText: string,   // New text to replace the old text with
): void;

// Writes content to a file.
// Creates the file if it doesn't exist, overwrites if it does.
// Automatically creates parent directories as needed.
function write(
  path: string,     // Path to the file to write (relative or absolute)
  content: string,  // Content to write to the file
): void;
```
