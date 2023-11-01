import pygame
from powers import PowerUp
from paddle import *
from pong import *

# color black, rgb scale
BLACK = (0, 0, 0)
PINK = (248, 131, 121)


# Let´s create the paddle class
paddle_sizeA = 100
class BigPaddle(PowerUp):

    def __int__(self):
        print("init")

    def affect_player_A(self):
        global paddle_sizeA
        paddle_sizeA = 200

    def affect_player_B(self):
        pass
