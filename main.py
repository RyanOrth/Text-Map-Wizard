import curses
# from curses import newwin
from curses import window


def generate_map(map_width, map_height, pos_y, pos_x):
    # Need extra space for width due to cursor moving past extra character when adding string
    map_window = curses.newwin(map_height, map_width + 1, pos_y, pos_x)
    map_window.box()
    for i in range(1, map_height - 1):
        for j in range(1, map_width):
            map_window.addstr(i, j, '*')
    return map_window


class render_map:
    '''Render function for screen windows'''
    def __init__():
        screen
        window = []

    def render():
        screen.erase()


def main(screen: curses.window):
    # screen = curses.initscr()

    # my__window = curses.newwin(10, 10)
    # my__window.addstr(0, 0, "G'day mate")
    # my__window.refresh()
    my__window = generate_map(5, 5, 0, 0)

    my__window.refresh()

    win2 = generate_map(8, 5, 5, 5)
    win2.refresh()
    # curses.napms(2000)

    for i in range(0, 15):
        y, x = my__window.getbegyx()
        screen.erase()
        screen.refresh()
        my__window.mvwin(i, i)
        win2.refresh()
        my__window.refresh()
        curses.napms(500)

    curses.napms(4000)


curses.wrapper(main)
