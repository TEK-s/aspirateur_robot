import random
import threading
import time

from src.Environment.Room import Room

DUST_RATE = 45
JEWEL_RATE = 15

DUST_POINT = 1
JEWEL_POINT = 1
FAIL_POINT = -1

SPAWN_DELAY = 1


class Mansion(threading.Thread):

    def __init__(self, size: int, run_event: threading.Event):
        threading.Thread.__init__(self)

        self.size = size
        self.run_event = run_event
        self.rooms = self.create_rooms()
        self.last_action = ''
        self.agent_position = [round(size / 2), round(size / 2)]
        self.collected = [0, 0, 0, 0]  # [dust, jewel, both, fail]

    def create_rooms(self) -> list[list[Room]]:
        return [[Room() for _ in range(self.size)] for _ in range(self.size)]

    def get_rooms(self) -> list[list[Room]]:
        return self.rooms

    def get_room(self, x: int, y: int) -> Room:
        return self.rooms[x][y]

    def get_size(self) -> int:
        return self.size

    def get_score(self) -> int:
        [dust, jewel, both, fail] = self.collected
        return dust * DUST_POINT + jewel * JEWEL_POINT + (both + fail) * FAIL_POINT

    def vacuum(self) -> None:
        room = self.get_room(self.agent_position[0], self.agent_position[1])

        if room.has_dust and room.has_jewel:
            self.collected[2] += 1
        elif room.has_jewel:
            self.collected[3] += 1
        elif room.has_dust:
            self.collected[0] += 1
        else:
            self.collected[3] += 1

        room.reset()

    def collect(self) -> None:
        room = self.get_room(self.agent_position[0], self.agent_position[1])

        if room.has_dust:
            self.collected[3] += 1
        elif room.has_jewel:
            self.collected[1] += 1
        else:
            self.collected[3] += 1

        room.reset()

    def update(self) -> None:
        if random.randint(0, 99) < DUST_RATE:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            self.rooms[x][y].add_dust()

        if random.randint(0, 99) < JEWEL_RATE:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            self.rooms[x][y].add_jewel()

    def run(self) -> None:
        while self.run_event.is_set():
            self.update()
            time.sleep(SPAWN_DELAY)
