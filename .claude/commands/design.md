# Design

Create a high-level design document with solutions, architecture, and visual diagrams for the given idea or prompt.

## Variables
prompt: $ARGUMENTS

## Instructions

- If the prompt is not provided, stop and ask the user to provide it.
- IMPORTANT: Create a comprehensive design document that provides high-level understanding without any code implementation
- Focus on conceptual architecture, solution approaches, and system design
- Include mermaid diagrams to visualize the design
- The design should be appropriately detailed based on the idea complexity:
  - Simple ideas: Focus on core concept and basic architecture
  - Complex ideas: Include detailed system design, data flow, and component interactions
- Create the design document in the current directory with filename: `design-{descriptive-name}.md`
  - Replace `{descriptive-name}` with a short, descriptive name based on the idea
- IMPORTANT: When you finish your design, return only the path to the design file created.
- IMPORTANT: Replace every <placeholder> in the `Design Format` with the requested value
- Think through the requirements, constraints, and architectural considerations
- Focus on high-level patterns, not implementation details

## Workflow

1. **Analyze the Prompt**: Understand the core idea, requirements, and scope
2. **Design Architecture**: Create high-level system design and component relationships
3. **Create Visualizations**: Generate mermaid diagrams for key architectural concepts
4. **Write Design Document**: Create the design document following the Design Format template
5. IMPORTANT: Return ONLY the path to the design document created and nothing else.

## Design Format

```md
# Design: <idea name>

## Overview
<provide a clear, concise summary of the idea and what it aims to achieve>

## Problem Statement
<clearly define the problem or opportunity this idea addresses>

## Solution Approach
<describe the high-level solution approach and key concepts>

## Core Requirements
<list the essential functional and non-functional requirements>

## System Architecture

### High-Level Architecture
<describe the overall system architecture and key components>

```mermaid
<create a system architecture diagram showing main components and their relationships>
```

### Component Overview
<describe each major component and its responsibilities>

### Data Flow
<describe how data flows through the system>

```mermaid
<create a data flow diagram showing how information moves through the system>
```

## Key Design Decisions
<list and justify important architectural and design decisions>

## Technology Considerations
<discuss technology stack considerations, patterns, and architectural styles>

## Scalability & Performance
<address scalability, performance, and capacity considerations>

## Security & Compliance
<outline security requirements and compliance considerations>

## Integration Points
<describe how this system integrates with external systems or services>

## User Experience Design

### User Journey
<describe the key user workflows and interactions>

```mermaid
<create a user journey flowchart>
```

### Interface Design Principles
<outline key UI/UX principles and design guidelines>

## Implementation Strategy
<provide high-level implementation approach and phases>

## Risk Assessment
<identify potential risks and mitigation strategies>

## Success Metrics
<define how success will be measured>

## Future Considerations
<discuss potential future enhancements and evolution paths>

## Conclusion
<summarize the design and next steps>
```

## Task
Use the idea description from the `prompt` variable to create a comprehensive design document.

## Report

IMPORTANT: Exclusively return the path to the design file created.