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

        try:  # Controller starting
            self._joystick = pygame.joystick.Joystick(controller_index)
            self._joystick.init()
        except pygame.error:
            print("No Controller available")
            pygame.quit()
            return

        self._axis_left_right = axis_l_r
        self._axis_power = axis_pow

        self._polling_rate = pollingrate  # how often are new values

        self._raw_output = [0.00, 0.00]  # help variable for raw controller values
        self.outputs = [0.00, 0.00]  # Controls for wheel 1 and wheel 2 Ranges from -1000 to 1000

        self.power_modifier = 0.9  # limit the total output 1 = no limit
        self._precision_multiplier = 1.0  # In precision mode(as long button 0 is pressed) decrease max. speed

        # Start polling and output threads
        self._event_thread = Thread(target=self.event_poll, )
        self._event_thread.start()

        self._output_thread = Thread(target=self.send_output, args=(self._polling_rate,))
        self._output_thread.start()

    def event_poll(self):
        while self.active:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.JOYAXISMOTION:
                    self._raw_output[0] = self._joystick.get_axis(self._axis_left_right)
                    self._raw_output[1] = self._joystick.get_axis(self._axis_power)

                elif event.type == pygame.JOYBUTTONDOWN:  # activate slowmo when button 0 is pressed
                    if self._joystick.get_button(0) == 1:
                        self._precision_multiplier = 0.1  # limit to 10% max

                elif event.type == pygame.JOYBUTTONUP:  # deactivate slowmo when button 0 is released
                    if self._joystick.get_button(0) == 0:
                        self._precision_multiplier = 1  # no limit

        pygame.quit()
        print("loop ended")

    def send_output(self, pollingrate):
        # sends output via I2C
        while self.active:
            self.outputs[0] = self._raw_output[0] * self.power_modifier * self._precision_multiplier * 1000.00
            self.outputs[1] = self._raw_output[1] * self.power_modifier * self._precision_multiplier * 1000.00
            #print(self.outputs)
            time.sleep(pollingrate)


if __name__ == '__main__':
    xbox = Controller(pollingrate=0.2)
    time.sleep(15)
    xbox.active = False
