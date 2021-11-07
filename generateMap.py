from window import Room, Window
from specialCharacters import SpecialEdgeCharacter
import random
from constants import MIN_ROOM_SIZE, MAX_ROOM_SIZE


class GenerateMap:
    def __init__(self, map_height: int, map_width: int):
        self._map_height = map_height
        self._map_width = map_width

    def generate_map(self):
        map = []
        for i in range(1, random.randrange(2, 6)):
            map.append(self._generate_room(i))
        return map

    def _generate_room(self, index: int):
        height = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        width = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        pos_y = random.randrange(0, self._map_height - height)
        pos_x = random.randrange(0, self._map_width - width)
        return Room(f'room{index}', height, width, pos_y, pos_x, self._generate_doors(height, width))

    def _generate_doors(self, room_height, room_width):
        doors = []
        num_doors_options = [1, 2, 3, 4]
        num_doors_list = random.choices(num_doors_options, weights=(60, 80, 20, 10))

        for i in range(0, num_doors_list[0]):
            pos_y, pos_x = self._generate_random_door_position(
                room_height, room_width)
            doors.append(SpecialEdgeCharacter(f'door{i}', pos_y, pos_x, '+'))

        return doors

    def _generate_random_door_position(self, room_height, room_width):
        pos_x = random.randrange(0, room_width)
        pos_y = None
        if(pos_x == 0 or pos_x == room_width):
            pos_y = random.randrange(0, room_height)
        else:
            pos_y = random.choice([0, room_height])
        return (pos_y, pos_x)
