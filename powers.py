import random
from abc import ABC, abstractmethod
from paddle import *
from random import randint

import pygame

BLACK = (0, 0, 0)
WHITE = (255,255,255)

class PowerUp(ABC):

    @abstractmethod
    def affect_player_A(self):
        pass

    @abstractmethod
    def affect_player_B(self):
        pass


class Colision_power(PowerUp, pygame.sprite.Sprite):
    # This class represents the Power. It derives from the "Sprite" class in Pygame.
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def spawn_pos(self):
        self.rect.x = random.randint(100, 600)
        self.rect.y = random.randint(100, 400)

    def affect_player_A(self):
        self.rect.x = random.randint(110, 300)
        self.rect.y = random.randint(200, 400)

    def affect_player_B(self):
        self.rect.x = random.randint(410, 600)
        self.rect.y = random.randint(200, 400)


class Inv_ball(PowerUp, pygame.sprite.Sprite):

    # This class represents the Power. It derives from the "Sprite" class in Pygame.
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([319, 500])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, WHITE, [0, 0, 319, 500])

        self.rect = self.image.get_rect()

    def affect_player_A(self):
        self.rect.x = 30
        self.rect.y = 0

    def affect_player_B(self):
        self.rect.x = 354
        self.rect.y = 0


class modify_paddle(PowerUp, pygame.sprite.Sprite):

    # This class represents a paddle. It derives from the "Sprite" class in Pygame.
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Pass in the color of the Paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!) - Using pygame method
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):

        self.rect.y -= pixels

        # Preventing going too far (off the screen)
        if self.rect.y < 0:
            self.rect.y = 0

    # ONE THAT MOVES IT DOWN

    def moveDown(self, pixels):

        self.rect.y += pixels

        if self.rect.y > 400:
            self.rect.y = 400

    def affect_player_A(self):
        self.rect.x = 20
        self.rect.y = 2


class Freeze_paddle(PowerUp, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        print("innit")

    def affect_player_A(self):
        self.freezeA = 75

    def affect_player_B(self):
        self.freezeB = 75