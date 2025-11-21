---
description: Generate comprehensive unit tests for front-end components
argument-hint: component-file-path
allowed-tools: Read, Write, Bash
model: sonnet
---

# Generate Component Tests

Generate comprehensive, production-ready unit tests for front-end components following industry best practices.

## Purpose
Execute the `Workflow` and `Report` sections to create thorough test coverage for a component, including unit tests, integration tests, accessibility tests, and edge cases.

## Variables
COMPONENT_PATH: $1  # Path to component file (e.g., ./src/components/Button/Button.tsx)
TEST_FRAMEWORK: vitest  # vitest | jest
COMPONENT_LIB: react  # react | vue | svelte | angular
OUTPUT_PATH: auto  # auto (same dir as component) | custom path
COVERAGE_TARGET: 80  # Minimum coverage percentage
TEST_STYLE: rtl  # rtl (React Testing Library) | enzyme | testing-library

## Workflow

### 1. VALIDATE Input
1. REQUIRED: {{COMPONENT_PATH}} must be provided
2. CRITICAL: Verify component file exists:
   ```bash
   test -f {{COMPONENT_PATH}} || echo "File not found"
   ```
3. IF file not found: Exit with clear error message
4. Determine test file path:
   - IF {{OUTPUT_PATH}} is "auto": Same directory as component
   - ELSE: Use {{OUTPUT_PATH}}
   - Test filename: `ComponentName.test.tsx` (or .ts, .jsx, .js based on original)

### 2. Analyze Component Structure
1. Read component file at {{COMPONENT_PATH}}
2. IMPORTANT: Extract component metadata:
   - **Component name**: Identify export (default or named)
   - **Component type**:
     - Functional vs Class component
     - Hooks used (useState, useEffect, useContext, custom hooks)
     - Props interface/PropTypes
   - **Props analysis**:
     - Required props
     - Optional props with defaults
     - Callback props (event handlers)
     - Children support
   - **State management**:
     - Local state (useState)
     - Context usage
     - External state (Redux, Zustand, etc.)
   - **Side effects**:
     - useEffect hooks
     - API calls
     - Subscriptions
     - Timers
   - **Conditional rendering**:
     - IF statements
     - Ternary operators
     - Logical AND (&&)
   - **User interactions**:
     - Click handlers
     - Form submissions
     - Keyboard events
     - Focus/blur events
   - **Accessibility features**:
     - ARIA attributes
     - Semantic HTML
     - Keyboard navigation
   - **Dependencies**:
     - External libraries
     - Custom hooks
     - Utility functions
     - Child components

3. THOROUGHLY analyze component logic to identify:
   - Edge cases (empty data, null, undefined)
   - Error conditions
   - Loading states
   - Success states
   - Boundary conditions (min/max values)

### 3. Design Test Suite Architecture
1. IMPORTANT: Organize tests by concern:
   ```typescript
   describe('ComponentName', () => {
     describe('Rendering', () => {
       // Basic rendering tests
     });

     describe('Props', () => {
       // Props validation and default values
     });

     describe('User Interactions', () => {
       // Click, input, keyboard events
     });

     describe('State Management', () => {
       // State changes and updates
     });

     describe('Side Effects', () => {
       // API calls, subscriptions, timers
     });

     describe('Accessibility', () => {
       // ARIA, keyboard navigation, screen readers
     });

     describe('Edge Cases', () => {
       // Null, undefined, empty, boundary conditions
     });

     describe('Error Handling', () => {
       // Error states, fallbacks
     });
   });
   ```

2. Calculate required test cases:
   - Minimum: 1 test per user interaction
   - Add: 1 test per conditional branch
   - Add: 1 test per side effect
   - Add: 2-3 accessibility tests
   - Add: 3-5 edge case tests
   - Target: 15-30 tests for typical component

### 4. CRITICAL: Generate Test File Header
1. Create imports section:
   ```typescript
   import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
   import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
   import userEvent from '@testing-library/user-event';
   import { ComponentName } from './ComponentName';
   import type { ComponentNameProps } from './ComponentName.types';

   // Mock dependencies if needed
   vi.mock('./hooks/useCustomHook', () => ({
     useCustomHook: vi.fn(),
   }));

   // Mock external modules
   vi.mock('axios');
   ```

