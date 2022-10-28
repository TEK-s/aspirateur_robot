from src.Environment.Room import Room


class Sensor:

    def __init__(self, environment):
        self.environment = environment

    def get_state(self) -> list[list[Room]]:
        return self.environment.get_rooms()
