import os, subprocess, curses

def run(p):
    if os.name == "nt":
        os.startfile(p)
    else:
        subprocess.call(["xdg-open", p])

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

        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(0, 2, " FILE MANAGER ")
        stdscr.addstr(1, 0, "─" * w)
        stdscr.attroff(curses.color_pair(1))

        for i, it in enumerate(items):
            icon = "📁" if os.path.isdir(os.path.join(cwd, it)) else "📄"
            y = i + 2
            if y >= h - 2:
                break
            if i == idx:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, 2, f"{icon} {it[:w-6]}")
                stdscr.attroff(curses.color_pair(2))
            else:
                color = 3 if icon == "📁" else 4
                stdscr.attron(curses.color_pair(color))
                stdscr.addstr(y, 2, f"{icon} {it[:w-6]}")
                stdscr.attroff(curses.color_pair(color))

        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(h-2, 0, "─" * w)
        stdscr.addstr(h-1, 2, f"DIR: {cwd[:w-6]}")
        stdscr.attroff(curses.color_pair(1))

        k = stdscr.getch()

        if k in (ord("q"), ord("Q")):
            break
        if k == curses.KEY_UP and idx > 0:
            idx -= 1
        if k == curses.KEY_DOWN and idx < len(items) - 1:
            idx += 1
        if k in (curses.KEY_ENTER, 10, 13):
            p = os.path.join(cwd, items[idx])
            if os.path.isdir(p):
                cwd = p
                os.chdir(cwd)
                idx = 0
            else:
                run(p)
        if k in (curses.KEY_BACKSPACE, 127):
            cwd = os.path.dirname(cwd)
            os.chdir(cwd)
            idx = 0

curses.wrapper(main)

# v2