2. ALWAYS: Set up test utilities:
   ```typescript
   // Helper to render component with common props
   const renderComponent = (props: Partial<ComponentNameProps> = {}) => {
     const defaultProps: ComponentNameProps = {
       // Set up sensible defaults
       data: mockData,
       onAction: vi.fn(),
       ...props,
     };

     return {
       ...render(<ComponentName {...defaultProps} />),
       props: defaultProps,
     };
   };

   // Common test data
   const mockData = {
     id: '1',
     title: 'Test Title',
     description: 'Test Description',
   };
   ```

### 5. Generate Rendering Tests
1. ESSENTIAL: Basic rendering test:
   ```typescript
   describe('Rendering', () => {
     it('renders without crashing', () => {
       renderComponent();
       expect(screen.getByRole('button')).toBeInTheDocument();
     });

     it('renders with required props', () => {
       renderComponent({
         data: mockData,
         onAction: vi.fn(),
       });
       expect(screen.getByText(mockData.title)).toBeInTheDocument();
     });

     it('IMPORTANT: renders null when data is missing', () => {
       renderComponent({ data: null });
       expect(screen.queryByRole('button')).not.toBeInTheDocument();
     });

     it('applies custom className', () => {
       const { container } = renderComponent({ className: 'custom-class' });
       expect(container.firstChild).toHaveClass('custom-class');
     });
   });
   ```

### 6. Generate Props Tests
1. THOROUGHLY test all prop variations:
   ```typescript
   describe('Props', () => {
     it('uses default prop values', () => {
       renderComponent();
       const element = screen.getByRole('button');
       expect(element).toHaveClass('variant-primary'); // default variant
       expect(element).toHaveClass('size-medium'); // default size
     });

     it('IMPORTANT: respects all variant options', () => {
       const variants = ['primary', 'secondary', 'tertiary'] as const;
       variants.forEach(variant => {
         const { container } = renderComponent({ variant });
         expect(container.firstChild).toHaveClass(`variant-${variant}`);
       });
     });

     it('respects disabled prop', () => {
       renderComponent({ disabled: true });
       expect(screen.getByRole('button')).toHaveAttribute('aria-disabled', 'true');
     });

     it('forwards ref correctly', () => {
       const ref = React.createRef<HTMLDivElement>();
       render(<ComponentName ref={ref} data={mockData} onAction={vi.fn()} />);
       expect(ref.current).toBeInstanceOf(HTMLDivElement);
     });
   });
   ```

### 7. Generate User Interaction Tests
1. CRITICAL: Test all user interactions:
   ```typescript
   describe('User Interactions', () => {
     it('calls onClick handler when clicked', async () => {
       const user = userEvent.setup();
       const onAction = vi.fn();
       renderComponent({ onAction });

       await user.click(screen.getByRole('button'));
       expect(onAction).toHaveBeenCalledTimes(1);
       expect(onAction).toHaveBeenCalledWith('clicked');
     });

     it('CRITICAL: does not call handler when disabled', async () => {
       const user = userEvent.setup();
       const onAction = vi.fn();
       renderComponent({ onAction, disabled: true });

       await user.click(screen.getByRole('button'));
       expect(onAction).not.toHaveBeenCalled();
     });

     it('handles keyboard navigation (Enter key)', async () => {
       const user = userEvent.setup();
       const onAction = vi.fn();
       renderComponent({ onAction });

       const button = screen.getByRole('button');
       button.focus();
       await user.keyboard('{Enter}');
       expect(onAction).toHaveBeenCalled();
     });

     it('handles keyboard navigation (Space key)', async () => {
       const user = userEvent.setup();
       const onAction = vi.fn();
       renderComponent({ onAction });

       const button = screen.getByRole('button');
       button.focus();
       await user.keyboard(' ');
       expect(onAction).toHaveBeenCalled();
     });

     it('IMPORTANT: handles form submission', async () => {
       const user = userEvent.setup();
       const onSubmit = vi.fn((e) => e.preventDefault());
       render(
         <form onSubmit={onSubmit}>
           <ComponentName data={mockData} onAction={vi.fn()} />
         </form>
       );

       await user.click(screen.getByRole('button'));
       expect(onSubmit).toHaveBeenCalled();
     });
   });
   ```

