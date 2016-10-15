import fcntl
import os
from queue import Queue
from threading import Thread

class BuzzerEvent:
    def __init__(self, buzzer_index, button):
        self.buzzer_index = buzzer_index
        self.button = button
        self.buzzer = None

def worker(buzzers):
    while True:
        buzzers.read()

class BuzzerController:
    def __init__(self, device):
        self.f = open(device, mode='r+b', buffering=0)
        flag = fcntl.fcntl(self.f.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(self.f.fileno(), fcntl.F_SETFL, flag | os.O_NONBLOCK)
        self.old_bits = 0
        self.queue = Queue()
        self.thread = Thread(target=worker, args=(self,))
        self.thread.daemon = True
        self.thread.start()
        self.buzzers = [Buzzer(self, i) for i in range(4)]

    def decode(self, bits):
        mask = 1
        for i in range(0, 20):
            if bits & mask and not(self.old_bits & mask):
                self.queue.put(BuzzerEvent(int(i / 5), i % 5))
            mask = mask << 1
        self.old_bits = bits

    def read(self):
        input = self.f.read(5)
        if input:
            bits = input[4] << 16 | input[3] << 8 | input[2]
            self.decode(bits)

    def set_leds(self):
        self.f.write(bytearray([0, 0,
                                255 if self.buzzers[0].led_state else 0,
                                255 if self.buzzers[1].led_state else 0,
                                255 if self.buzzers[2].led_state else 0,
                                255 if self.buzzers[3].led_state else 0]))

    def get_pressed(self):
        if self.queue.empty():
            return None
        else:
            message = self.queue.get()
            message.buzzer = self.buzzers[message.buzzer_index]
            return message

    def flush(self):
        while self.get_pressed() != None:
            None

class Buzzer:
    def __init__(self, controller, index):
        self.controller = controller
        self.index = index
        self.led_state = False
        self.player = None

    def set_player(self, player):
        self.player = player
        player.buzzer = self

    def set_led(self, led_state):
        self.led_state = led_state
        self.controller.set_leds()
