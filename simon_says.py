# Names: Amanda Berg and Lily Williams

import pineworkslabs.RPi as GPIO
from time import sleep
from random import choice
import pygame
from pygame.mixer import Sound
import os

pygame.init()

GPIO.setmode(GPIO.LE_POTATO_LOOKUP)


class Button:
    
    def __init__(self, switch: int, led: int, sound: str, color: str):
        self.switch = switch
        self.led = led
        self.sound: Sound = Sound(sound)
        self.color = color

    def setupGPIO(self):
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.sestup(self.led, GPIO.OUT)

    def turn_light_on(self):
        GPIO.output(self.led, True)

    def turn_light_off(self):
        GPIO.output(self.led, False)

    def is_pressed(self):
        result = GPIO.input(self.switch)
        if result == True:
            return True
        else:
            return False

    def respond(self,play_time, wait_time, lights):
        if not lights:
            self.turn_light_on()

        self.sound.play()
        sleep(play_time)
        self.turn_light_off()
        sleep(wait_time)

    def __str__(self):
        return self.color


class Simon:
    
    WELCOME_MESSAGE = "Welcome to SIMON!!! Press CTRL+C to quit anytime."

    # Paths should use os.path.join()
    # Do not use C:\\directory\\directory2\\
    # Windows is wrong with the backslash
    #       avoid windows paths of \\directory\\directory2\\
    # do not use the root directory of the VS code project
    BUTTONS = [
        Button(switch=20, led=6, sound=os.path.join("sounds", "one.wav"), color="red"),
        Button(switch=16, led=13, sound=os.path.join("sounds", "two.wav"), color="blue"),
        Button(switch=12, led=19, sound=os.path.join("sounds", "three.wav"), color="yellow"),
        Button(switch=26, led=21, sound=os.path.join("sounds", "four.wav"), color="green")
    ]

    def __init__(self, debug=True):
        self.debug = debug
        self.sequence: list[Button] = []  #python 3.10+ only?
        self.score = 0

    def debut_out(self, *args):
        if self.debug:
            print(*args)
    
    def blink_all_buttoms(self):
        leds = []
        for button in Simon.BUTTONS:
            leds.append(button.led)
        GPIO.output(leds, True)
        sleep(0.5)
        GPIO.output(leds, False)
        sleep(0.5)

        # alternative if above doesnt work on potato:
        # for button in Simon.BUTTONS:
        #     button.turn_light_on()
        #     sleep(0.5)
        #     button.turn_light_off()
        #     sleep(0.5)

    def add_to_sequence(self):
        random_button = choice(Simon.BUTTONS)
        self.sequence.append(random_button)

    def lose(self):
        for _ in range(4):
            self.blink_all_buttoms()
        print(f"You made it to a sequence of {self.score}")
        GPIO.cleanup()
        exit()

    def playback(self, play_time, wait_time, lights):
        for button in self.sequence:
            button.respond(play_time, wait_time, lights)

    def wait_for_press(self):
        while True:
            for button in Simon.BUTTONS:
                if button.is_pressed():
                    self.debut_out(button.color)
                    button.respond(1,0.5, True)
                    return button  # this kills the while true and tells us which button was pressed

    def check_input(self, pressed_button, correct_button):
        if pressed_button.switch != correct_button.switch:
            self.lose()
    
    def run(self):
        print(Simon.WELCOME_MESSAGE)

        # game starts with 2 buttons in sequence
        self.add_to_sequence()
        self.add_to_sequence()

        # vars that affect difficulty settings
        play_time = 1.0
        wait_time = 0.5
        lights = True

        # use ctrl + c to kill the game at any time
        try:

            while True:
                self.add_to_sequence()

                # added difficulty settings
                if len(self.sequence) in [5, 7]:
                    play_time -= 0.1
                    wait_time -= 0.1
                if len(self.sequence) in [10, 13]:
                    play_time -= 0.1
                    wait_time -= 0.05
                if len(self.sequence) == 15:
                    lights = False

                self.playback(play_time, wait_time, lights)
                self.debut_out(*self.sequence)
                for button in self.sequence:
                    pressed_button = self.wait_for_press()
                    self.check_input(pressed_button, button)
                    self.score += 1

        except KeyboardInterrupt:
            GPIO.cleanup()
        

simon = Simon()
simon.run()
