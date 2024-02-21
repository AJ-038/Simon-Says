import pineworkslabs.RPi as GPIO
from time import sleep
from random import choice
import pygame
from pygame.mixer import Sound

pygame.init()

GPIO.setmode(GPIO.LE_POTATO_LOOKUP)

class Button:
    
    def __init__(self, switch:int, led:int, sound:str, color:str):
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

    def respond(self):
        self.turn_light_on()
        self.sound.play()
        sleep(1)
        self.turn_light_off()
        sleep(0.25)

    def __str__(self):
        return self.color


class Simon:
    
    WELCOME_MESSAGE = ""

    BUTTONS = [

    ]

    def __init__(self, debug=True):
        self.debug = debug
        self.sequence: list[Button] = []  #python 3.10+ only?

    def debut_out(self, *args):
        if self.debug:
            print(*args)
    
    def blink_all_buttoms(self):
        pass

    def add_to_sequence(self):
        pass

    def lose(self):
        pass

    def playback(self):
        pass

    def check_input(self, pressed_button, correct_button):
        pass

    def run(self):
        pass