### 8. Generate State Management Tests
1. THOROUGHLY test state changes:
   ```typescript
   describe('State Management', () => {
     it('toggles state on interaction', async () => {
       const user = userEvent.setup();
       renderComponent();

       const button = screen.getByRole('button');
       expect(button).toHaveAttribute('aria-expanded', 'false');

       await user.click(button);
       expect(button).toHaveAttribute('aria-expanded', 'true');

       await user.click(button);
       expect(button).toHaveAttribute('aria-expanded', 'false');
     });

     it('IMPORTANT: updates derived state correctly', async () => {
       const user = userEvent.setup();
       const { rerender } = renderComponent({ count: 0 });

       expect(screen.getByText('Count: 0')).toBeInTheDocument();

       rerender(<ComponentName {...defaultProps} count={5} />);
       expect(screen.getByText('Count: 5')).toBeInTheDocument();
     });

     it('maintains state across re-renders', async () => {
       const user = userEvent.setup();
       const { rerender } = renderComponent();

       await user.click(screen.getByRole('button'));
       expect(screen.getByText('Clicked')).toBeInTheDocument();

       rerender(<ComponentName {...defaultProps} />);
       expect(screen.getByText('Clicked')).toBeInTheDocument();
     });
   });
   ```

### 9. Generate Side Effects Tests
1. CRITICAL: Test async operations and side effects:
   ```typescript
   describe('Side Effects', () => {
     it('fetches data on mount', async () => {
       const mockFetch = vi.fn().mockResolvedValue({ data: mockData });
       vi.mocked(axios.get).mockResolvedValue({ data: mockData });

       renderComponent();

       await waitFor(() => {
         expect(axios.get).toHaveBeenCalledWith('/api/data');
       });

       expect(screen.getByText(mockData.title)).toBeInTheDocument();
     });

     it('IMPORTANT: handles API errors gracefully', async () => {
       const consoleError = vi.spyOn(console, 'error').mockImplementation();
       vi.mocked(axios.get).mockRejectedValue(new Error('API Error'));

       renderComponent();

       await waitFor(() => {
         expect(screen.getByText(/error/i)).toBeInTheDocument();
       });

       consoleError.mockRestore();
     });

     it('CRITICAL: cleans up subscriptions on unmount', () => {
       const unsubscribe = vi.fn();
       const subscribe = vi.fn(() => unsubscribe);

       const { unmount } = renderComponent({ subscribe });

       expect(subscribe).toHaveBeenCalled();
       expect(unsubscribe).not.toHaveBeenCalled();

       unmount();
       expect(unsubscribe).toHaveBeenCalled();
     });

     it('cancels pending requests on unmount', async () => {
       const abortController = new AbortController();
       const abortSpy = vi.spyOn(abortController, 'abort');

       const { unmount } = renderComponent();
       unmount();

       await waitFor(() => {
         expect(abortSpy).toHaveBeenCalled();
       });
     });
   });
   ```

