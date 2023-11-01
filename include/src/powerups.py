import pygame
from abc import ABC, abstractmethod
from random import randint
from src.config import GlobalSettings
from src.paddle import Paddle


# Class Parent for Powerups
class PowerUp(pygame.sprite.Sprite, ABC):  # sprite-Simple base class for visible game objects
    """
    PowerUp class that has the methods to draw, activate and deactivate the powerup. It derives from the "Sprite"
    and 'ABC' classes in Pygame. It has six child classes that inherit from it.

    Attributes
    ----------
    settings : GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    visible_time : int
        Visible time in seconds for the power-up icon before it is activated.
    width : float
        Width of the power-up icon.
    height : float
        Height of the power-up icon.
    owner : str
        The owner of the power-up defines which player should be affected.
    image : pygame.Surface
        The image of the power-up icon.
    rect : pygame.Rect
        The rectangle of the power-up icon.

    Methods
    ----------
    @abstractmethod
    affect_playerA(self, player_A: Paddle) -> None
        Abstract method to affect player A.

    @abstractmethod
    affect_playerB(self, player_B: Paddle) -> None
        Abstract method to affect player B.

    @abstractmethod
    run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Abstract method to run the power-up.

    @abstractmethod
    revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Abstract method to revert the power-up.

    draw(self, filename: str) -> None
        Draw the power-up icon on the screen.

    """

    # Set the PowerUp visible time in seconds
    visible_time: int = GlobalSettings.POWERUP_VISIBLE_TIME

    def __init__(self, ball_owner: str, width: float, height: float, settings: GlobalSettings):
        """
        Initialize the PowerUp class.

        Parameters
        ----------
        ball_owner : str
            The owner of the ball defines which player should be affected.
        width : float
            Width of the power-up icon.
        height : float
            Height of the power-up icon.
        settings : GlobalSettings
            An instance of the `GlobalSettings` class that stores the game settings.

        Return
        ----------
        None
        """

        super().__init__()  # Call the parent class (Sprite) constructor
        self.settings: GlobalSettings = settings  # Pass PowerUp settings
        self.width, self.height = width, height  # Set PowerUp width and height
        self.owner = ball_owner  # Set the ball owner to affect a certain player

    # Abstract Method that affects player A
    @abstractmethod
    def affect_playerA(self, player_A: Paddle) -> None:
        """
        Abstract method to affect player A, if it is the owner.

        Parameters
        ----------
        player_A : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """
        pass

    # Abstract Method that affects player B
    @abstractmethod
    def affect_playerB(self, player_B: Paddle) -> None:
        """
        Abstract method to affect player B, if it is the owner.

        Parameters
        ----------
        player_B : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """
        pass

    # Abstract Method that runs the powerup
    @abstractmethod
    def run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Abstract method to run the powerup.

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """
        pass

    # Abstract Methods that reverts the powerup
    @abstractmethod
    def revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Abstract method to revert the powerup.

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """
        pass

    # Draw the powerup icon on the screen
    def draw(self, filename: str) -> None:
        """
        Load and scale the image, draw and get the rect object, and set the position of the powerup on the field.

        Parameters
        ----------
        filename : str
            The filename of the image to be loaded.

        Return
        ----------
        None
        """

        # Load and scale the image
        self.image: pygame.image = pygame.image.load(filename).convert_alpha()
        self.image: pygame.transform = pygame.transform.scale(self.image, (self.width, self.height))
        # Draw and get the rect object
        pygame.draw.rect(self.image, self.settings.BLACK, [self.width, self.height, 0, 0])
        self.rect: pygame.rect = self.image.get_rect()
        # Set the position of the powerup on the field
        self.rect.y = randint(self.settings.powerup_field_height[0], self.settings.powerup_field_height[1])
        self.rect.x = randint(self.settings.powerup_field_width[0], self.settings.powerup_field_width[1])


# === Mandatory PowerUps ===

