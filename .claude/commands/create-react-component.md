---
description: Generate production-ready React component with best practices
argument-hint: component-description
allowed-tools: Write, Read, Edit
model: sonnet
---

# Create React Component

Generate a scalable, maintainable React component following industry best practices.

## Purpose
Execute the `Workflow` and `Report` sections to create a production-ready React component with TypeScript, proper architecture, and comprehensive documentation.

## Variables
COMPONENT_DESCRIPTION: $1  # What the component should do
COMPONENT_DIR: ./src/components
HOOKS_DIR: ./src/hooks
TYPES_DIR: ./src/types
STYLES_APPROACH: css-modules  # css-modules | styled-components | tailwind
TYPESCRIPT: true
TEST_FRAMEWORK: vitest  # vitest | jest

## Workflow

### 1. Parse Component Requirements
1. Analyze {{COMPONENT_DESCRIPTION}} to extract:
   - Component name (PascalCase)
   - Primary responsibility (single responsibility principle)
   - Required props/data
   - User interactions
   - State requirements
   - Side effects (API calls, subscriptions, etc.)
   - Accessibility requirements

### 2. IMPORTANT: Design Component Architecture
1. Determine component type:
   - **Presentational**: Pure UI, no business logic
   - **Container**: Handles state and logic, minimal UI
   - **Compound**: Parent + children pattern (e.g., Tabs, Accordion)
   - **Layout**: Structural, handles positioning only

2. CRITICAL: Apply Design Principles:
   - **Single Responsibility**: Component does ONE thing well
   - **Composition over Inheritance**: Build from smaller components
   - **Separation of Concerns**: UI, logic, styles are separate
   - **DRY**: Extract reusable logic to hooks
   - **KISS**: Keep implementation simple and clear

3. Plan file structure:
   ```
   components/
   └── ComponentName/
       ├── ComponentName.tsx           # Main component
       ├── ComponentName.module.css    # Styles (if css-modules)
       ├── ComponentName.test.tsx      # Tests
       ├── ComponentName.types.ts      # TypeScript types
       ├── index.ts                    # Public exports
       └── hooks/                      # Component-specific hooks
           └── useComponentName.ts
   ```

### 3. Generate TypeScript Types
1. Create `{{TYPES_DIR}}/ComponentName.types.ts`:

   ```typescript
   // IMPORTANT: Use descriptive prop names with proper types
   export interface ComponentNameProps {
     // Required props first
     data: DataType;
     onAction: (value: string) => void;

     // Optional props with defaults documented
     variant?: 'primary' | 'secondary' | 'tertiary';
     size?: 'small' | 'medium' | 'large';
     disabled?: boolean;
     className?: string;

     // Accessibility props
     ariaLabel?: string;
     ariaDescribedBy?: string;
   }

   // Internal state types
   export interface ComponentNameState {
     isOpen: boolean;
     selectedValue: string | null;
   }

   // ALWAYS export helper types
   export type ComponentNameVariant = ComponentNameProps['variant'];
   export type ComponentNameSize = ComponentNameProps['size'];
   ```

2. VALIDATE type definitions:
   - All required props are marked
   - Optionals have `?` and documented defaults
   - Event handlers use proper function signatures
   - Accessibility props included

### 4. Extract Custom Hooks (if needed)
1. IF component has complex logic or state:
   - Create custom hook in `hooks/useComponentName.ts`:

   ```typescript
   import { useState, useCallback, useEffect } from 'react';
   import type { ComponentNameState } from '../ComponentName.types';

   export const useComponentName = (initialValue?: string) => {
     const [state, setState] = useState<ComponentNameState>({
       isOpen: false,
       selectedValue: initialValue ?? null,
     });

     // IMPORTANT: Memoize callbacks to prevent re-renders
     const handleOpen = useCallback(() => {
       setState(prev => ({ ...prev, isOpen: true }));
     }, []);

     const handleClose = useCallback(() => {
       setState(prev => ({ ...prev, isOpen: false }));
     }, []);

     const handleSelect = useCallback((value: string) => {
       setState(prev => ({ ...prev, selectedValue: value }));
     }, []);

     // Cleanup side effects
     useEffect(() => {
       return () => {
         // Cleanup logic here
       };
     }, []);

     return {
       ...state,
       handleOpen,
       handleClose,
       handleSelect,
     };
   };
   ```

