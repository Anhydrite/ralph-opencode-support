"""Terminal-based Snake game using curses."""

import curses
from typing import Any


GRID_HEIGHT = 20
GRID_WIDTH = 20
TICK_MS = 150

# Direction vectors: (row_delta, col_delta)
DIR_RIGHT = (0, 1)
DIR_DOWN = (1, 0)
DIR_LEFT = (0, -1)
DIR_UP = (-1, 0)


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

    # Initialise snake: list of (row, col) head-to-tail in window coords
    center_row = GRID_HEIGHT // 2 + 1
    center_col = GRID_WIDTH // 2 + 1
    snake = [
        (center_row, center_col),       # head
        (center_row, center_col - 1),   # body
        (center_row, center_col - 2),   # tail
    ]
    direction = DIR_RIGHT

    # Game loop
    while True:
        # Check for quit
        key = win.getch()
        if key == ord("q"):
            break

        # Move snake: compute new head position
        head_r, head_c = snake[0]
        dr, dc = direction
        new_head = (head_r + dr, head_c + dc)
        snake.insert(0, new_head)
        tail = snake.pop()

        # Clear old tail position
        win.addch(tail[0], tail[1], " ")

        # Render snake body (cells that were the head and body)
        for r, c in snake[1:]:
            win.addch(r, c, "o")
        # Render head
        win.addch(snake[0][0], snake[0][1], "O")

        # Redraw border (in case of corruption)
        win.border(0)
        win.refresh()

        curses.napms(TICK_MS)  # Tick rate


if __name__ == "__main__":
    curses.wrapper(main)
