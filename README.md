<div align="center">

# Tock

A modern, minimal Terminal User Interface (TUI) clock with multiple display styles.

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com)

</div>

## Features

- **4 Distinct Display Styles**
  - 🎚️ **Digital** - Large ASCII art digits
  - 📟 **Simple** - Clean centered 24-hour format
  - 🔢 **Binary** - Bit grid representation of H:M:S
  - 📝 **Words** - Minimalist word-based display

- **Intuitive Navigation**
  - ← / → Arrow keys to cycle through styles
  - H key to toggle help footer
  - Q to quit

- **Modern UI**
  - No borders - clock floats freely
  - Perfectly centered (auto-adjusts on resize)
  - Flicker-free 1-second updates

## Installation

### Prerequisites

- Python 3.6 or higher

### Install Dependencies

**Windows:**
```bash
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
# curses is included with Python, no extra dependencies needed
```

## Usage

### Run the Clock
```bash
python tock.py
```

### Keyboard Controls
| Key | Action |
|-----|--------|
| `←` | Previous display style |
| `→` | Next display style |
| `H` | Toggle help footer |
| `Q` | Quit application |

## Display Styles

### Digital
Large 6-character ASCII art digits for a classic digital clock look.
```
  ████     ████ 
█    █   █    █
█    █   █    █
█    █   █    █
  ████     ████
```

### Simple
Clean, minimal text format.
```
12:34:56
```

### Binary
Dot grid showing binary representation of hours, minutes, and seconds.
```
H ○ ○ ● ● ○
  6  5  4  3  2  1
M ● ○ ○ ● ● ●
  6  5  4  3  2  1
```

### Words
Time displayed in natural language.
```
TWELVE THIRTY
ONE O'CLOCK
```

## Development

### Testing
Run the display test to verify all clock styles:
```bash
python test_display.py
```

### Project Structure
```
tock/
├── tock.py              # Main clock application
├── test_display.py      # Display logic tests
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use and modify for your projects.

## Credits

Built with Python and `curses` - keeping it simple, fast, and reliable.

---

<div align="center">

Made with ❤️ for terminal enthusiasts

[⬆ Back to top](#tock)

</div>
