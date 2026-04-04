# AGENTS.md - Font Generator Development Guide

This document provides guidelines for agents working on this font generator codebase.

## Project Overview

This is a Python-based font generator that simulates pen nib strokes to create blackletter-style fonts. The core modules are in `ownimage/font_generator/`.

## Build, Run, and Test Commands

### Running the Application

```bash
# Run demo scripts
python pen_nib_demo.py
python pen_nib_demo2.py

# Run test utilities
python test.py
python test_stroke.py
python testOffset.py
```

### Running Tests

```bash
# Run all tests using unittest discovery
python -m unittest discover

# Run a specific test file
python -m unittest test_stroke

# Run a specific test function
python -m unittest test_stroke.test_geometry
```

### Linting and Type Checking

```bash
# Run flake8 on the font_generator module
python -m flake8 ownimage/font_generator/

# Run mypy for type checking
python -m mypy ownimage/font_generator/

# Run black for formatting
python -m black ownimage/font_generator/

# Run isort for import sorting
python -m isort ownimage/font_generator/
```

---

## Code Style Guidelines

### General Principles

- Write clean, readable code with meaningful names
- Keep functions focused on a single responsibility
- Use docstrings for public APIs and complex functions
- Prefer explicit over implicit

### Import Conventions

**Relative imports for internal modules:**
```python
from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .vector import Vector

# Absolute imports for standard library and third-party
from dataclasses import dataclass, field
from math import cos, sin, radians
```

**Import ordering (per-file):**
1. Standard library imports
2. Third-party imports
3. Internal module imports (grouped, separated by blank line)

### Formatting

- **Line length**: 100 characters maximum
- **Indentation**: 4 spaces (no tabs)
- **Blank lines**: Two between top-level definitions, one between method definitions
- **Trailing whitespace**: Remove all trailing whitespace

### Type Hints

Use type hints for all function parameters and return values:
```python
def geometry(self, start: Vector, fp: FontParameters, scale: float, 
             before: Strokeable, after: Strokeable, geom_set: GeometrySet) -> Vector:
```

Use string quotes for forward references:
```python
def from_font_parameters(fp: FontParameters) -> "PenNib":
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `class PenNib:` |
| Functions/methods | snake_case | `def geometry():` |
| Variables | snake_case | `vec = Vector(1, 2)` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_ITERATIONS = 100` |
| Modules | snake_case | `pen_nib.py` |
| Private methods | prefix with `_` | `def _internal_method():` |

### Dataclasses

This codebase heavily uses frozen dataclasses for immutable data structures:

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Vector:
    x: float = 0.0
    y: float = 0.0
    
    # For computed fields that can't be set in __init__
    direction: Vector = field(init=False)
    
    def __post_init__(self):
        direction = self.vec.normalized()
        object.__setattr__(self, "direction", direction)
```

**Rules for frozen dataclasses:**
- Never modify `self` directly after initialization
- Use `object.__setattr__(self, "field", value)` in `__post_init__` for computed fields
- Return new instances from methods rather than mutating

### Error Handling

- Use explicit exceptions with descriptive messages
- Prefer `RuntimeError` with clear messages over generic exceptions
- Let exceptions propagate when appropriate
```python
if e.stroke_type == StrokeType.Extend:
    return Stroke(self.vec + e.vec, self.stroke_type)
raise RuntimeError("Can only extend by a Stroke of type Extend.")
```

### Property Patterns

Use `@property` for computed attributes that are cheap to calculate:
```python
@property
def tl(self): return self._offset(-self.width / 2, self.thickness / 2)
```

### Static Methods

Use `@staticmethod` for constructor-like methods that don't need `self`:
```python
@staticmethod
def from_xy(x: float, y: float, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
    return Stroke(Vector(x, y), stroke_type)

@staticmethod
def down(length: float = 1, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
    return Stroke(Vector(0, -length), stroke_type)
```

### Docstrings

Use Google-style docstrings for public methods:
```python
def cross(self, other: "Vector") -> float:
    """2D cross product (returns scalar)."""
    return self.x * other.y - self.y * other.x
```

### File Organization

Each module should contain:
1. Imports (stdlib, third-party, local)
2. Module-level docstring (if applicable)
3. Class definitions
4. Functions

---

## Testing Guidelines

- Place tests in the project root or a `tests/` directory
- Use `unittest.TestCase` or simple test functions
- Test files should be named `test_*.py` or `*_test.py`
- Run individual tests with: `python -m unittest test_module.test_function`

---

## Dependencies

Key dependencies (from code analysis):
- `shapely` - Geometry operations
- `svgpathtools` - SVG path manipulation
- Standard library: `dataclasses`, `math`, `typing`

---

## Module Structure

```
ownimage/font_generator/
├── __init__.py
├── vector.py          # 2D vector math
├── stroke.py          # Stroke representation
├── pen_nib.py        # Pen nib geometry
├── pen_stroke.py     # Pen stroke rendering
├── stroke_type.py    # Stroke type enum
├── strokeable.py     # Strokeable interface
├── font_parameters.py # Font configuration
├── geometry_set.py   # Geometry collection
├── compound_stroke.py # Combined strokes
├── stroke_line.py    # Linear strokes
├── geom.py           # Geometry utilities
├── blackletter.py    # Blackletter font generation
├── display.py        # Display utilities
├── birdfont_reader.py # Birdfont file parsing
└── ui.py             # User interface
```