2. VALIDATE hook:
   - Uses proper React hooks patterns
   - Callbacks are memoized with `useCallback`
   - Cleanup in `useEffect` return
   - Returns stable API

### 5. CRITICAL: Generate Main Component
1. Create `{{COMPONENT_DIR}}/ComponentName/ComponentName.tsx`:

   ```typescript
   import { memo, forwardRef } from 'react';
   import type { ComponentNameProps } from './ComponentName.types';
   import { useComponentName } from './hooks/useComponentName';
   import styles from './ComponentName.module.css';

   /**
    * ComponentName - [Brief description]
    *
    * @example
    * ```tsx
    * <ComponentName
    *   data={data}
    *   onAction={handleAction}
    *   variant="primary"
    * />
    * ```
    */
   export const ComponentName = memo(
     forwardRef<HTMLDivElement, ComponentNameProps>(
       (
         {
           data,
           onAction,
           variant = 'primary',
           size = 'medium',
           disabled = false,
           className = '',
           ariaLabel,
           ariaDescribedBy,
         },
         ref
       ) => {
         // IMPORTANT: Extract complex logic to custom hooks
         const {
           isOpen,
           selectedValue,
           handleOpen,
           handleClose,
           handleSelect,
         } = useComponentName();

         // ALWAYS: Early returns for conditional rendering
         if (!data) {
           return null;
         }

         // Compose CSS classes
         const componentClasses = [
           styles.component,
           styles[`variant-${variant}`],
           styles[`size-${size}`],
           disabled && styles.disabled,
           className,
         ]
           .filter(Boolean)
           .join(' ');

         // Event handlers
         const handleClick = () => {
           if (disabled) return;
           handleOpen();
           onAction('clicked');
         };

         return (
           <div
             ref={ref}
             className={componentClasses}
             role="button"
             tabIndex={disabled ? -1 : 0}
             aria-label={ariaLabel}
             aria-describedby={ariaDescribedBy}
             aria-disabled={disabled}
             onClick={handleClick}
             onKeyDown={(e) => {
               if (e.key === 'Enter' || e.key === ' ') {
                 e.preventDefault();
                 handleClick();
               }
             }}
           >
             {/* Component content */}
             <div className={styles.content}>
               {/* Keep JSX clean and readable */}
             </div>
           </div>
         );
       }
     )
   );

   ComponentName.displayName = 'ComponentName';
   ```

2. VALIDATE component implementation:
   - Uses `memo` for performance optimization
   - Uses `forwardRef` for ref forwarding
   - Props destructured with defaults
   - Custom hooks extract complex logic
   - Event handlers are clean and focused
   - Accessibility attributes present (role, aria-*, tabIndex)
   - Keyboard navigation support
   - Conditional rendering uses early returns
   - CSS classes composed properly

### 6. Generate Styles
1. IF {{STYLES_APPROACH}} is "css-modules":
   Create `ComponentName.module.css`:

   ```css
   /* IMPORTANT: Use CSS custom properties for theming */
   .component {
     /* Layout */
     display: flex;
     align-items: center;
     gap: var(--spacing-md, 1rem);

     /* Sizing */
     padding: var(--spacing-sm, 0.5rem);

     /* Visual */
     background-color: var(--color-background, #fff);
     border: 1px solid var(--color-border, #ccc);
     border-radius: var(--border-radius, 0.25rem);

     /* Interaction */
     cursor: pointer;
     transition: all 0.2s ease-in-out;
   }

   /* ALWAYS: Include hover and focus states */
   .component:hover:not(.disabled) {
     border-color: var(--color-primary, #0066cc);
   }

   .component:focus-visible {
     outline: 2px solid var(--color-focus, #0066cc);
     outline-offset: 2px;
   }

   /* Variants */
   .variant-primary {
     background-color: var(--color-primary, #0066cc);
     color: var(--color-on-primary, #fff);
   }

   .variant-secondary {
     background-color: var(--color-secondary, #6c757d);
     color: var(--color-on-secondary, #fff);
   }

   /* Sizes */
   .size-small {
     padding: var(--spacing-xs, 0.25rem) var(--spacing-sm, 0.5rem);
     font-size: var(--font-size-sm, 0.875rem);
   }

   .size-medium {
     padding: var(--spacing-sm, 0.5rem) var(--spacing-md, 1rem);
     font-size: var(--font-size-md, 1rem);
   }

   .size-large {
     padding: var(--spacing-md, 1rem) var(--spacing-lg, 1.5rem);
     font-size: var(--font-size-lg, 1.125rem);
   }

   /* States */
   .disabled {
     opacity: 0.5;
     cursor: not-allowed;
     pointer-events: none;
   }

   /* IMPORTANT: Responsive design */
   @media (max-width: 768px) {
     .component {
       padding: var(--spacing-xs, 0.25rem);
     }
   }
   ```

