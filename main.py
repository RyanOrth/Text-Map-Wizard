import curses
from enum import Enum
# from curses import newwin
# from curses import window


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def generate_room(width: int = 5, height: int = 5,
                  pos_y: int = 0, pos_x: int = 0, name=None):
    # Need extra space for width due to cursor moving past extra
    # character when adding string
    map_window = curses.newwin(height, width + 1, pos_y, pos_x)
    map_window.box()
    for i in range(1, height - 1):
        for j in range(1, width):
            map_window.addstr(i, j, '*')
    return Window(name, map_window, [SpecialEdgeCharacter(5, 0, '*'), SpecialEdgeCharacter(height, 5, '*')])


def generate_dungeon():
    '''
    Makes a template dungeon
    '''
    dungeon = []
    for i in range(4):
        dungeon.append(Room(name=None, pos_x=i*10, open_sides=[SpecialEdgeCharacter('door1', 3, 0, ' '), SpecialEdgeCharacter('door2', 0, 3, ' ')]))
    return dungeon

class SpecialEdgeCharacter:
  def __init__(self, name:str, pos_y: int, pos_x: int, character: str):
    self._name = name
    self._pos_y = pos_y
    self._pos_x = pos_x
    self._character = character

  @property
  def name(self) -> str:
    return self._name

  @property
  def pos_y(self) -> int:
    return self._pos_y

  @property
  def pos_x(self) -> int:
    return self._pos_x

  @property
  def character(self) -> str:
    return self._character

class Window:

    def __init__(self, name: str, layout: curses.window, special_edge_characters = None) -> None:
        self._name = name
        self._layout = layout

        if special_edge_characters is not None:
          for special_edge_character in special_edge_characters:
            layout.addstr(special_edge_character.pos_y, special_edge_character.pos_x, special_edge_character.character)
          self._special_edge_characters = special_edge_characters
        else:
          self._special_edges_characters = None

        return None

    @property
    def name(self) -> str:
        return self._name

    @property
    def layout(self) -> curses.window:
        return self._layout

    @property
    def special_edges(self):
        return self._special_edge_characters
        

class Room(Window):
    def __init__(self, name: str = None, width: int = 5, height: int = 5,
                 pos_y: int = 0, pos_x: int = 0, open_sides: list = []) -> None:
        layout = curses.newwin(height, width + 1, pos_y, pos_x)
        for i in range(0, height-1):
            for j in range(0, width):
                layout.addstr(i, j, '*')
        layout.box()
        if open_sides is not None:
          for special_edge_character in open_sides:
            layout.addstr(special_edge_character.pos_y, special_edge_character.pos_x, special_edge_character.character)
        super().__init__(name, layout)


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
    curses.curs_set(0)
    # screen = curses.initscr()

    # my__window = curses.newwin(10, 10)
    # my__window.addstr(0, 0, "G'day mate")
    # my__window.refresh()
    render_map = RenderMap(screen)
    # win1 = generate_room(5, 5, 0, 0, 'win1')

    # # win1.refresh()

    # win2 = generate_room(8, 5, 5, 5, 'win2')
    # # win2.refresh()
    # # curses.napms(2000)

    # render_map.add_window(win1)
    # render_map.add_window(win2)
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
    curses.curs_set(1)


curses.wrapper(main)
