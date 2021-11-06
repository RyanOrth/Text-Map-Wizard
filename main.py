import curses
# from curses import newwin
# from curses import window


def generate_room(width, height, pos_y, pos_x, name = None):
    # Need extra space for width due to cursor moving past extra character when adding string
    map_window = curses.newwin(height, width + 1, pos_y, pos_x)
    map_window.box()
    for i in range(1, height - 1):
        for j in range(1, width):
            map_window.addstr(i, j, '*')
    return Window(name, map_window)


def generate_dungeon():
    '''
    Makes a template dungeon
    '''
    for i in range(3):
        generate_room(pos_x=i*10).refresh()


class Window:

    def __init__(self, name: str, layout: curses.window) -> None:
        self._name = name
        self._layout = layout

        borders = []
        layout_height, layout_width = layout.getmaxyx()
        for i in range(0, layout_width):
          borders.append((0, i, layout.getch(0, i)))
        for j in range(1, layout_height):
          borders.append((j, layout_width, layout.getch(j, layout_width)))
        for i in range(layout_width - 1, 0):
          borders.append((layout_height, i, layout.getch(layout_height, i)))
        for j in range(layout_height - 1, 1):
          borders.append((j, 0, layout.getch(j, 0)))
        self._borders = borders
        return None

    @property
    def name(self):
        return self._name

    @property
    def layout(self):
        return self._layout

    @property
    def borders(self):
        return self._borders


class RenderMap:
    '''Contains windows to be rendered'''

    def __init__(self, screen):
        self.screen = screen
        self.windows = []

    def add_window(self, window: Window):
        '''Adding a new window to the windows list'''
        self.windows.append(window)

    def replace_window(self, window: Window):
        '''Update or remove a window in the windows list'''
        self.windows.pop(self.windows.index(window))
        if window is not None:
            self.windows.append(window)

    def render(self):
        '''Render screen function'''
        self.screen.erase()
        self.screen.refresh()
        for window in self.windows:
            window.layout.refresh()


def main(screen: curses.window):
    # screen = curses.initscr()

    # my__window = curses.newwin(10, 10)
    # my__window.addstr(0, 0, "G'day mate")
    # my__window.refresh()
    render_map = RenderMap(screen)

    win1 = generate_room(5, 5, 0, 0, 'win1')

    # win1.refresh()

    win2 = generate_room(8, 5, 5, 5, 'win2')
    # win2.refresh()
    # curses.napms(2000)

    render_map.add_window(win1)
    render_map.add_window(win2)
    render_map.render()
    # for i in range(0, 15):
    #     y, x = win1.layout.getbegyx()
    #     # screen.erase()
    #     # screen.refresh()
    #     # win1.mvwin(i, i)
    #     # win2.refresh()
    #     # win1.refresh()
    #     win1.layout.mvwin(i, i)
    #     render_map.replace_window(win1)
    #     render_map.render()
    #     curses.napms(500)

    curses.napms(4000)

curses.wrapper(main)
