import curses
import random
from enum import Enum

from renderMap import RenderMap
from specialCharacters import SpecialEdgeCharacter
from window import Room, Window


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
    return Window(name, map_window, [SpecialEdgeCharacter('ryan is a bad person', 5, 0, '*'),
                                     SpecialEdgeCharacter('ryan has many erro',  height, 5, '*')])


def generate_dungeon():
    '''
    Makes a template dungeon
    '''
    dungeon = []
    for i in range(4):
        dungeon.append(Room(name=None, pos_x=i*10, open_sides=[SpecialEdgeCharacter(
            'door1', 3, 0, ' '), SpecialEdgeCharacter('door2', 0, 3, ' ')]))
    return dungeon


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


def main(screen: curses.window):
    curses.curs_set(0)

    render_map = RenderMap(screen)

    # count = 2

    # while count > 0:
    #     canRoom = Room(name=None, width=random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE),
    #                    height=random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE),
    #                    pos_y=random.randrange(0, 2*MAX_ROOM_SIZE+1), pos_x=random.randrange(0, 2*MAX_ROOM_SIZE+1))
    #     if(render_map.add_window(canRoom)):
    #         count -= 1
    for i in range(4):
        for j in range(4):
            render_map.add_window(Room(None, 5, 5, i*10, j*10))

    render_map.render()
    curses.napms(5000)
    curses.curs_set(1)


curses.wrapper(main)
