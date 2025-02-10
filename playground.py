import curses
import time

def bounce_ball(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    
    stdscr.timeout(50)  # Control speed of animation



    height, width = stdscr.getmaxyx()
    ball = "O"
    x, y = width // 2, height // 2  # Start at center
    dx, dy = 1, 1  # Initial movement direction

    while True:
        stdscr.clear()
        stdscr.addch(y, x, ball)
        stdscr.refresh()

        x += dx
        y += dy

        if x <= 0 or x >= width - 1:
            dx = -dx  # Reverse horizontal direction
        if y <= 0 or y >= height - 1:
            dy = -dy  # Reverse vertical direction

        time.sleep(0.05)  # Delay to control speed

        key = stdscr.getch()
        if key == ord("q"):
            break  # Exit loop on 'q' press


if __name__ == "__main__":
    curses.wrapper(bounce_ball)