2. IF {{STYLES_APPROACH}} is "tailwind":
   Use utility classes with proper organization

3. IF {{STYLES_APPROACH}} is "styled-components":
   Create styled-components file

### 7. Generate Comprehensive Tests
1. Create `ComponentName.test.tsx`:

   ```typescript
   import { describe, it, expect, vi } from 'vitest';
   import { render, screen, fireEvent } from '@testing-library/react';
   import userEvent from '@testing-library/user-event';
   import { ComponentName } from './ComponentName';

   describe('ComponentName', () => {
     const mockData = { /* test data */ };
     const mockOnAction = vi.fn();

     it('renders without crashing', () => {
       render(
         <ComponentName
           data={mockData}
           onAction={mockOnAction}
         />
       );
       expect(screen.getByRole('button')).toBeInTheDocument();
     });

     it('IMPORTANT: handles user interactions correctly', async () => {
       const user = userEvent.setup();
       render(
         <ComponentName
           data={mockData}
           onAction={mockOnAction}
         />
       );

       await user.click(screen.getByRole('button'));
       expect(mockOnAction).toHaveBeenCalledWith('clicked');
     });

     it('supports keyboard navigation', async () => {
       const user = userEvent.setup();
       render(
         <ComponentName
           data={mockData}
           onAction={mockOnAction}
         />
       );

       const button = screen.getByRole('button');
       button.focus();
       await user.keyboard('{Enter}');
       expect(mockOnAction).toHaveBeenCalled();
     });

     it('CRITICAL: respects disabled state', () => {
       render(
         <ComponentName
           data={mockData}
           onAction={mockOnAction}
           disabled={true}
         />
       );

       const button = screen.getByRole('button');
       expect(button).toHaveAttribute('aria-disabled', 'true');
       fireEvent.click(button);
       expect(mockOnAction).not.toHaveBeenCalled();
     });

     it('applies variant styles correctly', () => {
       const { container } = render(
         <ComponentName
           data={mockData}
           onAction={mockOnAction}
           variant="primary"
         />
       );

       expect(container.firstChild).toHaveClass('variant-primary');
     });

     it('forwards ref correctly', () => {
       const ref = React.createRef<HTMLDivElement>();
       render(
         <ComponentName
           ref={ref}
           data={mockData}
           onAction={mockOnAction}
         />
       );

       expect(ref.current).toBeInstanceOf(HTMLDivElement);
     });

     it('IMPORTANT: meets accessibility requirements', () => {
       render(
         <ComponentName
           data={mockData}
           onAction={mockOnAction}
           ariaLabel="Test component"
         />
       );

       const button = screen.getByRole('button');
       expect(button).toHaveAttribute('aria-label', 'Test component');
       expect(button).toHaveAttribute('tabIndex', '0');
     });
   });
   ```

### 8. Create Public Export
1. Create `index.ts`:

   ```typescript
   export { ComponentName } from './ComponentName';
   export type {
     ComponentNameProps,
     ComponentNameVariant,
     ComponentNameSize,
   } from './ComponentName.types';
   export { useComponentName } from './hooks/useComponentName';
   ```

