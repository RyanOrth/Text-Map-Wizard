import curses
import random
from enum import Enum

from renderMap import RenderMap
from specialCharacters import SpecialEdgeCharacter
from window import PassageWay, Room, Window


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 8


def generate_dungeon() -> list:
    '''
    Makes a template dungeon
    '''
    dungeon = []
    for i in range(4):
        dungeon.append(Room(name=None, pos_x=i*10, open_sides=[SpecialEdgeCharacter(
            'door1', 3, 0, ' '), SpecialEdgeCharacter('door2', 0, 3, ' ')]))
    return dungeon


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
    for i in range(2):
        for j in range(2):
            render_map.add_room(Room(None, 5, 5, i*10, j*10))

    render_map.add_passageWay(PassageWay(None, 3, 5, 1, 5))

    render_map.render()
    curses.napms(5000)
    curses.curs_set(1)


curses.wrapper(main)