### 10. Generate Accessibility Tests
1. ESSENTIAL: Test accessibility requirements:
   ```typescript
   describe('Accessibility', () => {
     it('CRITICAL: has correct ARIA role', () => {
       renderComponent();
       expect(screen.getByRole('button')).toBeInTheDocument();
     });

     it('CRITICAL: has accessible name', () => {
       renderComponent({ ariaLabel: 'Submit form' });
       expect(screen.getByRole('button')).toHaveAccessibleName('Submit form');
     });

     it('IMPORTANT: supports keyboard focus', () => {
       renderComponent();
       const button = screen.getByRole('button');
       button.focus();
       expect(button).toHaveFocus();
     });

     it('has correct tabIndex', () => {
       renderComponent();
       expect(screen.getByRole('button')).toHaveAttribute('tabIndex', '0');
     });

     it('CRITICAL: indicates disabled state to assistive tech', () => {
       renderComponent({ disabled: true });
       const button = screen.getByRole('button');
       expect(button).toHaveAttribute('aria-disabled', 'true');
       expect(button).toHaveAttribute('tabIndex', '-1');
     });

     it('provides describedBy relationship', () => {
       renderComponent({ ariaDescribedBy: 'help-text' });
       expect(screen.getByRole('button')).toHaveAttribute(
         'aria-describedby',
         'help-text'
       );
     });

     it('IMPORTANT: announces state changes to screen readers', async () => {
       const user = userEvent.setup();
       renderComponent();

       const button = screen.getByRole('button');
       expect(button).toHaveAttribute('aria-pressed', 'false');

       await user.click(button);
       expect(button).toHaveAttribute('aria-pressed', 'true');
     });
   });
   ```

### 11. Generate Edge Cases Tests
1. THOROUGHLY test boundary conditions:
   ```typescript
   describe('Edge Cases', () => {
     it('handles null data gracefully', () => {
       renderComponent({ data: null });
       expect(screen.queryByRole('button')).not.toBeInTheDocument();
     });

     it('handles undefined data gracefully', () => {
       renderComponent({ data: undefined });
       expect(screen.queryByRole('button')).not.toBeInTheDocument();
     });

     it('handles empty array', () => {
       renderComponent({ items: [] });
       expect(screen.getByText(/no items/i)).toBeInTheDocument();
     });

     it('handles empty string', () => {
       renderComponent({ title: '' });
       expect(screen.queryByText(/title/i)).not.toBeInTheDocument();
     });

     it('IMPORTANT: handles very long text', () => {
       const longText = 'A'.repeat(1000);
       renderComponent({ description: longText });
       expect(screen.getByText(longText)).toBeInTheDocument();
     });

     it('handles special characters in text', () => {
       const specialText = '<script>alert("xss")</script>';
       renderComponent({ description: specialText });
       expect(screen.getByText(specialText)).toBeInTheDocument();
       expect(screen.queryByRole('script')).not.toBeInTheDocument();
     });

     it('CRITICAL: handles maximum number of items', () => {
       const maxItems = new Array(1000).fill(mockData);
       renderComponent({ items: maxItems });
       expect(screen.getAllByRole('listitem')).toHaveLength(1000);
     });

     it('handles rapid successive clicks', async () => {
       const user = userEvent.setup();
       const onAction = vi.fn();
       renderComponent({ onAction });

       const button = screen.getByRole('button');
       await user.tripleClick(button);

       // Should debounce or handle multiple clicks
       expect(onAction.mock.calls.length).toBeLessThanOrEqual(3);
     });
   });
   ```

### 12. Generate Error Handling Tests
1. CRITICAL: Test error scenarios:
   ```typescript
   describe('Error Handling', () => {
     it('displays error message when present', () => {
       renderComponent({ error: 'Something went wrong' });
       expect(screen.getByText('Something went wrong')).toBeInTheDocument();
     });

     it('IMPORTANT: recovers from error state', async () => {
       const user = userEvent.setup();
       const { rerender } = renderComponent({ error: 'Error' });

       expect(screen.getByText('Error')).toBeInTheDocument();

       rerender(<ComponentName {...defaultProps} error={null} />);
       expect(screen.queryByText('Error')).not.toBeInTheDocument();
     });

     it('CRITICAL: displays fallback UI on render error', () => {
       const consoleError = vi.spyOn(console, 'error').mockImplementation();

       // Trigger error by passing invalid prop
       expect(() => {
         renderComponent({ data: { invalid: true } });
       }).toThrow();

       consoleError.mockRestore();
     });

     it('handles validation errors', async () => {
       const user = userEvent.setup();
       renderComponent();

       const input = screen.getByRole('textbox');
       await user.type(input, 'invalid');
       await user.click(screen.getByRole('button', { name: /submit/i }));

       expect(screen.getByText(/invalid input/i)).toBeInTheDocument();
     });
   });
   ```

