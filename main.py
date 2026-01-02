import os, subprocess, curses

def run(p):
    if os.name == "nt":
        os.startfile(p)
    else:
        subprocess.call(["xdg-open", p])

def safe_add(stdscr, y, x, text, attr=0):
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h or x < 0 or x >= w:
        return
    stdscr.addnstr(y, x, text, w - x - 1, attr)

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)

    idx = 0
    cwd = os.getcwd()

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        items = os.listdir(cwd)

        safe_add(stdscr, 0, 2, " FILE MANAGER ", curses.color_pair(1))
        safe_add(stdscr, 1, 0, "─" * (w-1), curses.color_pair(1))

        for i, it in enumerate(items):
            y = i + 2
            if y >= h - 2:
                break

            path = os.path.join(cwd, it)
            icon = "[D]" if os.path.isdir(path) else "[F]"
            line = f"{icon} {it}"

            if i == idx:
                safe_add(stdscr, y, 2, line, curses.color_pair(2))
            else:
                color = 3 if os.path.isdir(path) else 4
                safe_add(stdscr, y, 2, line, curses.color_pair(color))

        safe_add(stdscr, h-2, 0, "─" * (w-1), curses.color_pair(1))
        safe_add(stdscr, h-1, 2, f"DIR: {cwd}", curses.color_pair(1))

        k = stdscr.getch()

        if k in (ord("q"), ord("Q")):
            break
        elif k == curses.KEY_UP and idx > 0:
            idx -= 1
        elif k == curses.KEY_DOWN and idx < len(items) - 1:
            idx += 1
        elif k in (10, 13):
            p = os.path.join(cwd, items[idx])
            if os.path.isdir(p):
                cwd = p
                os.chdir(cwd)
                idx = 0
            else:
                run(p)
        elif k in (curses.KEY_BACKSPACE, 127, 8):
            parent = os.path.dirname(cwd)
            if parent:
                cwd = parent
                os.chdir(cwd)
                idx = 0

curses.wrapper(main)

# v3