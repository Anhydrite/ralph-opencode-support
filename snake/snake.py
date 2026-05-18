"""Terminal-based Snake game using curses."""

import curses
from typing import Any


GRID_HEIGHT = 20
GRID_WIDTH = 20


def main(stdscr: Any) -> None:
    """Initialize and run the snake game."""
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    # Get terminal dimensions
    max_y, max_x = stdscr.getmaxyx()

    # Calculate window position to center the grid
    win_height = GRID_HEIGHT + 2  # +2 for border
    win_width = GRID_WIDTH + 2   # +2 for border
    start_y = max(0, (max_y - win_height) // 2)
    start_x = max(0, (max_x - win_width) // 2)

    # Create the game window with a border
    win = curses.newwin(win_height, win_width, start_y, start_x)
    win.border(0)
    win.nodelay(True)  # Non-blocking input
    win.keypad(True)   # Enable arrow keys

    # Game loop
    while True:
        # Redraw border (in case of corruption)
        win.border(0)
        win.refresh()

        # Check for quit
        key = win.getch()
        if key == ord("q"):
            break

        curses.napms(150)  # Tick rate


if __name__ == "__main__":
    curses.wrapper(main)
