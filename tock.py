#!/usr/bin/env python3
"""
Tock - A modern TUI clock application
"""

import curses
import time
from datetime import datetime
from typing import List, Tuple


class TockClock:
    """Main clock application with multiple display styles"""

    def __init__(self):
        self.stdscr = None
        self.current_style = 0
        self.styles = ['digital', 'simple', 'binary', 'words']
        self.show_footer = True
        self.running = True

        # ASCII art digits for large digital display
        self.digits = {
            '0': [
                ' ████ ',
                '█    █',
                '█    █',
                '█    █',
                '█    █',
                ' ████ '
            ],
            '1': [
                '  █   ',
                ' ██   ',
                '  █   ',
                '  █   ',
                '  █   ',
                ' ████ '
            ],
            '2': [
                ' ████ ',
                '█    █',
                '     █',
                '    █ ',
                '   █  ',
                ' █████'
            ],
            '3': [
                ' ████ ',
                '     █',
                '  ███ ',
                '     █',
                '     █',
                ' ████ '
            ],
            '4': [
                '█     ',
                '█  █  ',
                '█████ ',
                '    █ ',
                '    █ ',
                '    █ '
            ],
            '5': [
                ' █████',
                '█     ',
                '█████ ',
                '     █',
                '     █',
                ' ████ '
            ],
            '6': [
                ' ████ ',
                '█     ',
                '█████ ',
                '█    █',
                '█    █',
                ' ████ '
            ],
            '7': [
                ' █████',
                '     █',
                '    █ ',
                '   █  ',
                '  █   ',
                '  █   '
            ],
            '8': [
                ' ████ ',
                '█    █',
                ' ████ ',
                '█    █',
                '█    █',
                ' ████ '
            ],
            '9': [
                ' ████ ',
                '█    █',
                ' █████',
                '     █',
                '     █',
                ' ████ '
            ],
            ':': [
                '      ',
                '  ██  ',
                '  ██  ',
                '  ██  ',
                '  ██  ',
                '      '
            ]
        }

    def get_current_time(self) -> Tuple[int, int, int]:
        """Get current time as hours, minutes, seconds"""
        now = datetime.now()
        return now.hour, now.minute, now.second

    def center_text(self, text: str, max_width: int) -> str:
        """Center text within max_width"""
        return text.center(max_width)

    def draw_digital_clock(self, h: int, m: int, s: int) -> List[str]:
        """Generate large digital clock display"""
        time_str = f"{h:02d}:{m:02d}:{s:02d}"
        lines = ['' for _ in range(6)]

        for char in time_str:
            char_lines = self.digits.get(char, self.digits['0'])
            for i, line in enumerate(char_lines):
                lines[i] += line + '  '

        return lines

    def draw_simple_clock(self, h: int, m: int, s: int) -> List[str]:
        """Generate simple 24h centered text display"""
        time_str = f"{h:02d}:{m:02d}:{s:02d}"
        return [time_str]

    def draw_binary_clock(self, h: int, m: int, s: int) -> List[str]:
        """Generate binary clock with dot grid"""
        hours = h % 24
        minutes = m
        seconds = s

        lines = []
        labels = ['H ', 'M ', 'S ']

        for value, label in zip([hours, minutes, seconds], labels):
            # Get binary representation (6 bits for hours, 6 for minutes, 6 for seconds)
            bits = format(value, '06b')
            line = label
            for bit in bits:
                if bit == '1':
                    line += '● '
                else:
                    line += '○ '
            lines.append(line)
            lines.append('  ' + '  '.join(['6','5','4','3','2','1']))
            lines.append('')

        return lines[:-1]  # Remove trailing empty line

    def draw_words_clock(self, h: int, m: int, s: int) -> List[str]:
        """Generate minimalist words clock display"""
        hours_word = self._number_to_words(h % 12 or 12)
        minutes_word = self._minutes_to_words(m)

        if m == 0:
            return [f"{hours_word} O'CLOCK"]
        else:
            return [f"{hours_word} {minutes_word}"]

    def _number_to_words(self, n: int) -> str:
        """Convert number 1-12 to words"""
        words = {
            1: 'ONE', 2: 'TWO', 3: 'THREE', 4: 'FOUR',
            5: 'FIVE', 6: 'SIX', 7: 'SEVEN', 8: 'EIGHT',
            9: 'NINE', 10: 'TEN', 11: 'ELEVEN', 12: 'TWELVE'
        }
        return words.get(n, str(n))

    def _minutes_to_words(self, m: int) -> str:
        """Convert minutes to words"""
        if m == 1:
            return 'ONE'
        elif m == 15:
            return 'FIFTEEN'
        elif m == 30:
            return 'THIRTY'
        elif m == 45:
            return 'FORTY-FIVE'
        elif m < 30:
            return self._number_to_words(m)
        else:
            ones = self._number_to_words(m - 40)
            return f"FORTY-{ones}"

    def get_clock_display(self) -> List[str]:
        """Get the current clock display based on style"""
        h, m, s = self.get_current_time()

        style = self.styles[self.current_style]

        if style == 'digital':
            return self.draw_digital_clock(h, m, s)
        elif style == 'simple':
            return self.draw_simple_clock(h, m, s)
        elif style == 'binary':
            return self.draw_binary_clock(h, m, s)
        elif style == 'words':
            return self.draw_words_clock(h, m, s)
        else:
            return self.draw_simple_clock(h, m, s)

    def draw_centered(self, screen, text_lines: List[str]):
        """Draw text centered on screen"""
        height, width = screen.getmaxyx()

        start_y = (height - len(text_lines)) // 2

        for i, line in enumerate(text_lines):
            x = (width - len(line)) // 2
            try:
                screen.addstr(start_y + i, x, line)
            except curses.error:
                pass  # Handle edge case where text doesn't fit

    def draw_footer(self, screen):
        """Draw the help footer at bottom"""
        if not self.show_footer:
            return

        height, width = screen.getmaxyx()
        footer_text = "H - hide  Arrow - change style"
        x = (width - len(footer_text)) // 2
        try:
            screen.addstr(height - 2, x, footer_text)
        except curses.error:
            pass

    def handle_input(self):
        """Handle keyboard input"""
        key = self.stdscr.getch()

        if key == curses.KEY_LEFT:
            self.current_style = (self.current_style - 1) % len(self.styles)
        elif key == curses.KEY_RIGHT:
            self.current_style = (self.current_style + 1) % len(self.styles)
        elif key == ord('h') or key == ord('H'):
            self.show_footer = not self.show_footer
        elif key == ord('q') or key == ord('Q'):
            self.running = False

    def run(self):
        """Main run loop"""
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.nodelay(True)  # Non-blocking input
        self.stdscr.keypad(True)

        try:
            while self.running:
                self.stdscr.clear()

                # Draw the clock
                display_lines = self.get_clock_display()
                self.draw_centered(self.stdscr, display_lines)

                # Draw footer
                self.draw_footer(self.stdscr)

                # Refresh display
                self.stdscr.refresh()

                # Handle input with timeout
                curses.halfdelay(10)  # Wait up to 1 second for input
                self.handle_input()

                # Small delay to ensure exactly 1 second updates
                time.sleep(0.1)

        finally:
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()


def main():
    """Entry point"""
    clock = TockClock()
    clock.run()


if __name__ == '__main__':
    main()
