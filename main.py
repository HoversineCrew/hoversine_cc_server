import pygame
import time


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
        self.power_modifier = 0.8  # limit the total output 1 = no limit
        self.start()

    def start(self):
        while self._running:
            for event in pygame.event.get():  # User did something
                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")

                self.output_left_right = self._joystick.get_axis(self._axis_left_right) * 1000 * self.power_modifier
                self.output_power = self._joystick.get_axis(self._axis_power) * 1000 * self.power_modifier
                print(self.output_left_right)

                # button = self._joystick.get_button(i)

                # Limit polling rate
                time.sleep(0.2)

        pygame.quit()


xbox = Controller()