### 13. Add Setup and Teardown
1. ALWAYS: Include proper cleanup:
   ```typescript
   describe('ComponentName', () => {
     beforeEach(() => {
       // Reset mocks before each test
       vi.clearAllMocks();

       // Reset any global state
       localStorage.clear();
       sessionStorage.clear();
     });

     afterEach(() => {
       // Cleanup after each test
       vi.restoreAllMocks();
     });

     // Tests here...
   });
   ```

### 14. Generate Performance Tests (Optional)
1. IF component has performance concerns:
   ```typescript
   describe('Performance', () => {
     it('IMPORTANT: does not re-render unnecessarily', () => {
       const renderSpy = vi.fn();
       const TestComponent = () => {
         renderSpy();
         return <ComponentName data={mockData} onAction={vi.fn()} />;
       };

       const { rerender } = render(<TestComponent />);
       expect(renderSpy).toHaveBeenCalledTimes(1);

       // Re-render with same props
       rerender(<TestComponent />);
       expect(renderSpy).toHaveBeenCalledTimes(1); // Should not re-render
     });

     it('handles large datasets efficiently', () => {
       const largeDataset = new Array(10000).fill(mockData);
       const start = performance.now();

       renderComponent({ items: largeDataset });

       const end = performance.now();
       expect(end - start).toBeLessThan(1000); // Should render in <1s
     });
   });
   ```

### 15. CRITICAL: Validate Test Quality
1. Run tests and check coverage:
   ```bash
   npm run test -- {{TEST_FILE_PATH}} --coverage
   ```

2. VALIDATE coverage meets target:
   - Lines: >={{COVERAGE_TARGET}}%
   - Branches: >={{COVERAGE_TARGET}}%
   - Functions: >={{COVERAGE_TARGET}}%
   - Statements: >={{COVERAGE_TARGET}}%

3. IF coverage < target:
   - Identify uncovered lines
   - Add tests for uncovered branches
   - Regenerate missing test cases

4. IMPORTANT: Check test quality:
   - [ ] Tests are independent (can run in any order)
   - [ ] Tests are deterministic (same result every time)
   - [ ] Tests are fast (<100ms each)
   - [ ] Tests use meaningful assertions
   - [ ] Tests have clear descriptions
   - [ ] No test doubles (mocks) for implementation details
   - [ ] Tests follow AAA pattern (Arrange, Act, Assert)

### 16. Add Test Documentation
1. Add comments for complex tests:
   ```typescript
   it('handles complex user flow', async () => {
     // Arrange: Set up component with initial state
     const user = userEvent.setup();
     const onComplete = vi.fn();
     renderComponent({ onComplete });

     // Act: Simulate user interactions
     await user.click(screen.getByRole('button', { name: /start/i }));
     await user.type(screen.getByRole('textbox'), 'test input');
     await user.click(screen.getByRole('button', { name: /submit/i }));

     // Assert: Verify expected outcome
     await waitFor(() => {
       expect(onComplete).toHaveBeenCalledWith({ input: 'test input' });
     });
   });
   ```

## Report

Provide comprehensive test summary:

```typescript
{
  status: 'success' | 'failure',
  componentPath: string,
  testFilePath: string,
  testSuiteStructure: {
    totalDescribeBlocks: number,
    totalTests: number,
    testsByCategory: {
      rendering: number,
      props: number,
      interactions: number,
      state: number,
      sideEffects: number,
      accessibility: number,
      edgeCases: number,
      errorHandling: number,
      performance: number,
    },
  },
  coverage: {
    lines: number,      // percentage
    branches: number,   // percentage
    functions: number,  // percentage
    statements: number, // percentage
    meetsTarget: boolean,
  },
  testQuality: {
    allTestsPass: boolean,
    averageTestDuration: number, // ms
    slowestTest: { name: string, duration: number },
    warnings: string[],
  },
  recommendations: string[],
  nextSteps: string[],
}
```

## Error Handling

- IF {{COMPONENT_PATH}} does not exist:
  → Exit with: "Component file not found at {{COMPONENT_PATH}}"
  → Suggest running `find . -name "*.tsx" -o -name "*.ts"` to locate

