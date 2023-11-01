import pygame
from random import randint
from .config import GlobalSettings
from .paddle import Paddle


# Class Ball represents the ball that bounces around the screen
class Ball(pygame.sprite.Sprite):  # Inherit from Pygame Sprite class
    """
    Ball class represents the ball in a game of Pong. It derives from the "Sprite" class in Pygame.

    Attributes
    ----------
    settings: GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    width: float
        The height of the ball in pixels.
    height: float
        The width of the ball in pixels.
    image: pygame. surface
        A Pygame surface representing the image of the ball.
    rect: pygame. rect
        A Pygame rect representing the position and size of the ball.
    x_velocity: randint
        The velocity of the ball along the x-axis.
    y_velocity: randint
        The velocity of the ball along the y-axis.
    velocity: list
        A list containing the x and y velocities of the ball.
    ball_free: bool
        A boolean indicating whether the ball is colliding with a paddle.

    Methods
    ----------
    update(move: bool) -> None
        Update the position of the ball.

    bounce() -> None
        Bounce the ball off a horizontal surface (paddle).

    bounceUpDown() -> None
        Bounce the ball off a vertical surface (wall).

    handleBallCollision(paddleA: Paddle, paddleB: Paddle) -> str
        Detect collision between the ball and the paddles and change its speed accordingly.

    resetBall() -> None
        Reset the ball to its initial position.

    handleBallMotion(scoreA: int, scoreB: int, ball_owner: str, triggered: bool) -> tuple[int, int, str, bool]
        Handle the ball motion in the screen.

    handleMultipleBallsMotion(self, powerup_owner: str, scoreA: int, scoreB: int) -> tuple[int, int, bool]
        Handle the motion of multiple balls in the screen.

    """

    def __init__(self, filename: str, width: float, height: float, settings: GlobalSettings):
        """

        Initialize the Ball class.

        Parameters
        ----------
        filename : str
            Path to the image file.
        width : float
            The width of the ball in pixels.
        height : float
            The height of the ball in pixels.
        settings : GlobalSettings
            An instance of the `GlobalSettings` class that stores the game settings.
        """

        super().__init__()  # Call the parent class (Sprite) constructor
        self.settings: GlobalSettings = settings  # Pass Ball settings
        self.image: pygame.image = pygame.image.load(filename)  # Load the image
        self.image: pygame.transform = pygame.transform.smoothscale(self.image, (width, height))  # Scale the image
        pygame.draw.rect(self.image, self.settings.BLACK, [width, height, 0, 0])  # Draw the ball
        self.rect: pygame.image = self.image.get_rect()  # Get the rectangle of the ball
        # X and Y velocity
        self.x_velocity: randint = randint(int(-self.settings.height / 70), int(-self.settings.height / 120))
        self.y_velocity: randint = randint(int(self.settings.height / 120), int(self.settings.height / 70))
        self.velocity: list = [self.x_velocity, self.y_velocity]  # Ball velocity
        self.ball_free = True  # Check if the ball is out of paddle bounds

    # Method that updates the position of the ball
    def update(self, move: bool) -> None:
        """
        Update the position of the ball on the screen.

        Parameters
        ----------
        move: bool
            Determine whether the ball should move or not.

        Return
        ----------
        None
        """

        if move:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

    # Methods that update the position of the ball once it hits an obstacle
    # Bounce the ball off a horizontal surface (paddle)
    def bounce(self) -> None:
        """
        Bounce the ball off a horizontal surface (paddle).

        Return
        ----------
        None
        """

        # X changes to opposite direction
        self.velocity[0] = - self.velocity[0]
        # Y Goes up or down randomly
        self.velocity[1] = randint(-8, 8)

    # Bounce the ball off a vertical surface (wall)
    def bounceUpDown(self) -> None:
        """
        Bounce the ball off a vertical surface (wall).

        Return
        ----------
        None
        """

        # X not affected
        # Y changes to opposite direction
        self.velocity[1] = - self.velocity[1]

    # Detect collision between the ball and the paddles and change its speed accordingly
    def handleBallCollision(self, ball_owner: str, paddleA: Paddle, paddleB: Paddle) -> str:
        """
        Detect collision between the ball and the paddles and change its speed accordingly.

        Parameters
        ----------
        ball_owner: str
            The owner of the ball.
        paddleA: Paddle
            A Paddle object representing player A's paddle.
        paddleB: Paddle
            A Paddle object representing player B's paddle.

        Return
        ----------
        ball_owner: str
            The owner of the ball after colliding with a paddle, or None if it is not colliding with any paddles.
        """

        # Detect collision with paddleA
        if pygame.sprite.collide_mask(self, paddleA):
            if self.ball_free:  # if the ball is free, i.e. is not colliding with paddles
                ball_owner: str = 'paddleA'
                # Bounce the ball since it is the first collision (avoids being stuck in the paddle)
                self.bounce()
            self.ball_free = False
        # Detect collision with paddleB
        elif pygame.sprite.collide_mask(self, paddleB):
            if self.ball_free:
                ball_owner: str = 'paddleB'
                self.bounce()
            self.ball_free = False
        else:
            self.ball_free = True
        return ball_owner  # Return the ball owner

    # Reset Ball position
    def resetBall(self) -> None:
        """
        Reset the ball to its initial position. (center of the screen)

        Return
        ----------
        None
        """

        # Initial position of the ball (center of the screen)
        self.rect.x, self.rect.y = (self.settings.initial_pos_x, self.settings.initial_pos_y)

    # Handle the ball motion in the screen
    def handleBallMotion(self, scoreA: int, scoreB: int, ball_owner: str, triggered: bool) -> tuple[
        int, int, str, bool]:
        """
        Handle the ball motion in the screen, update the scores and reset ball's position if it goes out of the screen.
        Update ball's speed if it bounces on top or bottom of the screen.

        Parameters
        ----------
        scoreA: int
            player A's score.
        scoreB: int
            player B's score.
        ball_owner: str
            The owner of the ball.
        triggered: bool
            Indicates if the ball has been triggered to move.

        Return
        ----------
        scoreA: int
            The updated score of player A.
        scoreB: int
            The updated score of player B.
        ball_owner: str
            The updated owner of the ball.
        triggered: bool
            The updated trigger status of the ball.
        """

        # If the ball goes off the right of the screen
        if self.rect.x >= self.settings.width + self.settings.ball_width:
            # Add score to player A
            scoreA += self.settings.SCORE_ADDER_A
            # Reset the ball
            self.resetBall()
            ball_owner = None  # Reset the ball owner
            triggered: bool = False  # Reset the trigger
            # Ball direction turns to the left
            self.velocity[0] = - self.velocity[0]
        # If the ball goes off the left side of the screen
        if self.rect.x <= 0 - self.settings.ball_width:
            # Add score to player B
            scoreB += self.settings.SCORE_ADDER_B
            # Reset the ball
            self.resetBall()
            ball_owner = None  # Reset the ball owner
            triggered: bool = False  # Reset the trigger
            # Ball direction turns to the right
            self.velocity[0] = - self.velocity[0]
        # if the ball hits the bottom of the screen, bounce it
        if self.rect.y >= self.settings.height - self.settings.ball_height:
            self.bounceUpDown()
        # If the ball hits the top of the screen, bounce it
        if self.rect.y <= 0:
            self.bounceUpDown()
        return scoreA, scoreB, ball_owner, triggered

    # Handle multiple balls motion in the screen
    def handleMultipleBallsMotion(self, powerup_owner: str, scoreA: int, scoreB: int) -> tuple[int, int, bool]:
        """
        Handle the motion of multiple balls in the screen, update the scores and kill each ball that goes out of the screen.
        Update ball's speed if it bounces on top or bottom of the screen.

        Parameters
        ----------
        powerup_owner: str
            The player who owns the powerup that caused multiple balls to appear.
        scoreA: int
            player A's score.
        scoreB: int
            player B's score.

        Return
        ----------
        scoreA: int
            The updated score of player A.
        scoreB: int
            The updated score of player B.
        should_kill: bool
            A boolean indicating whether the extra ball should be removed from the game.
        """

        # Boolean to check if the ball is out of the screen
        should_kill: bool = False
        # If the ball goes off the right of the screen
        if self.rect.x >= self.settings.width + self.settings.ball_width:
            if powerup_owner == 'paddleA':  # If the ball is owned by player A
                # Add score to player A
                scoreA += self.settings.SCORE_ADDER_A
            # Ball out of the screen --> kill the ball
            should_kill: bool = True
            self.kill()  # kill the ball
        # If the ball goes off the left of the screen
        if self.rect.x <= 0 - self.settings.ball_width:
            if powerup_owner == 'paddleB':  # If the ball is owned by player B
                # Add score to player B
                scoreB += self.settings.SCORE_ADDER_B
            # Ball out of the screen --> kill the ball
            should_kill: bool = True
            self.kill()  # kill the ball
        # If the ball hits the bottom of the screen, bounce it
        if self.rect.y >= self.settings.height - self.settings.ball_height:
            self.bounceUpDown()
        # If the ball hits the top of the screen, bounce it
        if self.rect.y <= 0:
            self.bounceUpDown()
        return scoreA, scoreB, should_kill