# AntMan: The AntMan "Power-up" makes the player’s Paddle bigger
class ShrinkEnlarge(PowerUp):
    """
    The Ant-Man "Power-up" represents a hero that makes the ball owner's Paddle bigger.
        This class inherits from the PowerUp class.

    Attributes
    ----------
    active_time : int
        Active time in seconds for the power-up before it is deactivated.
    probability : int
        Probability of the power-up to be activated.
    name : str
        Name of the power-up.
    description : str
        Description of the power-up.
    icon : str
        Powerup Icon path.
    width : float
        Width of the power-up icon.
    height : float
        Height of the power-up icon.
    settings : GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    owner : str
        The owner of the power-up defines which player should be affected.
    image : pygame.Surface
        The image of the power-up icon.
    rect : pygame.Rect
        The rectangle of the power-up icon.

    Methods
    ----------
    affect_playerA(self, player_A: Paddle) -> None
        Change Paddle A size and border radius.

    affect_playerA(self, player_B: Paddle) -> None
        Change Paddle B size and border radius.

    run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Run the power-up affecting the ball owner.

    revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Revert the Paddle size and border radius.

    """

    active_time: int = 5  # PowerUp active time in seconds
    probability: int = 15  # PowerUp probability
    name: str = 'Ant-Man'  # PowerUp name
    description: str = 'Enlarges your paddle size'  # Powerup Description
    icon: str = 'img/icons/powerup5.png'  # Icon path

    def __init__(self, ball_owner: str, width: float, height: float, settings: GlobalSettings):
        """
        Initialize ShrinkEnlarge class.

        Parameters
        ----------
        ball_owner : str
            The owner of the ball defines which player should be affected.
        width : float
            Width of the power-up icon.
        height : float
            Height of the power-up icon.
        settings : GlobalSettings
            An instance of the `GlobalSettings` class that stores the game settings.

        Return
        ----------
        None
        """

        # Call the parent class (Powerup)
        super().__init__(ball_owner, width, height, settings)
        super().draw(self.icon)  # Call the draw method

    def affect_playerA(self, player_A: Paddle) -> None:
        """
        Affect the size and border radius of player A's paddle.

        Parameters
        ----------
        player_A : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Change the paddle A size and border radius
        player_A.border_radius = 12
        player_A.image = pygame.transform.scale(player_A.image, (player_A.rect.width * 1.5, player_A.rect.height * 2))
        player_A.height = self.settings.paddle_height_a * 2

    def affect_playerB(self, player_B: Paddle) -> None:
        """
        Affect the size and border radius of player B's paddle.

        Parameters
        ----------
        player_B : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Change the paddle B size and border radius
        player_B.border_radius = 12
        player_B.image = pygame.transform.scale(player_B.image, (player_B.rect.width * 1.5, player_B.rect.height * 2))
        player_B.height = self.settings.paddle_height_b * 2

    def run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:  # Affects the ball owner
        """
        Abstract method to run the powerup.

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        if self.owner == 'paddleA':
            self.affect_playerA(paddleA)
        elif self.owner == 'paddleB':
            self.affect_playerB(paddleB)

    def revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Abstract method to revert the powerup. (Revert the Paddle size and border radius)

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        # Revert the paddle size and border radius
        paddleA.border_radius, paddleB.border_radius = self.settings.PADDLE_ROUND_CORNERS_A, \
            self.settings.PADDLE_ROUND_CORNERS_B
        paddleA.image = pygame.transform.scale(paddleA.image, (paddleA.rect.width, paddleA.rect.height))
        paddleA.height = self.settings.paddle_height_a
        paddleB.image = pygame.transform.scale(paddleB.image, (paddleB.rect.width, paddleB.rect.height))
        paddleB.height = self.settings.paddle_height_b


# Black Widow: The Black Widow "Power-up" freezes the position of the player’s paddle
class Freeze(PowerUp):
    """
    The Black Widow "Power-up" represents a hero that freezes the position of the enemy´s paddle.
        This class inherits from the PowerUp class.

    Attributes
    ----------
    active_time : int
        Active time in seconds for the power-up before it is deactivated.
    probability : int
        Probability of the power-up to be activated.
    name : str
        Name of the power-up.
    description : str
        Description of the power-up.
    icon : str
        Powerup Icon path.
    width : float
        Width of the power-up icon.
    height : float
        Height of the power-up icon.
    settings : GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    owner : str
        The owner of the power-up defines which player should be affected.
    image : pygame.Surface
        The image of the power-up icon.
    rect : pygame.Rect
        The rectangle of the power-up icon.

    Methods
    ----------
    affect_playerA(self, player_A: Paddle) -> None
        Freeze Paddle A.

    affect_playerA(self, player_B: Paddle) -> None
        Freeze Paddle B.

    run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Run the power-up affecting the opponent and not the ball owner.

    revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Revert the Paddle speed.

    """

    active_time: int = 3  # PowerUp active time in seconds
    probability: int = 20  # PowerUp probability
    name: str = 'Black Widow'  # PowerUp name
    description: str = 'Freezes your opponent paddle'  # Powerup Description
    icon: str = 'img/icons/powerup3.png'  # Icon path

    def __init__(self, ball_owner: str, width: float, height: float, settings: GlobalSettings):
        """
        Initialize Freeze class.

        Parameters
        ----------
        ball_owner : str
            The owner of the ball defines which player should be affected.
        width : float
            Width of the power-up icon.
        height : float
            Height of the power-up icon.
        settings : GlobalSettings
            An instance of the `GlobalSettings` class that stores the game settings.

        Return
        ----------
        None
        """

        # Call the parent class (Powerup)
        super().__init__(ball_owner, width, height, settings)
        super().draw(self.icon)  # Call the draw method

    def affect_playerA(self, player_A: Paddle) -> None:
        """
        Freeze Paddle A.

        Parameters
        ----------
        player_A : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Freeze player A
        self.settings.paddle_speed_a = 0

    def affect_playerB(self, player_B: Paddle) -> None:
        """
        Freeze Paddle B.

        Parameters
        ----------
        player_B : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Freeze player B
        self.settings.paddle_speed_b = 0

    def run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:  # Does not affect the ball owner
        """
        Abstract method to run the powerup.

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        # If the ball is owned by player A
        if self.owner == 'paddleA':
            # Freeze player B
            self.affect_playerB(paddleB)
            # If the ball is owned by player B
        elif self.owner == 'paddleB':
            # Freeze player A
            self.affect_playerA(paddleA)

    def revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Abstract method to revert the powerup. (Revert the paddle speed)

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        # Revert the paddle speed
        self.settings.paddle_speed_a = self.settings.default_paddle_speed
        self.settings.paddle_speed_b = self.settings.default_paddle_speed


