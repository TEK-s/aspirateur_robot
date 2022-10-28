import threading
import time

from src.Environment.Mansion import Mansion
from src.Environment.View import View

from src.Agent.Agent import Robot


def main() -> None:
    run_event = threading.Event()
    run_event.set()

    environment = Mansion(5, run_event)
    environment.start()

    agent = Robot(environment, run_event)
    agent.start()

    view = View(environment, run_event)
    view.start()

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        run_event.clear()

        environment.join()
        agent.join()
        view.join()

        print('Stopped.')


if __name__ == '__main__':
    main()
