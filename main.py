import curses
# from curses import newwin
# from curses import window


def generate_room(width: int = 5, height: int = 5,
                  pos_y: int = 0, pos_x: int = 0, name=None):
    # Need extra space for width due to cursor moving past extra
    # character when adding string
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
    dungeon = []
    for i in range(3):
        dungeon.push(generate_room(pos_x=i*10))
    return dungeon


class Window:

    def __init__(self, name: str, layout: curses.window) -> None:
        self._name = name
        self._layout = layout
        return None

    @property
    def name(self) -> str:
        return self._name

    @property
    def layout(self) -> curses.window:
        return self._layout


class RenderMap:
    '''Render function for screen windows'''

    def __init__(self, screen):
        self.screen = screen
        self.windows = []

    def add_window(self, window: Window):
        self.windows.append(window)

    def replace_window(self, window: Window):
        # index =
        # index = list(
        #     filter(lambda name: window.name in name, self.windows)).index
        self.windows.pop(self.windows.index(window))
        if window is not None:
            self.windows.append(window)

    def render(self):
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

    win1 = generate_room(5, 5, 0, 0)

    # win1.refresh()

    win2 = generate_room(8, 5, 5, 5)
    # win2.refresh()
    # curses.napms(2000)

    render_map.add_window(win1)
    render_map.add_window(win2)
    for room in generate_dungeon():
        render_map.add_window(room)

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
    render_map.render()
    curses.napms(4000)


curses.wrapper(main)