# Scarlet Witch: The Scarlet Witch "Power-up" creates multiple balls that move in the different directions
class MultipleBalls(PowerUp):
    """
    The Scarlet Witch "Power-up" represents a hero that creates multiple balls that move in the different directions.
        This class inherits from the PowerUp class.

    Attributes
    ----------
    active_time : int
        Active time in seconds for the power-up before it is deactivated.
    probability : int
        Probability of the power-up to be activated.
    name : str
        Name of the power-up.
    description : str
        Description of the power-up.
    icon : str
        Powerup Icon path.
    width : float
        Width of the power-up icon.
    height : float
        Height of the power-up icon.
    settings : GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    owner : str
        The owner of the power-up defines which player should be affected.
    image : pygame.Surface
        The image of the power-up icon.
    rect : pygame.Rect
        The rectangle of the power-up icon.

    Methods
    ----------
    affect_playerA(self, player_A: Paddle) -> None
        Has no effect on player A. Method takes place in 'PongVerse' class.

    affect_playerA(self, player_B: Paddle) -> None
        Has no effect on player B. Method takes place in 'PongVerse' class.

    run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Has no effect. Method takes place in 'PongVerse' class.

    revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Has no effect. Method takes place in 'PongVerse' class.

    """

    active_time: int = 30  # PowerUp active time in seconds
    probability: int = 10  # PowerUp probability
    name: str = 'Scarlet Witch'  # PowerUp name
    description: str = 'Multiple balls that score for you'  # Powerup Description
    icon: str = 'img/icons/powerup6.png'  # Icon path

    def __init__(self, ball_owner: str, width: float, height: float, settings: GlobalSettings):
        """
        Initialize MultipleBalls class.

        Parameters
        ----------
        ball_owner : str
            The owner of the ball defines which player should be affected.
        width : float
            Width of the power-up icon.
        height : float
            Height of the power-up icon.
        settings : GlobalSettings
            An instance of the `GlobalSettings` class that stores the game settings.

        Return
        ----------
        None
        """

        # Call the parent class (Powerup)
        super().__init__(ball_owner, width, height, settings)
        super().draw(self.icon)  # Call the draw method

    # -- Powerup controlled on PongGame class --

    def affect_playerA(self, player_A: Paddle) -> None:
        """
        Multiple balls score for player A.

        Parameters
        ----------
        player_A : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """
        pass

    def affect_playerB(self, player_B: Paddle) -> None:
        """
        Multiple balls score for player B.

        Parameters
        ----------
        player_B : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """
        pass

    def run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:  # Does not affect the ball owner
        """
        Abstract method to run the powerup.

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        pass

    def revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Abstract method to revert the powerup. (Removes extra balls from the game)

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        pass


# === Optional PowerUps ===

# Quicksilver: The Quicksilver "Power-up" increases the speed of the player’s paddle
class FasterPaddle(PowerUp):
    """
    The Quicksilver "Power-up" represents a hero that increases the speed of the player’s paddle.
        This class inherits from the PowerUp class.

    Attributes
    ----------
    active_time : int
        Active time in seconds for the power-up before it is deactivated.
    probability : int
        Probability of the power-up to be activated.
    name : str
        Name of the power-up.
    description : str
        Description of the power-up.
    icon : str
        Powerup Icon path.
    width : float
        Width of the power-up icon.
    height : float
        Height of the power-up icon.
    settings : GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    owner : str
        The owner of the power-up defines which player should be affected.
    image : pygame.Surface
        The image of the power-up icon.
    rect : pygame.Rect
        The rectangle of the power-up icon.

    Methods
    ----------
    affect_playerA(self, player_A: Paddle) -> None
        Increase Paddle A speed.

    affect_playerA(self, player_B: Paddle) -> None
        Increase Paddle B speed.

    run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Run the power-up affecting the ball owner.

    revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Revert Paddles speed to default speed.

    """

    active_time: int = 6  # PowerUp active time in seconds
    probability: int = 15  # PowerUp probability
    name: str = 'Quicksilver'  # PowerUp name
    description: str = 'Increases your paddle speed'  # Powerup Description
    icon: str = 'img/icons/powerup1.png'  # Icon path

    def __init__(self, ball_owner: str, width: float, height: float, settings: GlobalSettings):
        """
        Initialize FasterPaddle class.

        Parameters
        ----------
        ball_owner : str
            The owner of the ball defines which player should be affected.
        width : float
            Width of the power-up icon.
        height : float
            Height of the power-up icon.
        settings : GlobalSettings
            An instance of the `GlobalSettings` class that stores the game settings.

        Return
        ----------
        None
        """

        # Call the parent class (Powerup)
        super().__init__(ball_owner, width, height, settings)
        super().draw(self.icon)  # Call the draw method

    def affect_playerA(self, player_A: Paddle) -> None:
        """
        Increase Paddle A speed.

        Parameters
        ----------
        player_A : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Increase player A paddle speed
        self.settings.paddle_speed_a = self.settings.faster_paddle_speed

    def affect_playerB(self, player_B: Paddle) -> None:
        """
        Increase Paddle B speed.

        Parameters
        ----------
        player_B : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Increase player B paddle speed
        self.settings.paddle_speed_b = self.settings.faster_paddle_speed

    def run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:  # Affects the ball owner
        """
        Abstract method to run the powerup.

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        if self.owner == 'paddleA':
            self.affect_playerA(paddleA)
        elif self.owner == 'paddleB':
            self.affect_playerB(paddleB)

    def revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Abstract method to revert the powerup. (Revert the Paddle to default speed)

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        # Revert player A and player B paddle speed
        self.settings.paddle_speed_a = self.settings.default_paddle_speed
        self.settings.paddle_speed_b = self.settings.default_paddle_speed


