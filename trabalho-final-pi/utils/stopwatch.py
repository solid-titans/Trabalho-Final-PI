import time as Timer

class Stopwatch():

    def __init__(self) -> None:
        self.__start = 0
        self.__end   = 0

    def start(self):
        self.__start = Timer.time()

    def stop(self) -> str:
        self.__end = Timer.time()
        hours, rem = divmod(self.__end-self.__start, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)