- IF component is too complex (>500 lines):
  → Generate tests but warn: "Component is large, consider splitting"
  → Suggest refactoring into smaller components
  → Generate additional test files for sub-components

- IF component has no testable logic:
  → Generate basic rendering tests only
  → Warn: "Component is purely presentational, limited tests generated"

- IF dependencies cannot be mocked:
  → Document which dependencies need manual mocking
  → Provide examples of how to mock them
  → Generate tests with TODO comments

- IF coverage < {{COVERAGE_TARGET}}:
  → Report which lines/branches are uncovered
  → Suggest additional test cases
  → Offer to regenerate with more tests

- IF tests fail after generation:
  → Report failing tests with error messages
  → Suggest fixes based on error type
  → Offer to debug and regenerate

## Examples

### Example 1: Simple Button Component
```bash
/generate-component-tests ./src/components/Button/Button.tsx
```

**Generated**:
- `Button.test.tsx` (280 lines, 25 tests)
  - 3 rendering tests
  - 4 props tests
  - 6 interaction tests
  - 7 accessibility tests
  - 5 edge cases tests

**Coverage**: 95% lines, 92% branches, 100% functions

---

### Example 2: Complex Form Component
```bash
/generate-component-tests ./src/components/ContactForm/ContactForm.tsx
```

**Generated**:
- `ContactForm.test.tsx` (450 lines, 38 tests)
  - 4 rendering tests
  - 5 props tests
  - 12 interaction tests (form fields, validation, submission)
  - 5 state management tests
  - 4 side effects tests (API calls)
  - 6 accessibility tests
  - 2 performance tests

**Coverage**: 88% lines, 85% branches, 95% functions

---

### Example 3: Data Table with Hooks
```bash
/generate-component-tests ./src/components/DataTable/DataTable.tsx
```

**Generated**:
- `DataTable.test.tsx` (520 lines, 42 tests)
  - 5 rendering tests
  - 8 props tests
  - 10 interaction tests (sorting, filtering, pagination)
  - 8 state management tests
  - 6 accessibility tests
  - 5 edge cases tests (empty, large datasets)

**Coverage**: 92% lines, 89% branches, 94% functions

---

## Best Practices Applied

### Test Organization
- **Describe blocks**: Logical grouping by concern
- **Clear naming**: "should..." or "handles..." patterns
- **AAA pattern**: Arrange, Act, Assert in every test

### Test Independence
- No shared state between tests
- Each test can run in isolation
- Use `beforeEach`/`afterEach` for cleanup

### Test Readability
- Descriptive test names
- Helper functions for common setup
- Comments for complex scenarios
- Avoid test logic (if/else in tests)

### Test Coverage
- Happy path (main use case)
- Edge cases (boundaries)
- Error cases (failures)
- Accessibility (a11y requirements)
- User interactions (all events)

### Mock Strategy
- Mock external dependencies (APIs, modules)
- Don't mock component internals
- Use real implementations when possible
- Spy on functions to verify calls

### Performance
- Fast tests (<100ms each)
- Parallel execution safe
- No unnecessary waits
- Cleanup after each test

---

## Integration with Development Workflow

### Pre-commit Hook
```bash
# Run tests before commit
npm run test -- --run
```

### CI/CD Pipeline
```yaml
# .github/workflows/test.yml
- name: Run Tests
  run: npm run test -- --coverage
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

### Test-Driven Development (TDD)
```bash
# 1. Generate tests first
/generate-component-tests ./src/components/NewFeature/NewFeature.tsx

# 2. Run tests (they should fail)
npm run test -- --watch

# 3. Implement component until tests pass
```

---

**IMPORTANT**: Every test follows these principles:
- Tests behavior, not implementation
- Uses real user interactions (userEvent over fireEvent)
- Queries by accessible roles (getByRole over getByTestId)
- Waits for async operations (waitFor, findBy)
- Cleans up after itself
- Runs in isolation

**CRITICAL**: Tests are documentation. They show how the component should be used and what behavior it guarantees.
