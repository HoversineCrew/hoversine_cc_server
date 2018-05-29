import pygame
import time
from threading import Thread


class Controller(object):
    def __init__(self, controller_index=0, axis_l_r=0, axis_pow=1):
        pygame.init()
        pygame.joystick.init()

        self._running = True

        self._joystick = pygame.joystick.Joystick(controller_index)
        self._joystick.init()
        self._axis_left_right = axis_l_r
        self._axis_power = axis_pow
        self.output_left_right = 0
        self.output_power = 0
        self.power_modifier = 0.9  # limit the total output 1 = no limit
        self._polling_thread = Thread(target=self.start,)
        self._polling_thread.start()

        self._output_thread = Thread(target=self.send_output, )
        self._output_thread.start()

    def start(self):
        while self._running:
            for event in pygame.event.get():  # User did something
                # print(event)
                self.output_left_right = self.calculate_power(self._joystick.get_axis(self._axis_left_right))
                self.output_power = self.calculate_power(self._joystick.get_axis(self._axis_power))

                # button = self._joystick.get_button(i)

            # Limit polling rate
            # time.sleep(0.2)
        pygame.quit()

    def calculate_power(self, value):
        x = round(value, 2) * 1000 * self.power_modifier
        return x

    def send_output(self):
        # sends output via I2C
        while True:
            print(self.output_power, self.output_left_right)
            time.sleep(1)


xbox = Controller()
while 1:
    time.sleep(0.2)
    # print(xbox.output_left_right)
