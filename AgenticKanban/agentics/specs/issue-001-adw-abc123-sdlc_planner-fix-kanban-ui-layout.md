# Bug: Fix Kanban Board UI Layout and Responsiveness Issues

## Metadata
issue_number: `001`
adw_id: `abc123`
issue_json: `{"title": "Kanban Board UI Layout Issues", "body": "1. I may not need the pipeline summary. 2. within the commands I want the real commands that are present in .claude. Ensure that all the stages are visible I see lot of white space around the application. the stages should be long enough. the widths, heights should be relative to the resolution so your measurements should be in terms of percentages. Lets there be one more stage before which has all the features to be implemented in the pipeline that can have a New Task cta as well"}`

## Bug Description
The Kanban board has several UI/UX issues that affect usability and visual appeal:
1. Pipeline summary section may not be necessary and takes up valuable space
2. Commands palette should display actual .claude commands instead of placeholder content
3. Excessive white space around the application reduces content visibility
4. Stage columns are not sized appropriately for the viewport
5. Fixed pixel sizing causes responsiveness issues across different screen resolutions
6. Missing a "backlog" or "idle" stage for new feature planning with a "New Task" call-to-action button

## Problem Statement
The current Kanban board layout has poor space utilization, lacks responsiveness, and missing functionality for task creation. Users cannot efficiently view all stages simultaneously and the interface doesn't adapt well to different screen sizes.

## Solution Statement
Implement a responsive layout using percentage-based sizing, add a new "Backlog" stage with task creation functionality, optionally hide the pipeline summary, and integrate real .claude commands into the commands palette.

## Steps to Reproduce
1. Open the Kanban board application
2. Observe excessive white space around the board
3. Notice stages are too narrow and don't utilize full viewport width
4. Resize browser window to see poor responsiveness
5. Try to create a new task - no clear entry point in the workflow
6. Open commands palette - shows placeholder content instead of real commands

## Root Cause Analysis
1. **Fixed sizing**: CSS uses fixed pixel values (280px) instead of responsive percentages
2. **Missing stage**: No initial stage for task creation and backlog management
3. **Space utilization**: Pipeline summary and padding consume valuable viewport space
4. **Commands integration**: Commands palette not connected to actual .claude command files
5. **Responsive design**: Grid system doesn't adapt well to different screen sizes

## Relevant Files
Use these files to fix the bug:

- `src/components/KanbanBoard.jsx` - Main Kanban board component that controls layout and stages
- `src/styles/kanban.css` - Contains the CSS grid layout and sizing that needs percentage-based responsive design
- `src/stores/kanbanStore.js` - State management for stages array, needs new "backlog" stage added
- `src/components/CommandsPalette.jsx` - Commands interface that should display real .claude commands
- `src/services/claudeCommandsService.js` - Service for loading and managing .claude commands
- `.claude/commands/conditional_docs.md` - Documentation for understanding styling requirements
- `.claude/commands/test_e2e.md` - E2E testing framework documentation
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test structure

### New Files
- `.claude/commands/e2e/test_kanban_ui_layout.md` - E2E test to validate the UI layout fixes

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Add Backlog Stage to Store
- Add new "backlog" stage as the first stage in the stages array in `kanbanStore.js`
- Configure stage with appropriate icon, color, and "New Task" functionality
- Update stage progression logic to handle the new backlog stage

### 2. Update Kanban Board Component Layout
- Modify `KanbanBoard.jsx` to include the new backlog stage
- Add "New Task" button/CTA to the backlog stage
- Make pipeline summary section conditionally visible (hidden by default)
- Add responsive grid configuration for better stage visibility

### 3. Implement Responsive CSS with Percentage-Based Sizing
- Update `.kanban-board-grid` in `kanban.css` to use percentage-based widths
- Replace fixed 280px columns with flexible percentage-based sizing
- Implement proper viewport height utilization (80vh to 90vh)
- Add responsive breakpoints that maintain stage visibility across screen sizes
- Reduce excessive padding and margins to maximize content area

### 4. Integrate Real Claude Commands
- Update `CommandsPalette.jsx` to load and display actual .claude commands
- Enhance `claudeCommandsService.js` to read command files from `.claude/commands/` directory
- Display command names, descriptions, and usage from actual command files
- Filter and categorize commands appropriately in the palette

### 5. Create E2E Test for UI Layout
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_complex_query.md` and create a new E2E test file in `.claude/commands/e2e/test_kanban_ui_layout.md` that validates the UI layout fixes
- Test responsive behavior across different viewport sizes
- Verify all stages are visible and properly sized
- Validate new backlog stage and "New Task" functionality
- Capture screenshots proving the layout improvements

### 6. Test and Validate Changes
- Run validation commands to ensure zero regressions
- Test responsive behavior manually across different screen sizes
- Verify all existing functionality still works correctly

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `npm run dev` - Start development server to test UI changes
- `npm run build` - Ensure the build process completes without errors
- `npm run lint` - Validate code quality and styling standards
- Manual testing across viewport sizes (mobile: 375px, tablet: 768px, desktop: 1200px+)
- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_kanban_ui_layout.md` test file to validate this functionality works

## Notes
- Use CSS custom properties for consistent spacing and sizing
- Ensure accessibility standards are maintained during layout changes
- Consider implementing CSS Grid subgrid if browser support allows
- The new backlog stage should integrate seamlessly with existing task progression logic
- Pipeline summary visibility should be controlled by a user preference or configuration option
- All changes should maintain backward compatibility with existing task data