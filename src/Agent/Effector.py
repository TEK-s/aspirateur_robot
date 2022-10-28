from src.Agent.Actions import Actions


class Effector:

    def __init__(self, environment):
        self.environment = environment

    def execute(self, action: Actions) -> None:
        if action is Actions.MOVE_UP:
            self.move_up()
        if action is Actions.MOVE_DOWN:
            self.move_down()
        if action is Actions.MOVE_LEFT:
            self.move_left()
        if action is Actions.MOVE_RIGHT:
            self.move_right()
        if action is Actions.VACUUM:
            self.vacuum()
        if action is Actions.COLLECT:
            self.collect()

    def move_up(self) -> None:
        if self.environment.agent_position[1] > 0:
            self.environment.agent_position[1] -= 1

    def move_down(self) -> None:
        if self.environment.agent_position[1] < self.environment.get_size() - 1:
            self.environment.agent_position[1] += 1

    def move_left(self) -> None:
        if self.environment.agent_position[0] > 0:
            self.environment.agent_position[0] -= 1

    def move_right(self) -> None:
        if self.environment.agent_position[0] < self.environment.get_size() - 1:
            self.environment.agent_position[0] += 1

    def vacuum(self) -> None:
        self.environment.vacuum()

    def collect(self) -> None:
        self.environment.collect()
