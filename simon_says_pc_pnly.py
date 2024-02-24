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
BACKGROUND = "#b7b7b7"
button_colors = [RED_COLOR, YELLOW_COLOR, BLUE_COLOR, GREEN_COLOR]
player_order = []
is_pressed = tk.StringVar

# root window
pygame.init()
pygame.mixer.init()
window = tk.Tk()
window.configure(background=BACKGROUND)
window.geometry(f'{WIDTH}x{HEIGHT}')
window.title("Simon Says!")



class Light(tk.Button):
    def __init__(self, color, signal, key, state=0):
        tk.Button.__init__(self, window,
                           command=lambda : [self.signal.respond(), self.pressed()],
                           font=15,
                           borderwidth=10,
                           padx=BUTTON_PADDING,
                           pady=BUTTON_PADDING,
                           background= color,
                           width=10)
        self.state = state
        self.signal = signal
        self.key = key

    def pressed(self):
        global player_order, is_pressed
        player_order.append(self.key)
        is_pressed.set("True")


class Signal(tk.Label):
    def __init__(self, text, color, sound, key):
        if color == YELLOW_COLOR:
            padding = 10
        elif color == RED_COLOR:
            padding = 55
        else:
            padding = 40

        tk.Label.__init__(self, window, font=('Comic Sans', 40),text=text, fg=color, bg=BACKGROUND, padx=padding)
        self.key = key

        if sound != None:
            self.sound = Sound(sound)


    def turn_on(self):
        self.grid(column=1, columnspan=2, row=3, rowspan=4, pady=HEIGHT / 2 - 75)
        self.lift()

    def respond(self):
        self.turn_on()
        self.sound.play()
        sleep(0.25)



class Simon:
    WELCOME_MESSAGE = "Welcome to Simon!!"

    # SIGNALS
    red_sig = Signal("RED", button_colors[0], os.path.join('sounds', 'one.wav'), "red")
    yellow_sig = Signal("YELLOW", button_colors[1], os.path.join('sounds', 'two.wav'), "yellow")
    green_sig = Signal("GREEN", button_colors[3], os.path.join('sounds', 'three.wav'), "green")
    blue_sig = Signal("BLUE", button_colors[2], os.path.join('sounds', 'four.wav'), "blue")
    blank = Signal("","#b7b7b7", None, "blank")
    SIGNALS = [red_sig, yellow_sig, green_sig, blue_sig]

    # BUTTONS
    red = Light(button_colors[0], red_sig, "red")
    yellow = Light(button_colors[1], yellow_sig, "yellow")
    blue = Light(button_colors[2], blue_sig, "blue")
    green = Light(button_colors[3], green_sig, "green")
    BUTTONS = [red, yellow, green, blue]

    def __init__(self, debug=True):
        self.debug = debug
        self.sequence: list = []

    def blink_all_buttons(self):
        for signal in self.SIGNALS:
            signal.respond()

    def pack_buttons(self):
        i=0
        for button in Simon.BUTTONS:
            button.grid(column=i, row=0)
            i += 1

    def add_to_sequence(self):
        rand_but = choice(Simon.SIGNALS)
        self.sequence.append(rand_but)

    def lose(self):
        for _ in range(4):
            self.blink_all_buttons()
        exit()

    def playback(self):
        for signal in self.sequence:
            signal.respond()
            window.update()
            sleep(0.5)

    def begin_visual(self):
        self.pack_buttons()
        print(Simon.WELCOME_MESSAGE)

    def begin_game(self):
        self.add_to_sequence()
        self.add_to_sequence()

    def game_loop(self):

        try:
            while True:
                self.add_to_sequence()
                self.playback()

                global player_order, is_pressed

                while len(player_order) < len(self.sequence):
                    window.wait_variable(is_pressed)
                    is_pressed.set("False")

                for i in self.sequence:
                    if i.key != player_order[i]:
                        self.lose()

        except KeyboardInterrupt:
            exit()

    def run(self):
        window.after(1000, self.begin_visual)
        window.after(2000, self.begin_game)
        window.after(2500, self.game_loop())




game = Simon()
game.run()
window.mainloop()



# SO IN ORDER TO GET THE CHECKING TO WORK.
# have second sequence. store button pressed until the number of buttons in it
# equals the length of the sequence.
# if the sequences dont line up
#
#
