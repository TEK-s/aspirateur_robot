import math
import threading
import time
import typing

from src.Environment.Room import Room

from src.Agent.Actions import Actions
from src.Agent.Sensor import Sensor
from src.Agent.Effector import Effector

MAX_STEPS = 10
UPDATE_DELAY = .5


class Robot(threading.Thread):
    beliefs: typing.Union[list[list[Room]], None]
    desires: typing.Union[list[list[bool]], None]

    def __init__(self, environment, run_event: threading.Event):
        threading.Thread.__init__(self)

        self.run_event = run_event
        self.environment = environment

        self.sensor = Sensor(environment)
        self.effector = Effector(environment)

        self.beliefs = None
        self.desires = None
        self.intentions = []

    def run_action(self, action: Actions) -> None:
        self.environment.last_action = action.value
        self.effector.execute(action)

    def search(self, start_x: int, start_y: int) -> typing.Union[list[int], None]:
        last = math.inf
        best = None
        size = self.environment.get_size()

        for x in range(size):
            for y in range(size):
                if self.beliefs[x][y].has_thing() and not self.desires[x][y]:
                    distance = abs(start_x - x) + abs(start_y - y)

                    if distance < last:
                        best = [x, y]
                        last = distance

        return best

    def determine_actions(self, from_x: int, from_y: int, to_x: int, to_y: int) -> None:
        while from_x != to_x:
            if from_x < to_x:
                from_x += 1
                self.intentions.append(Actions.MOVE_RIGHT)
            if from_x > to_x:
                from_x -= 1
                self.intentions.append(Actions.MOVE_LEFT)

        while from_y != to_y:
            if from_y < to_y:
                from_y += 1
                self.intentions.append(Actions.MOVE_DOWN)
            if from_y > to_y:
                from_y -= 1
                self.intentions.append(Actions.MOVE_UP)

        if self.beliefs[to_x][to_y].has_dust:
            self.intentions.append(Actions.VACUUM)
            return None

        if self.beliefs[to_x][to_y].has_jewel:
            self.intentions.append(Actions.COLLECT)

    def scan(self) -> None:
        self.beliefs = self.sensor.get_state()
        self.desires = [[False for _ in range(self.environment.get_size())] for _ in range(self.environment.get_size())]

        from_pos = self.environment.agent_position

        while len(self.intentions) < MAX_STEPS:
            to_pos = self.search(from_pos[0], from_pos[1])

            if to_pos is None:
                break

            self.determine_actions(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
            self.desires[to_pos[0]][to_pos[1]] = True

            from_pos = to_pos

    def update(self) -> None:
        if len(self.intentions) > 0:
            self.run_action(self.intentions.pop(0))
        else:
            self.environment.last_action = 'scan'
            self.scan()

    def run(self) -> None:
        while self.run_event.is_set():
            self.update()
            time.sleep(UPDATE_DELAY)
