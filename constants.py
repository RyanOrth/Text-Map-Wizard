from enum import Enum

MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 8
MAX_ITERATIONS = 1000
MAX_ROOM_COUNT = 5

MAP_X = 20
MAP_Y = 20


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
