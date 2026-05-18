"""Terminal-based Snake game using curses."""

import curses
import random
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

    # Food initialisation
    def spawn_food() -> tuple[int, int]:
        """Place food at a random grid cell not occupied by the snake."""
        occupied = set(snake)
        empty = [
            (r, c)
            for r in range(1, GRID_HEIGHT + 1)
            for c in range(1, GRID_WIDTH + 1)
            if (r, c) not in occupied
        ]
        return random.choice(empty)

    food = spawn_food()
    score = 0

    # Game loop
    game_over = False
    while True:
        # Check for quit and handle direction changes
        key = win.getch()
        if key == ord("q"):
            break
        if key == curses.KEY_UP and direction != DIR_DOWN:
            direction = DIR_UP
        elif key == curses.KEY_DOWN and direction != DIR_UP:
            direction = DIR_DOWN
        elif key == curses.KEY_LEFT and direction != DIR_RIGHT:
            direction = DIR_LEFT
        elif key == curses.KEY_RIGHT and direction != DIR_LEFT:
            direction = DIR_RIGHT

        # Move snake: compute new head position
        head_r, head_c = snake[0]
        dr, dc = direction
        new_head = (head_r + dr, head_c + dc)

        # Collision detection
        # Wall collision: head outside the grid area (rows/cols 1..GRID_HEIGHT/WIDTH)
        if not (1 <= new_head[0] <= GRID_HEIGHT and 1 <= new_head[1] <= GRID_WIDTH):
            game_over = True
        # Self-collision: head hits body segments that won't be removed
        # Exclude tail from check since it will be popped on normal moves
        elif new_head in snake[:-1]:
            game_over = True
        else:
            snake.insert(0, new_head)

        if game_over:
            break

        # Check if snake ate the food
        if new_head == food:
            score += 10
            food = spawn_food()  # New food immediately
            # Don't pop tail — snake grows by 1
        else:
            tail = snake.pop()
            # Clear old tail position
            win.addch(tail[0], tail[1], " ")

        # Render food
        win.addch(food[0], food[1], "$")

        # Render snake body (cells that were the head and body)
        for r, c in snake[1:]:
            win.addch(r, c, "o")
        # Render head
        win.addch(snake[0][0], snake[0][1], "O")

        # Redraw border (in case of corruption)
        win.border(0)
        # Display score at top-left of terminal
        stdscr.addstr(0, 0, f"Score: {score}".ljust(max_x))
        win.refresh()

        curses.napms(TICK_MS)  # Tick rate

    # Game over screen
    if game_over:
        # Switch to blocking input for the message display
        win.nodelay(False)
        msg = f"Game Over! Final Score: {score}"
        msg_row = GRID_HEIGHT // 2 + 1
        msg_col = (GRID_WIDTH - len(msg)) // 2 + 1
        win.addstr(msg_row, msg_col, msg)
        win.refresh()
        # Wait for any key to exit
        win.getch()


if __name__ == "__main__":
    curses.wrapper(main)
