import pygame
from random import randint

BLACK = (0, 0, 0)


# let's create the ball class
class Ball(pygame.sprite.Sprite):
    # This class represents a ball. It derives from the "Sprite" class in Pygame.
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball (a rectangle!) - using pygame built in method
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

        self.lastplayerhit = ""

        # setting the ball velocity in the form of [x velocity, y velocity]
        self.velocity = [randint(4, 8), randint(-8, 8)]

    # method that updates the position of the ball
    def move(self, move=False):
        if move:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

    # method that updates the position of the ball once it hit a paddle

    def bounce(self):

            self.velocity[0] = -self.velocity[0]
            # y can still randomly either go up or down
            self.velocity[1] = -self.velocity[1]

