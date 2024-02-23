# Names: Amanda Berg and Lily Williams
# PC only, uses tkinter to create a GUI for the game
# to run

from time import sleep
from random import choice
import pygame
from pygame.mixer import Sound
import os
import tkinter as tk

HEIGHT = 500
WIDTH = 530
BUTTON_PADDING = 10
RED_COLOR = "#822121"
YELLOW_COLOR = "#d6d335"
BLUE_COLOR = "#2393d3"
GREEN_COLOR = "#5bd323"
button_colors = [RED_COLOR, YELLOW_COLOR, BLUE_COLOR, GREEN_COLOR]

# root window
pygame.init()
pygame.mixer.init()
window = tk.Tk()
window.configure(background="#b7b7b7")
window.geometry(f'{WIDTH}x{HEIGHT}')
window.title("Simon Says!")


class Light(tk.Button):
    def __init__(self, color, signal, state=0):
        tk.Button.__init__(self, window,
                           command=lambda : self.respond(),
                           font=15,
                           borderwidth=10,
                           padx=BUTTON_PADDING,
                           pady=BUTTON_PADDING,
                           background= color,
                           width=10)
        self.state = state
        self.signal = signal

    def respond(self):
        self.signal.turn_on()
        self.signal.sound.play()

class Signal(tk.Label):
    def __init__(self, text, color, sound):
        if color == YELLOW_COLOR:
            padding = 10
        elif color == RED_COLOR:
            padding = 55
        else:
            padding = 30

        tk.Label.__init__(self, window, font=('Comic Sans', 40),text=text, fg=color, bg="#b7b7b7", padx=padding)
        self.sound = Sound(sound)

    def turn_on(self):
        self.grid(column=1, columnspan=2, row=3, rowspan=4, pady=HEIGHT / 2 - 75)
        self.lift()


## MAIN STUFF ##

# signals
red_sig = Signal("RED", button_colors[0], os.path.join('sounds', 'one.wav'))
yellow_sig = Signal("YELLOW", button_colors[1], os.path.join('sounds', 'two.wav'))
green_sig = Signal("GREEN", button_colors[3], os.path.join('sounds', 'three.wav'))
blue_sig =Signal("BLUE", button_colors[2], os.path.join('sounds', 'four.wav'))
signals = [red_sig, yellow_sig, green_sig, blue_sig]

# create buttons
red = Light(button_colors[0], red_sig)
yellow = Light(button_colors[1], yellow_sig)
blue = Light(button_colors[2], blue_sig)
green = Light(button_colors[3], green_sig)
buttons = [red, yellow, green, blue]

i=0
for button in buttons:
    button.grid(column=i, row=0)
    i += 1

# create signals

window.mainloop()

#################
# PLAN
#################

# PHYSICAL OBJECTS
# 4 Buttons                     DONE
# 4 'lights'                    DONE
# Simon

# GAME MECHANICS
# light
#   has:
#   can:    respond --> that flashes light and plays sound
#
#
# Simon
#   has: four buttons, four lights
#   can:    add_to_sequence --> add random button to sequence
#           blink_all_buttons --> blink all one after another
#           lose --> if button pressed is not the next one in the sequence
#           playback --> play sequence
#           check_input --> checks if pressed button is the crrect one
#           run -->
#               print welcome message
#               add two things to sequence
#               try: