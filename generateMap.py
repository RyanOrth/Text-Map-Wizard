from window import Room, Window
from specialCharacters import SpecialEdgeCharacter
import random
from constants import MIN_ROOM_SIZE, MAX_ROOM_SIZE
from occupiedRegion import OccuppiedRegion

class GenerateMap:
    def __init__(self, map_height: int, map_width: int):
        self._map_height = map_height
        self._map_width = map_width
        self._map = []
        self._occupied_regions = []
        self._special_characters = {}

    def generate_map(self):
        for i in range(1, random.randrange(30, 40)):
            room = self._generate_room(i)
            if(self._window_is_not_overlapping(room)):
                self._map.append(room)
                self._occupied_regions.append(OccuppiedRegion(room))
        return self._map

    def _window_is_not_overlapping(self, candidate_window: Room) -> bool:
        candidate_region = OccuppiedRegion(candidate_window)

        for occupied_region in self._occupied_regions:
            if(candidate_region.min_x in range(occupied_region.min_x, occupied_region.max_x + 1)):
                if(candidate_region.min_y in range(occupied_region.min_y, occupied_region.min_y + 1)):
                    return False
                elif(candidate_region.max_y in range(occupied_region.min_y, occupied_region.max_y + 1)):
                    return False
            elif (candidate_region.max_x in range(occupied_region.min_x, occupied_region.max_x + 1)):
                if(candidate_region.min_y in range(occupied_region.min_y, occupied_region.min_y + 1)):
                    return False
                elif(candidate_region.max_y in range(occupied_region.min_y, occupied_region.max_y + 1)):
                    return False
        return True

    def _connect_passageways(self, rooms):
        pass

    def _generate_room(self, room_index: int):
        height = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        width = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        pos_y = random.randrange(0, self._map_height - height)
        pos_x = random.randrange(0, self._map_width - width)
        return Room(f'room{room_index}', height, width, pos_y, pos_x, self._generate_doors(room_index=room_index, room_height=height, room_width=width))

    def _generate_doors(self, room_index: int, room_height: int, room_width: int):
        doors = []
        num_doors_options = [1, 2, 3, 4]
        num_doors_list = random.choices(
            num_doors_options, weights=(60, 80, 20, 10))

        for i in range(0, num_doors_list[0]):
            pos_y, pos_x = self._generate_random_door_position(room_height, room_width)
            doors.append(SpecialEdgeCharacter(f'door{i}', pos_y, pos_x, '+'))
            self._special_characters.update({f'room{room_index}-door{i}': '+'})

        return doors

    def _generate_random_door_position(self, room_height, room_width):
        pos_x = random.randrange(0, room_width)
        pos_y = None
        if(pos_x == 0 or pos_x == room_width):
            pos_y = random.randrange(0, room_height)
        else:
            pos_y = random.choice([0, room_height - 1])
        return (pos_y, pos_x)
