# Part 1: HBnB Evolution - Technical Documentation

## Overview
This directory contains the architectural design and high-level documentation for the HBnB Evolution application.

## Contents

### 📊 Diagrams
- `diagrams/package_diagram.mmd` - Three-layer architecture with Facade pattern

### 📖 Documentation
- `ARCHITECTURE.md` - Detailed architecture explanation
- `README.md` - This file

## Task 0: High-Level Package Diagram

### Objective
Create a visual representation of the application's three-layer architecture with Facade pattern communication.

### Deliverables Completed
✅ Package diagram showing all three layers
✅ Component identification within each layer
✅ Facade pattern communication pathways
✅ Detailed architecture documentation
✅ Layer responsibility breakdown

### Architecture Components

#### Presentation Layer
- API Controllers for each entity (User, Place, Review, Amenity)
- Request handlers and validators
- Response formatters

#### Business Logic Layer
- HBnB Facade (main entry point)
- Entity models (User, Place, Review, Amenity)
- Business rules and validations
- Relationship management

#### Persistence Layer
- Data repositories for each entity
- Database access layer
- Query execution and caching

## How to View Diagrams

### Option 1: VS Code
Install "Markdown Preview Mermaid Support" extension, then open `.mmd` files.

### Option 2: Mermaid Live Editor
Visit https://mermaid.live/ and paste diagram content.

### Option 3: GitHub
Push to GitHub - diagrams render automatically in README files.

## Next Steps

- Part 2: Detailed class diagrams for business logic layer
- Part 3: Sequence diagrams for API calls
- Part 4: Complete documentation compilation

## Design Patterns

### Facade Pattern
The application uses the Facade pattern to provide a unified interface between layers:
- Simplifies complex subsystem interactions
- Reduces coupling between layers
- Provides single entry point for operations
- Hides implementation details

### Repository Pattern
Data access is abstracted through repositories:
- Separates business logic from data access
- Enables easier testing with mock repositories
- Provides consistent data access interface

## Layer Communication Flow

```
Client Request
      ↓
[Presentation Layer]
  - API Controller receives request
  - Validates input format
  - Authenticates user
      ↓
[Business Logic Facade]
  - Routes to appropriate handler
  - Applies business rules
  - Manages entity operations
      ↓
[Persistence Layer]
  - Repository executes query
  - Database returns data
  - Validates data integrity
      ↓
Response flows back through layers
```

## Contributing

When adding new features:
1. Update relevant diagrams
2. Document new components
3. Follow existing patterns
4. Update this README

## References

- [UML Package Diagrams](https://www.uml-diagrams.org/package-diagrams.html)
- [Facade Pattern](https://refactoring.guru/design-patterns/facade)
- [Layered Architecture](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch01.html)
