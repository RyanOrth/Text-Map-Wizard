import curses
from enum import Enum
import random
# from curses import newwin
# from curses import window


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 8


def generate_room(width: int = 5, height: int = 5,
                  pos_y: int = 0, pos_x: int = 0, name=None):
    # Need extra space for width due to cursor moving past extra
    # character when adding string
    map_window = curses.newwin(height, width + 1, pos_y, pos_x)
    map_window.box()
    for i in range(1, height - 1):
        for j in range(1, width):
            map_window.addstr(i, j, '*')
    return Window(name, map_window, [SpecialEdgeCharacter('ryan is a bad person', 5, 0, '*'), SpecialEdgeCharacter('ryan has many erro',  height, 5, '*')])


def generate_dungeon():
    '''
    Makes a template dungeon
    '''
    dungeon = []
    for i in range(4):
        dungeon.append(Room(name=None, pos_x=i*10, open_sides=[SpecialEdgeCharacter(
            'door1', 3, 0, ' '), SpecialEdgeCharacter('door2', 0, 3, ' ')]))
    return dungeon


class SpecialEdgeCharacter:
    def __init__(self, name: str, pos_y: int, pos_x: int, character: str):
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

    def __init__(self, name: str, layout: curses.window, special_edge_characters=None) -> None:
        self._name = name
        self._layout = layout

        if special_edge_characters is not None:
            for special_edge_character in special_edge_characters:
                layout.addstr(special_edge_character.pos_y,
                              special_edge_character.pos_x, special_edge_character.character)
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
        self._width = width
        self._height = height
        self._pos_x = pos_x
        self._pos_y = pos_y
        layout = curses.newwin(height, width + 1, pos_y, pos_x)
        for i in range(0, height-1):
            for j in range(0, width):
                layout.addstr(i, j, '*')
        layout.box()
        if open_sides is not None:
            for special_edge_character in open_sides:
                layout.addstr(special_edge_character.pos_y,
                              special_edge_character.pos_x, special_edge_character.character)
        super().__init__(name, layout)

    @property
    def pos_x(self):
        return self._pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width


def check_for_overlap(room: Window, rooms: list):
    """Return false if the room overlaps any other room."""
    for current_room in rooms:
        xmin1 = room.pos_x
        xmax1 = room.pos_x + room.width
        xmin2 = current_room.pos_x
        xmax2 = current_room.pos_x + current_room.width
        ymin1 = room.pos_y
        ymax1 = room.pos_y + room.height
        ymin2 = current_room.pos_y
        ymax2 = current_room.pos_y + current_room.height
        if (xmin1 <= xmax2 and xmax1 >= xmin2) and \
           (ymin1 <= ymax2 and ymax1 >= ymin2):
            return True
    return False


class Passageway(Window):
    def __init__(self, name: str, layout: curses.window) -> None:
        super().__init__(name, layout)


class OccuppiedRegion:
    def __init__(self, name: str, min_y: int, min_x: int, max_y: int, max_x: int):
        self._name = name
        self._min_y = min_y
        self._min_x = min_x
        self._max_y = max_y
        self._max_x = max_x

    @property
    def name(self):
        return self.name

    @property
    def min_y(self):
        return self._min_y

    @property
    def min_x(self):
        return self._min_x

    @property
    def max_y(self):
        return self._max_y

    @property
    def max_x(self):
        return self._max_x


class RenderMap:
    '''Contains windows to be rendered'''

    def __init__(self, screen):
        self.screen = screen
        self._windows = []
        self._window_positions = []

    def _window_is_not_overlapping(self, candidate_window: Room):
        candidate_region = OccuppiedRegion(candidate_window.name, candidate_window.pos_y,
                                           candidate_window.pos_x,
                                           candidate_window.pos_y + candidate_window.height,
                                           candidate_window.pos_x + candidate_window.width)

        for window_position in self._window_positions:
            if(window_position.min_x <= candidate_region.min_x
               <= window_position.max_x):
                if(window_position.min_y <= candidate_region.min_y
                   <= window_position.max_y):
                    return False
                elif(window_position.min_y <= candidate_region.max_y
                     <= window_position.max_y):
                    return False
            elif (window_position.min_x <= candidate_region.max_x
                  <= window_position.max_x):
                if(window_position.min_y <= candidate_region.min_y
                   <= window_position.max_y):
                    return False
                elif(window_position.min_y <= candidate_region.max_y
                     <= window_position.max_y):
                    return False
        return True

    def add_window(self, window: Room):
        '''Adding a new window to the windows list'''
        if self._window_is_not_overlapping(window):
            self._windows.append(window)
            self._window_positions.append(OccuppiedRegion(
                window.name, window.pos_y, window.pos_x,
                window.pos_y + window.height, window.pos_x + window.width))
            return True
        return False

    def replace_window(self, window: Room):
        '''Update or remove a window in the windows list'''
        self._windows.pop(self._windows.index(window))
        # list(filter(lambda x:11 in x, Input))
        if window is not None:
            self._windows.append(window)

    def render(self):
        '''Render screen function'''
        self.screen.erase()
        self.screen.refresh()
        data = ''
        for window in self._windows:
            window.layout.refresh()

    @property
    def windows(self) -> list:
        return self._windows


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
    count = 2

    # while count > 0:
    #     canRoom = Room(name=None, width=random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE),
    #                    height=random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE),
    #                    pos_y=random.randrange(0, 2*MAX_ROOM_SIZE+1), pos_x=random.randrange(0, 2*MAX_ROOM_SIZE+1))
    #     if(render_map.add_window(canRoom)):
    #         count -= 1
    for i in range(4):
        for j in range(4):
            render_map.add_window(Room(None, 5, 5, i*10, j*10))

    # for room in generate_dungeon():
    #   render_map.add_window(room)

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
    curses.napms(5000)
    curses.curs_set(1)


curses.wrapper(main)