### 9. Generate Documentation
1. Create `ComponentName.stories.tsx` (Storybook):

   ```typescript
   import type { Meta, StoryObj } from '@storybook/react';
   import { ComponentName } from './ComponentName';

   const meta: Meta<typeof ComponentName> = {
     title: 'Components/ComponentName',
     component: ComponentName,
     tags: ['autodocs'],
     argTypes: {
       variant: {
         control: 'select',
         options: ['primary', 'secondary', 'tertiary'],
       },
       size: {
         control: 'select',
         options: ['small', 'medium', 'large'],
       },
     },
   };

   export default meta;
   type Story = StoryObj<typeof ComponentName>;

   export const Default: Story = {
     args: {
       data: { /* sample data */ },
       onAction: (value) => console.log('Action:', value),
     },
   };

   export const Primary: Story = {
     args: {
       ...Default.args,
       variant: 'primary',
     },
   };

   export const Disabled: Story = {
     args: {
       ...Default.args,
       disabled: true,
     },
   };
   ```

### 10. CRITICAL: Validate Best Practices
1. **Performance**:
   - [ ] Component wrapped in `memo`
   - [ ] Callbacks memoized with `useCallback`
   - [ ] Computed values memoized with `useMemo`
   - [ ] No inline object/array creation in JSX
   - [ ] Proper dependency arrays in hooks

2. **Accessibility**:
   - [ ] Semantic HTML elements
   - [ ] ARIA attributes (role, aria-label, etc.)
   - [ ] Keyboard navigation support
   - [ ] Focus management
   - [ ] Color contrast ratios met

3. **TypeScript**:
   - [ ] All props typed
   - [ ] No `any` types
   - [ ] Proper interface exports
   - [ ] Generic types where appropriate

4. **Code Quality**:
   - [ ] Single Responsibility Principle
   - [ ] DRY - no code duplication
   - [ ] KISS - simple and clear
   - [ ] Functions < 20 lines
   - [ ] File < 250 lines

5. **Testing**:
   - [ ] Unit tests for logic
   - [ ] Integration tests for interactions
   - [ ] Accessibility tests
   - [ ] Edge cases covered

6. **Documentation**:
   - [ ] JSDoc comments on component
   - [ ] Usage examples
   - [ ] Storybook stories
   - [ ] Props documented

## Report

Provide structured summary of generated component:

```typescript
{
  status: 'success' | 'failure',
  componentName: string,
  filesCreated: {
    component: string,        // ComponentName.tsx
    types: string,           // ComponentName.types.ts
    styles: string,          // ComponentName.module.css
    tests: string,           // ComponentName.test.tsx
    hooks: string[],         // Custom hooks
    stories: string,         // ComponentName.stories.tsx
    index: string,           // index.ts
  },
  bestPractices: {
    performance: boolean,    // memo, useCallback, useMemo
    accessibility: boolean,  // ARIA, keyboard, semantic HTML
    typescript: boolean,     // Proper typing
    testing: boolean,        // Comprehensive tests
    documentation: boolean,  // JSDoc, examples, Storybook
  },
  linesOfCode: number,
  complexity: 'low' | 'medium' | 'high',
  nextSteps: string[],
}
```

## Error Handling

- IF {{COMPONENT_DESCRIPTION}} is vague or unclear:
  → Ask clarifying questions about:
    - Primary responsibility
    - Required interactions
    - Data structure
    - Accessibility requirements
  → Generate placeholder component with TODOs

- IF component becomes too complex (>250 lines):
  → Suggest breaking into smaller components
  → Create compound component pattern
  → Extract presentational components

- IF custom hook logic is complex:
  → Add detailed comments
  → Consider splitting into multiple hooks
  → Add unit tests for hook

- IF styling conflicts with {{STYLES_APPROACH}}:
  → Confirm approach with user
  → Adjust generation accordingly

## Examples

### Example 1: Simple Button Component
```bash
/create-react-component "A reusable button component with primary, secondary, and tertiary variants, supporting different sizes and disabled state. Should be keyboard accessible and work with screen readers."
```

