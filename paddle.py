import pygame

# 1

# color black, rgb scale
BLACK = (0, 0, 0)
PINK = (248, 131, 121)


# Lets create the paddle class

class Paddle(pygame.sprite.Sprite):
    # This class represents a paddle. It derives from the "Sprite" class in Pygame.
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Pass in the color of the Paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.freeze_duration = 0

        # Draw the paddle (a rectangle!) - Using pygame method
        pygame.draw.rect(self.image, color, [0, 0, width, height], border_radius= 4)

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        if self.freeze_duration > 0:
            self.freeze_duration -= 1

        else:
            self.rect.y -= pixels

            # Preventing going too far (off the screen)
            if self.rect.y < 0:
                self.rect.y = 0


    def moveDown(self, pixels):
        if self.freeze_duration > 0:
            self.freeze_duration -= 1

        else:
            self.rect.y += pixels

            if self.rect.y > 400:
                self.rect.y = 400

