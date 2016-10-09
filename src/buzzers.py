import fcntl
import os
from queue import Queue
from threading import Thread

def worker(buzzers):
    while True:
        buzzers.read()

class Buzzers:

    def decode(self, bits):
        mask = 1
        for i in range(0, 20):
            if bits & mask and not(self.old_bits & mask):
                self.queue.put({'buzzer': int(i / 5),
                                'button': i % 5})
            mask = mask << 1
        self.old_bits = bits

    def read(self):
        input = self.f.read(5)
        if input:
            bits = input[4] << 16 | input[3] << 8 | input[2]
            self.decode(bits)

    def leds(self, one, two, three, four):
        self.f.write(bytearray([0, 0,
                                255 if one else 0,
                                255 if two else 0,
                                255 if three else 0,
                                255 if four else 0]))

    def get_pressed(self):
        if self.queue.empty():
            return None
        else:
            return self.queue.get()

    def __init__(self, device):
        print('init buzzers')
        self.f = open('/dev/hidraw0', mode='r+b', buffering=0)
        flag = fcntl.fcntl(self.f.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(self.f.fileno(), fcntl.F_SETFL, flag | os.O_NONBLOCK)
        self.old_bits = 0
        self.queue = Queue()
        self.thread = Thread(target=worker, args=(self,))
        self.thread.daemon = True
        self.thread.start()
        print('init buzzers done')
