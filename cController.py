#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import time
from threading import Thread


class Controller(object):
    def __init__(self, controller_index=0, axis_l_r=0, axis_pow=1, pollingrate=1.00):
        pygame.init()
        pygame.joystick.init()

        self.active = True

        self._joystick = pygame.joystick.Joystick(controller_index)
        self._joystick.init()
        self._axis_left_right = axis_l_r
        self._axis_power = axis_pow
        self._polling_rate = pollingrate
        self.output_left_right = 0
        self.output_power = 0
        self.power_modifier = 0.9  # limit the total output 1 = no limit

        self._event_thread = Thread(target=self.start, )
        self._event_thread.start()

        self._output_thread = Thread(target=self.send_output, args=(self._polling_rate,))
        self._output_thread.start()

    def start(self):
        while self.active:
            for event in pygame.event.get():  # User did something
                # print(event)
                self.output_left_right = self.calculate_power(self._joystick.get_axis(self._axis_left_right))
                self.output_power = self.calculate_power(self._joystick.get_axis(self._axis_power))

        pygame.quit()
        print("loop ended")

    def calculate_power(self, value):
        x = round(value, 2) * 1000 * self.power_modifier
        return x

    def send_output(self, pollingrate):
        # sends output via I2C
        while self.active:
            print(self.output_power, self.output_left_right)
            time.sleep(pollingrate)


if __name__ == '__main__':
    xbox = Controller(pollingrate=0.2)
    time.sleep(5)
    xbox.active = False
