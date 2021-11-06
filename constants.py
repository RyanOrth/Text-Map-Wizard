from enum import Enum

MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 8

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3