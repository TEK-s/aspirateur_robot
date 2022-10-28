import threading
import time
import os

REFRESH_DELAY = .1


class View(threading.Thread):

    def __init__(self, environment, run_event: threading.Event):
        threading.Thread.__init__(self)

        self.environment = environment
        self.run_event = run_event

    def print(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(' ╭─', end='')
        for _ in range(self.environment.get_size()):
            print('──', end='')
        print('╮')

        for y in range(self.environment.get_size()):
            print(' │ ', end='')

            for x in range(self.environment.get_size()):
                if self.environment.agent_position[0] is x and self.environment.agent_position[1] is y:
                    print("\033[95m{}\033[00m".format('# '), end='')
                else:
                    self.environment.get_room(x, y).print()
                    print(' ', end='')

            print('│', end='')

            [dust, jewel, both, fail] = self.environment.collected

            if y == 0:
                print(' \033[97m~\033[00m : Dust ({})'.format(dust), end='')
            if y == 1:
                print(' \033[96m¤\033[00m : Jewel ({})'.format(jewel), end='')
            if y == 2:
                print(' \033[91m%\033[00m : Dust & Jewel ({})'.format(both), end='')
            if y == 4:
                print(' Score: {0} \033[90m(fail: {1})\033[00m'.format(self.environment.get_score(), fail), end='')

            print()

        print(' ╰─', end='')
        for _ in range(self.environment.get_size()):
            print('──', end='')
        print('╯')

        print()
        print(' Action : {0}'.format(self.environment.last_action))
        print()

    def run(self) -> None:
        while self.run_event.is_set():
            self.print()
            time.sleep(REFRESH_DELAY)