# Iron Man: The Iron Man "Power-up" doubles the score of the player that hits the ball
class DoubleScore(PowerUp):
    """
    The Iron Man "Power-up" represents a hero that doubles the score of the player that hits the ball.
        This class inherits from the PowerUp class.

    Attributes
    ----------
    active_time : int
        Active time in seconds for the power-up before it is deactivated.
    probability : int
        Probability of the power-up to be activated.
    name : str
        Name of the power-up.
    description : str
        Description of the power-up.
    icon : str
        Powerup Icon path.
    width : float
        Width of the power-up icon.
    height : float
        Height of the power-up icon.
    settings : GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    owner : str
        The owner of the power-up defines which player should be affected.
    image : pygame.Surface
        The image of the power-up icon.
    rect : pygame.Rect
        The rectangle of the power-up icon.

    Methods
    ----------
    affect_playerA(self, player_A: Paddle) -> None
        Double player A score.

    affect_playerA(self, player_B: Paddle) -> None
        Double player B score.

    run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Run the power-up affecting the ball owner.

    revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Revert Players' score adder to default value.

    """

    active_time: int = 10  # PowerUp active time in seconds
    probability: int = 25  # PowerUp probability
    name: str = 'Iron Man'  # PowerUp name
    description: str = 'Doubles your score'  # Powerup Description
    icon: str = 'img/icons/powerup4.png'  # Icon path

    def __init__(self, ball_owner: str, width: float, height: float, settings: GlobalSettings):
        """
        Initialize DoubleScore class.

        Parameters
        ----------
        ball_owner : str
            The owner of the ball defines which player should be affected.
        width : float
            Width of the power-up icon.
        height : float
            Height of the power-up icon.
        settings : GlobalSettings
            An instance of the `GlobalSettings` class that stores the game settings.

        Return
        ----------
        None
        """

        # Call the parent class (Powerup)
        super().__init__(ball_owner, width, height, settings)
        super().draw(self.icon)  # Call the draw method

    def affect_playerA(self, player_A: Paddle) -> None:
        """
        Double player A score.

        Parameters
        ----------
        player_A : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Double the score of player A
        self.settings.SCORE_ADDER_A = 2

    def affect_playerB(self, player_B: Paddle) -> None:
        """
        Double player B score.

        Parameters
        ----------
        player_B : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Double the score of player B
        self.settings.SCORE_ADDER_B = 2

    def run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:  # Affects the ball owner
        """
        Abstract method to run the powerup.

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        if self.owner == 'paddleA':
            self.affect_playerA(paddleA)
        elif self.owner == 'paddleB':
            self.affect_playerB(paddleB)

    def revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Abstract method to revert the powerup. (Revert Score Adder to default value)

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        # Revert the score adder to 1
        self.settings.SCORE_ADDER_A, self.settings.SCORE_ADDER_B = 1, 1


# Captain America: The Captain America "Power-up" creates a shield that protects the player’s paddle from the ball
class Shield(PowerUp):
    """
    The Captain America "Power-up" represents a hero that creates a 'Vibranium' shield that protects the
    player’s paddle from the opponent to score a point.
        This class inherits from the PowerUp class.

    Attributes
    ----------
    active_time : int
        Active time in seconds for the power-up before it is deactivated.
    probability : int
        Probability of the power-up to be activated.
    name : str
        Name of the power-up.
    description : str
        Description of the power-up.
    icon : str
        Powerup Icon path.
    width : float
        Width of the power-up icon.
    height : float
        Height of the power-up icon.
    settings : GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    owner : str
        The owner of the power-up defines which player should be affected.
    image : pygame.Surface
        The image of the power-up icon.
    rect : pygame.Rect
        The rectangle of the power-up icon.

    Methods
    ----------
    affect_playerA(self, player_A: Paddle) -> None
        Create a shield for player A. (Height = 100%)

    affect_playerA(self, player_B: Paddle) -> None
        Create a shield for player B. (Height = 100%)

    run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Run the power-up affecting the ball owner.

    revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Revert the Paddle size.

    """

    active_time: int = 6  # PowerUp active time in seconds
    probability: int = 15  # PowerUp probability
    name: str = 'Captain America'  # PowerUp name
    description: str = 'Creates a shield on your paddle'  # Powerup Description
    icon: str = 'img/icons/powerup2.png'  # Icon path

    def __init__(self, ball_owner: str, width: float, height: float, settings: GlobalSettings):
        """
        Initialize Shield class.

        Parameters
        ----------
        ball_owner : str
            The owner of the ball defines which player should be affected.
        width : float
            Width of the power-up icon.
        height : float
            Height of the power-up icon.
        settings : GlobalSettings
            An instance of the `GlobalSettings` class that stores the game settings.

        Return
        ----------
        None
        """

        # Call the parent class (Powerup)
        super().__init__(ball_owner, width, height, settings)
        super().draw(self.icon)  # Call the draw method

    def affect_playerA(self, player_A: Paddle) -> None:
        """
        Create a shield for player A. (Height = 100%)

        Parameters
        ----------
        player_A : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Create a shield on the paddle A (Height = 100%)
        player_A.image = pygame.transform.scale(player_A.image,
                                                (player_A.rect.width * 1.15, self.settings.height))
        player_A.height = self.settings.height

    def affect_playerB(self, player_B: Paddle) -> None:
        """
        Create a shield for player B. (Height = 100%)

        Parameters
        ----------
        player_B : Paddle
            Player A paddle object.

        Return
        ----------
        None
        """

        # Create a shield on the paddle B (Height = 100%)
        player_B.image = pygame.transform.scale(player_B.image,
                                                (player_B.rect.width * 1.15, self.settings.height))
        player_B.height = self.settings.height

    def run_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:  # Affects the ball owner
        """
        Abstract method to run the powerup.

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        if self.owner == 'paddleA':
            self.affect_playerA(paddleA)
        elif self.owner == 'paddleB':
            self.affect_playerB(paddleB)

    def revert_powerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Abstract method to revert the powerup. (Revert the Paddle size)

        Parameters
        ----------
        paddleA : Paddle
            Player A paddle object.
        paddleB : Paddle
            Player B paddle object.

        Return
        ----------
        None
        """

        # Revert paddle A and paddle B to their original size
        paddleA.image = pygame.transform.scale(paddleA.image, (paddleA.rect.width, paddleA.rect.height))
        paddleB.image = pygame.transform.scale(paddleB.image, (paddleB.rect.width, paddleB.rect.height))
        paddleA.height, paddleB.height = self.settings.paddle_height_a, self.settings.paddle_height_b


# Dictionary of PowerUps and their probabilities
PowerUps: dict = {0: ShrinkEnlarge, 1: Freeze, 2: MultipleBalls, 3: FasterPaddle, 4: DoubleScore, 5: Shield}
