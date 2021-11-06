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


class RenderMap:
    '''Render function for screen windows'''
    def __init__(self, screen):
        self.screen = screen
        self.windows = []

    def add_window(self, window):
      self.windows.push((window.name, window))

    def replace_window(self, window):
      index = list(filter(lambda name:window.name in name, self.windows)).index
      self.windows.pop(index)
      if window is not None:
        self.windows.push((window.name, window))

    def render(self):
        self.screen.erase()
        self.screen.refresh()
        for window in self.windows:
          window.win.refresh()


def main(screen: curses.window):
    # screen = curses.initscr()

    # my__window = curses.newwin(10, 10)
    # my__window.addstr(0, 0, "G'day mate")
    # my__window.refresh()
    render_map = RenderMap(screen)

    win1 = generate_map(5, 5, 0, 0)

    win1.refresh()

    win2 = generate_map(8, 5, 5, 5)
    win2.refresh()
    # curses.napms(2000)

    render_map.add_window('win1', win1)
    render_map.add_window('win2', win2)

    for i in range(0, 15):
        y, x = win1.getbegyx()
        # screen.erase()
        # screen.refresh()
        # win1.mvwin(i, i)
        # win2.refresh()
        # win1.refresh()
        render_map.replace_window('win1', win2.mvwin(i, i))
        render_map.render()
        curses.napms(500)

    curses.napms(4000)


curses.wrapper(main)
