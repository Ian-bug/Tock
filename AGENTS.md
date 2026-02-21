# Agent Guide: Tock TUI Clock

This document helps agents work effectively with the Tock codebase.

## Project Overview

Tock is a minimal Terminal User Interface (TUI) clock application written in Python. It displays time in four different styles (digital, simple, binary, and words) and uses the `curses` library for the terminal interface.

**Key characteristics:**
- Single-file application (`tock.py`)
- Object-oriented design with a single `TockClock` class
- Python 3.6+ with type hints
- Cross-platform (Windows requires `windows-curses`, Linux/macOS use built-in curses)

## Essential Commands

### Running the Application
```bash
python tock.py
```

### Installing Dependencies (Windows only)
```bash
pip install -r requirements.txt
```
**Note:** On Linux and macOS, `curses` is included with Python and no installation is needed.

### Testing
The README mentions `python test_display.py` for testing display logic, but this file is currently listed in `.gitignore` and does not exist in the repository. Do not attempt to run non-existent test files.

## Project Structure

```
tuiclock/
├── tock.py              # Main clock application (all code is here)
├── requirements.txt     # Python dependencies (windows-curses only)
├── README.md           # User documentation
├── LICENSE             # MIT License
└── .gitignore          # Standard Python gitignore + project-specific ignores
```

## Code Organization

### Main Class: `TockClock`

The entire application lives in the `TockClock` class. Key sections:

**Initialization (`__init__`)**: Sets up curses state, display styles, and ASCII art digit definitions.

**Time Methods**:
- `get_current_time()` - Returns tuple (h, m, s) from `datetime.now()`

**Display Style Methods** (one per style):
- `draw_digital_clock()` - 6-line ASCII art display
- `draw_simple_clock()` - Single-line 24h text format
- `draw_binary_clock()` - Dot grid binary representation (H, M, S rows with bit labels)
- `draw_words_clock()` - Natural language time display
- `get_clock_display()` - Dispatcher that calls appropriate style method based on `self.current_style`

**Rendering Methods**:
- `center_text()` - String centering utility
- `draw_centered()` - Renders text lines centered on curses screen
- `draw_footer()` - Renders help text at bottom of screen

**Input Handling**:
- `handle_input()` - Processes keyboard input (arrow keys for style change, H for footer toggle, Q to quit)

**Main Loop**:
- `run()` - Main application loop with curses initialization and cleanup

## Code Patterns and Conventions

### Naming Conventions
- **Class names**: `PascalCase` (e.g., `TockClock`)
- **Methods/Functions**: `snake_case` (e.g., `get_current_time`, `draw_digital_clock`)
- **Variables**: `snake_case` (e.g., `time_str`, `char_lines`)
- **Constants**: Use class attributes in `__init__` (e.g., `self.digits`, `self.styles`)

### Type Hints
All methods use Python type hints:
- Return types: `-> str`, `-> List[str]`, `-> Tuple[int, int, int]`
- Parameters: `text: str`, `max_width: int`, `screen`
- Imports from `typing`: `List`, `Tuple`

### Error Handling
- Curses operations wrapped in `try/except curses.error` blocks
- Used in `draw_centered()` and `draw_footer()` to handle edge cases where text doesn't fit
- Main application wraps entire loop in `try/finally` for proper curses cleanup

### Display Style Data Structures

**ASCII Art Digits** (`self.digits` dictionary):
- Keys: character strings `'0'` through `'9'` and `':'`
- Values: lists of 6 strings (6 lines per digit)
- Spacing: Each line includes trailing spaces for consistent width
- Pattern: Dense Unicode block characters (`█`) for filled areas

**Binary Clock**:
- Uses format string `format(value, '06b')` for 6-bit representation
- Unicode filled circle `●` for 1 bits, empty circle `○` for 0 bits
- Includes bit position labels (6, 5, 4, 3, 2, 1)

**Word Clock**:
- Uses hardcoded dictionaries for number-to-word conversion
- Special handling for common times (1, 15, 30, 45 minutes)
- Fallback to generic number words for other values

## Important Gotchas

### Platform-Specific Dependencies
- **Windows**: Requires `windows-curses>=2.3.0` in `requirements.txt`
- **Linux/macOS**: Curses is built-in, no dependency needed
- The project targets Windows first (based on requirements.txt presence)

