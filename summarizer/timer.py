import timeit
from datetime import datetime


class Timer:
    def __init__(self, name):
        self.name = name
        self.start_time = timeit.default_timer()

    def start(self):
        self.start_time = timeit.default_timer()
        print('Stating {} timer @ {}'.format(self.name, datetime.now().time()))

    def stop(self):
        stop_time = timeit.default_timer()
        diff = (stop_time - self.start_time) / 60
        print('{} Time: {}'.format(self.name, diff))
        print()