**Generated**:
- `Button/Button.tsx` (85 lines)
- `Button/Button.types.ts` (15 lines)
- `Button/Button.module.css` (60 lines)
- `Button/Button.test.tsx` (120 lines)
- `Button/index.ts` (5 lines)

**Result**: Production-ready button with full accessibility, TypeScript support, and comprehensive tests.

---

### Example 2: Data Table Component
```bash
/create-react-component "A data table component that displays tabular data with sorting, filtering, and pagination. Supports column configuration, custom cell renderers, and row selection. Must be accessible and performant with large datasets (1000+ rows)."
```

**Generated**:
- `DataTable/DataTable.tsx` (180 lines)
- `DataTable/DataTable.types.ts` (45 lines)
- `DataTable/hooks/useDataTable.ts` (95 lines) - sorting, filtering, pagination logic
- `DataTable/hooks/useVirtualization.ts` (60 lines) - performance optimization
- `DataTable/DataTable.module.css` (85 lines)
- `DataTable/DataTable.test.tsx` (200 lines)
- `DataTable/components/` - TableHeader, TableRow, TableCell sub-components
- `DataTable/index.ts` (10 lines)

**Result**: Complex table with virtualization, full feature set, extracted hooks for reusability.

---

### Example 3: Modal Dialog
```bash
/create-react-component "A modal dialog component that overlays the main content. Supports custom header, body, and footer. Should trap focus, close on Esc key, prevent body scroll when open, and follow WAI-ARIA dialog pattern."
```

**Generated**:
- `Modal/Modal.tsx` (120 lines)
- `Modal/Modal.types.ts` (20 lines)
- `Modal/hooks/useModal.ts` (45 lines) - focus trap, escape handling
- `Modal/hooks/useLockBodyScroll.ts` (25 lines) - scroll prevention
- `Modal/Modal.module.css` (70 lines)
- `Modal/Modal.test.tsx` (150 lines)
- `Modal/index.ts` (5 lines)

**Result**: Fully accessible modal with proper focus management and UX patterns.

---

## Best Practices Applied

### 1. Component Architecture
- **Single Responsibility**: Each component/file has one clear purpose
- **Composition**: Build complex UIs from simple components
- **Separation**: UI (JSX), Logic (hooks), Styles (CSS), Types (TS) are separate

### 2. Performance
- `memo`: Prevent unnecessary re-renders
- `useCallback`: Memoize event handlers
- `useMemo`: Memoize expensive computations
- Lazy loading: Code splitting for large components

### 3. Accessibility (a11y)
- Semantic HTML: `<button>`, `<nav>`, `<main>`, etc.
- ARIA attributes: `role`, `aria-label`, `aria-describedby`
- Keyboard support: Tab navigation, Enter/Space activation, Escape to close
- Focus management: Trap focus in modals, restore focus on close
- Screen reader support: Proper labeling and state announcements

### 4. TypeScript
- Strict typing: No `any`
- Interface-based: Props, state, events all typed
- Generic components: Reusable with different data types
- Type exports: Share types across application

### 5. Testing
- Unit tests: Individual functions and hooks
- Integration tests: Component interactions
- Accessibility tests: ARIA, keyboard, screen reader
- Edge cases: Empty state, error state, loading state

### 6. Code Quality
- DRY: Extract reusable logic to hooks
- KISS: Simple, readable implementation
- YAGNI: Don't add features you don't need yet
- Small functions: < 20 lines each
- Small files: < 250 lines each

### 7. Documentation
- JSDoc: Comment component purpose and usage
- Examples: Show common use cases
- Storybook: Interactive component showcase
- TypeScript: Self-documenting through types

---

## Integration with Project

The generated component integrates seamlessly with:
- **TypeScript** projects
- **React Testing Library** + Vitest/Jest
- **Storybook** for documentation
- **CSS Modules**, Styled Components, or Tailwind
- **ESLint** and **Prettier** configs
- **CI/CD** pipelines (tests run automatically)

---

**IMPORTANT**: Every component generated follows these principles ALWAYS. No exceptions. This ensures consistency, maintainability, and quality across your entire component library.