### Curses Initialization Pattern
Always follow this exact sequence when working with curses:
```python
self.stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
self.stdscr.nodelay(True)  # Non-blocking input
self.stdscr.keypad(True)
```

And cleanup in `finally` block:
```python
curses.nocbreak()
self.stdscr.keypad(False)
curses.echo()
curses.endwin()
```

### Input Handling
- Uses `self.stdscr.nodelay(True)` for non-blocking input
- Uses `curses.halfdelay(10)` to wait up to 1 second for input
- Small `time.sleep(0.1)` ensures smooth 1-second updates

### Screen Coordinates
- `screen.getmaxyx()` returns `(height, width)` as tuple
- Coordinates are (row, column) - Y comes before X
- Always wrap `screen.addstr()` in `try/except curses.error`

### Display Style Cycling
- Styles stored in `self.styles` list: `['digital', 'simple', 'binary', 'words']`
- Current style tracked as index in `self.current_style`
- Cycle with modulo arithmetic: `(self.current_style + 1) % len(self.styles)`

### Text Rendering
- ASCII art uses double-width spaces for spacing between characters
- Centering uses `text.center(max_width)` or manual calculation: `(width - len(text)) // 2`
- Empty lines in display lists are significant for proper spacing

## Adding New Display Styles

To add a new clock display style:

1. **Add style name to `self.styles` list** in `__init__`:
   ```python
   self.styles = ['digital', 'simple', 'binary', 'words', 'newstyle']
   ```

2. **Implement drawing method** following existing pattern:
   ```python
   def draw_newstyle_clock(self, h: int, m: int, s: int) -> List[str]:
       """Generate newstyle clock display"""
       # Your implementation here
       return lines  # List of strings, one per display line
   ```

3. **Add case in `get_clock_display()` method**:
   ```python
   elif style == 'newstyle':
       return self.draw_newstyle_clock(h, m, s)
   ```

4. **Method signature requirements**:
   - Must accept `(self, h: int, m: int, s: int)` parameters
   - Must return `List[str]` (list of display lines)
   - Should not handle drawing/rendering directly (that's `draw_centered()`'s job)

## Modifying Keyboard Controls

To add or modify keyboard shortcuts:

1. **Edit `handle_input()` method**:
   ```python
   key = self.stdscr.getch()

   if key == curses.KEY_LEFT:  # Example: Left arrow
       # Your action
   elif key == ord('x') or key == ord('X'):  # Example: X key
       # Your action (case-insensitive)
   ```

2. **Key constants**:
   - Arrow keys: `curses.KEY_LEFT`, `curses.KEY_RIGHT`, `curses.KEY_UP`, `curses.KEY_DOWN`
   - Single characters: `ord('a')` for lowercase, `ord('A')` for uppercase
   - Special keys: `curses.KEY_ENTER`, `curses.KEY_ESCAPE`, etc.

## Testing Considerations

**Important:** No test suite currently exists in the repository. When adding tests:

1. Mock curses module - `curses` requires a terminal and can't be tested in standard environments
2. Focus on testing pure Python methods:
   - Time formatting logic (e.g., `draw_simple_clock`, `_number_to_words`)
   - Style dispatch logic in `get_clock_display`
   - String centering in `center_text`
3. Avoid testing UI rendering directly (`draw_centered`, `draw_footer`) - these depend on curses

## Code Style

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Not strictly enforced, but generally under 100 characters
- **Docstrings**: Triple-quoted strings, present on class and all public methods
- **Comments**: Minimal, used only where logic is non-obvious
- **Imports**: Standard library first, then type hints (no external deps except curses)

## Common Tasks

### Changing ASCII Art Font
Edit the `self.digits` dictionary in `__init__`. Each digit must have exactly 6 lines of equal length with consistent spacing.

### Adjusting Refresh Rate
Modify `time.sleep(0.1)` in the main loop and `curses.halfdelay(10)` (value is in tenths of seconds, so 10 = 1 second).

### Modifying Footer Text
Change `footer_text` string in `draw_footer()` method.

### Changing Initial Display Style
Set `self.current_style = 0` in `__init__` to desired index (0=digital, 1=simple, 2=binary, 3=words).

## Known Limitations

- Single-file architecture - all code is in `tock.py`
- No automated testing infrastructure
- No build system or packaging configuration
- No CI/CD pipeline
- Limited to 4 display styles (extensible but no plugin system)
- No configuration file or settings persistence
