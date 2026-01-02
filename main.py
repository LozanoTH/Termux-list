import os, subprocess, curses

def run(p):
    if os.name == "nt":
        os.startfile(p)
    else:
        subprocess.call(["xdg-open", p])

def main(stdscr):
    curses.curs_set(0)
    idx = 0
    cwd = os.getcwd()

    while True:
        stdscr.clear()
        items = os.listdir(cwd)
        stdscr.addstr(0, 0, f"DIR: {cwd}")
        for i, it in enumerate(items):
            if i == idx:
                stdscr.addstr(i+2, 0, f"> {it}", curses.A_REVERSE)
            else:
                stdscr.addstr(i+2, 0, f"  {it}")
        k = stdscr.getch()

        if k == ord("q"):
            break
        if k == curses.KEY_UP and idx > 0:
            idx -= 1
        if k == curses.KEY_DOWN and idx < len(items)-1:
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
