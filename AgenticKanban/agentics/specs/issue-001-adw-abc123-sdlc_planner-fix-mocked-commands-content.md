# Bug: Commands showing mocked content instead of real data

## Metadata
issue_number: `001`
adw_id: `abc123`
issue_json: `{"title": "Commands Content Mocked Instead of Real Data", "body": "The content with the /commands is mocked and not real data of the /commands but are still mocked and this is not fixed."}`

## Bug Description
The Commands Palette in the AgenticKanban application is displaying mock content instead of the actual content from the real `.claude/commands/*.md` files. When users interact with commands in the UI, they see generic mock descriptions rather than the detailed, specific command instructions that exist in the filesystem.

## Problem Statement
The commandContentService is attempting to read command content via a backend API that doesn't exist, causing it to fall back to generated mock content instead of reading the actual command files directly from the filesystem.

## Solution Statement
Modify the commandContentService to read command files directly from the filesystem instead of attempting to use a non-existent backend API, ensuring real command content is displayed to users.

## Steps to Reproduce
1. Start the application with `npm run dev`
2. Open the Commands Palette in the UI
3. Select any command (e.g., `/bug`, `/feature`, `/test`)
4. Observe that the command content shows generic mock descriptions instead of the actual command content from the `.md` files

## Root Cause Analysis
The `commandContentService.js` attempts to fetch command content via the `/api/commands/read` endpoint, but there is no backend API service running. When this API call fails, the service falls back to the `generateMockContent()` method which produces generic mock descriptions. The real command files exist and contain proper content, but the service needs to be modified to read files directly from the filesystem instead of trying to use an API.

## Relevant Files
Use these files to fix the bug:

- `src/services/commandContentService.js` - Contains the service that handles reading command content and fallback to mock content
- `.claude/commands/*.md` - The actual command files that contain real content
- `src/services/claudeCommandsService.js` - Service that discovers and manages commands, calls commandContentService
- `vite.config.js` - May need configuration to handle markdown file imports

### New Files
- `.claude/commands/e2e/test_fix_mocked_commands_content.md` - E2E test to validate commands show real content

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Use Direct File Imports with Vite
- Replace the API-based file reading logic with direct imports using `import.meta.glob()`
- Use Vite's built-in capability to import markdown files as text
- Remove all API-related code from `readCommandContent()` method
- Ensure the method returns the same data structure as before

### Import All Command Files at Build Time
- Use `import.meta.glob('.claude/commands/**/*.md', { as: 'raw' })` to import all markdown files
- Create a static mapping of command paths to their content
- Remove the need for any runtime file system access or API calls
- Maintain the existing caching mechanism for performance

### Update Error Handling
- Remove all API-related error handling from `commandContentService.js`
- Add appropriate error handling for missing files in the imported glob
- Ensure graceful fallback to mock content only when files are truly missing from the build
- Add better logging for import issues

### Test Real Content Loading
- Verify that real command content is loaded correctly from imported files
- Test with multiple command files to ensure all are accessible via the glob import
- Ensure token counting works with real content from direct imports
- Validate content caching is working properly with the imported content

### Create E2E Test
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_complex_query.md` and create a new E2E test file in `.claude/commands/e2e/test_fix_mocked_commands_content.md` that validates commands show real content instead of mock content. The test should verify that opening the Commands Palette shows actual command descriptions and not generic mock text.

### Run Validation Commands
- Execute all validation commands to ensure the bug is fixed with zero regressions

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `npm run dev:client-only` - Start the client application only and verify it starts correctly
- Open Commands Palette and verify real command content is displayed (not mock content)
- Verify that opening multiple commands shows actual content from their respective `.md` files
- Check browser DevTools Console tab to ensure no API-related errors
- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_fix_mocked_commands_content.md` test file to validate this functionality works
- `npm run lint` - Run linting to validate code quality
- `npm run build` - Run build to validate the application builds correctly and includes command files

## Notes
- No backend server is needed for this application - it should run as a client-only application
- Command files need to be bundled as static assets or imported directly
- The contentCache in commandContentService should improve performance once direct file access is working
- Mock content fallback should remain as a safety measure but should only be used when actual files are unavailable
- Consider using Vite's import.meta.glob() or similar bundling features to include command files at build time