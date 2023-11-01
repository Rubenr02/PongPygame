import sys
from random import choices
from .ball import Ball
from .powerups import *
from .config import *


# Class Pong represents the game
class PongVerse:
    """
    PongVerse class represents the game itself controls instructions, play, and win screens.

    Attributes
    ----------
    settings: GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    vanilla: bool
        Defines the existence or non-existence of power-ups.
    powerup_visible: Powerup (or None)
        Variable to store the visible powerup.
    powerup_active: Powerup (or None)
        Variable to store the active powerup.
    powerup_visible_time: pygame.Time
        Variable to store the visible powerup time.
    powerup_active_time: pygame.Time
        Variable to store the active powerup time.
    all_sprites_list: pygame.sprite.Group
        List of all sprites in the game.
    additional_balls: list[Ball]
        List of additional balls.
    ball_owner: str (or None)
        Variable to store the ball owner.
    powerup_owner: str (or None)
        Variable to store the powerup owner. (Only used in MultipleBalls)
    screen: pygame.Surface
        The game screen.
    default_font: pygame.Font
        The default font for the game.
    powerup_font: pygame.Font
        The font for the powerup text.
    small_powerup_font: pygame.Font
        The font for the small powerup text.
    clock: pygame.Clock
        The clock that controls the FPS and timers.
    scoreA: int
        Player A score.
    scoreB: int
        Player B score.
    triggered: bool
        Indicates if the ball has been triggered to move.
    random_second: int
        Random second used to spawn powerups.

    Methods
    ----------
    displayWinConditionInstructions(self, body_font: pygame.font, subtitle_font: pygame.Font,
                                        left_x_alignment: float) -> None
        Displays the win condition instructions.

    displayPowerupsInstructions(self, body_font: pygame.font, small_body_font: pygame.Font,
                                    subtitle_font: pygame.font) -> None
        Displays the powerups instructions with active time and description.

    displayPlayerKeysInstructions(self, body_font: pygame.font, subtitle_font: pygame.Font,
                                      left_x_alignment: float) -> None
        Displays the player keys (keyboard) instructions for each Paddle/Player.

    instructions(self) -> None
        Displays the instructions screen for the game.

    pressedKeys(self, keys: pygame.key, paddleA: Paddle, paddleB: Paddle) -> None
        Defines the keys used to move the paddles.

    setPowerupVisible(self, timer: pygame.time) -> None
        Sets the powerup visible if there is no active powerup but a ball owner and timer has reached a certain second.

    setPowerupInvisible(self) -> None
        Sets the powerup icon invisible after 5 seconds.

    setPowerupActive(self, paddleA: Paddle, paddleB: Paddle) -> None
        Sets the powerup active if a ball collided with an icon and has owner.

    setPowerupInactive(self, paddleA: Paddle, paddleB: Paddle) -> None
        Sets the powerup inactive if the active time has reached the powerup's active time.

    handleVisiblePowerup(self, ball: Ball, paddleA: Paddle, paddleB: Paddle) -> None
        Handles the visible powerup icon if there is one and checks if it collides with the ball.

    handleActivePowerup(self, paddleA: Paddle, paddleB: Paddle) -> None
        Handles the active powerup if there is one, also shows powerup name and description.

    handleMultipleBalls(self, paddleA: Paddle, paddleB: Paddle) -> None
        Handles the additional balls if there are any.

    displayScores(self) -> None
        Displays the scores of the players.

    setStaticElements(self, background_img: pygame.image, playerA_icon: pygame.transform,
                          playerB_icon: pygame.transform) -> None
        Sets the static elements of the game and shows them, background and players' icons.

    instanceNewBall(self) -> Ball
        Creates a new ball and returns it.

    powerupActivatedSound(self) -> None
        Plays a sound when a powerup is activated.

    winnerSound(self) -> None
        Plays a sound when a player wins.

    play(self) -> None
        Starts the game and manages everything since paddles, ball to powerups.

    winnerScreen(self) -> None
        Displays the winner screen.

    """

    def __init__(self, vanilla: bool, settings: GlobalSettings):
        """
        Initialize the game PongVerse, Instructions and WinScreen and their respective settings.

        Parameters
        ----------
        vanilla: bool
            Defines the existence or non-existence of power-ups.
        settings : GlobalSettings
            An instance of the GlobalSettings class containing the game settings.
        """

        self.settings: GlobalSettings = settings  # Load game settings
        self.vanilla: bool = vanilla  # Set game version
        self.powerup_visible: any = None  # Variable to store the visible powerup
        self.powerup_active: any = None  # Variable to store the active powerup
        self.powerup_visible_time: pygame.time = None  # Variable to store the visible powerup time
        self.powerup_active_time: pygame.time = None  # Variable to store the active powerup time
        self.all_sprites_list = pygame.sprite.Group()  # List of all sprites in the game
        self.additional_balls: list[Ball] = []  # List of additional balls
        self.ball_owner: any = None  # Variable to store the ball owner
        self.powerup_owner: any = None  # Variable to store the powerup owner
        self.screen = pygame.display.set_mode(settings.resolution)  # Set the screen resolution
        self.default_font = pygame.font.Font(settings.FONT_TYPE_DEFAULT,
                                             settings.font_size_default)  # Set the default font
        self.powerup_font = pygame.font.Font(settings.FONT_TYPE_DEFAULT,
                                             settings.font_size_powerup)  # Set the PowerUp font
        self.small_powerup_font = pygame.font.Font(settings.FONT_TYPE_MENU,
                                                   settings.font_size_small_powerup)  # Set the small PowerUp font
        self.clock = pygame.time.Clock()  # Create a clock that controls FPS
        self.scoreA: int = 0  # Player A score
        self.scoreB: int = 0  # Player B score
        self.triggered: bool = False  # Trigger is set to True when a player scores a point
        self.random_second: int = randint(10, 15)  # Create a random number to display the powerup icon

    # Display win condition (Instructions)
    def displayWinConditionInstructions(self, body_font: pygame.font, subtitle_font: pygame.font,
                                        left_x_alignment: float) -> None:
        """
        Displays the win condition instructions.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        body_font: pygame.Font
            The font for the body text.
        subtitle_font: pygame.Font
            The font for the subtitle text.
        left_x_alignment: float
            The left x alignment of the text.

        Return
        ----------
        None
        """

        # Display the win condition subtitle
        win_condition_title = subtitle_font.render('Win Condition', True, self.settings.LIGHT_BLUE)
        self.screen.blit(win_condition_title,
                         (left_x_alignment, self.settings.height * 0.6))
        # Display the win condition text
        win_condition_body = body_font.render(f'First player to hit {self.settings.WIN_SCORE} points wins!', True,
                                              self.settings.WHITE)
        self.screen.blit(win_condition_body,
                         (left_x_alignment, self.settings.height * 0.67))

    # Display powerups (Instructions)
    def displayPowerupsInstructions(self, body_font: pygame.font, small_body_font: pygame.font,
                                    subtitle_font: pygame.font) -> None:
        """
        Displays the powerups instructions with active time and description.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        body_font: pygame.Font
            The font for the body text.
        small_body_font: pygame.Font
            The font for the small body text.
        subtitle_font: pygame.Font
            The font for the subtitle text.

        Return
        ----------
        None
        """

        # Check if the game is not vanilla
        if not self.vanilla:
            # Display the powerups subtitle
            powerup_class_title = subtitle_font.render('Powerups', True, self.settings.LIGHT_BLUE)
            self.screen.blit(powerup_class_title,
                             (self.settings.right_x_alignment, self.settings.height * 0.2))
            # Check the powerups dictionary
            for powerup in PowerUps.values():
                # Get icon, name, description and active time for each powerup
                powerup_icon = pygame.transform.smoothscale(pygame.image.load(powerup.icon),
                                                            (self.settings.powerup_width,
                                                             self.settings.powerup_height))
                powerup_name = subtitle_font.render(powerup.name, True, self.settings.GOLDEN)
                powerup_description = body_font.render(powerup.description, True, self.settings.WHITE)
                powerup_active_time = small_body_font.render(f"{powerup.active_time} seconds active", True,
                                                             self.settings.LIGHT_BLUE)
                # Powerup icon position
                icon_pos = self.settings.powerup_icon_pos_list[powerup.name]
                # Display the powerup icon
                self.screen.blit(powerup_icon, icon_pos)
                # Display the powerup name
                self.screen.blit(powerup_name, [icon_pos[0] + self.settings.powerup_width * 1.1,
                                                icon_pos[1]])
                # Display the powerup description
                self.screen.blit(powerup_description,
                                 [icon_pos[0] + self.settings.powerup_width * 1.1,
                                  icon_pos[1] + self.settings.powerup_width * 0.45])
                # Display the powerup active time
                self.screen.blit(powerup_active_time,
                                 [icon_pos[0] + self.settings.powerup_width * 1.4,
                                  icon_pos[1] + self.settings.powerup_width * 0.8])

    # Display player keys (Instructions)
    def displayPlayerKeysInstructions(self, body_font: pygame.font, subtitle_font: pygame.font,
                                      left_x_alignment: float) -> None:
        """
        Displays the player keys (keyboard) instructions for each Paddle/Player.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        body_font: pygame.Font
            The font for the body text.
        subtitle_font: pygame.Font
            The font for the subtitle text.
        left_x_alignment: float
            The left x alignment of the text.

        Return
        ----------
        None
        """

        # Display the player keys subtitle
        player_keys_title = subtitle_font.render('Player keys', True, self.settings.LIGHT_BLUE)
        self.screen.blit(player_keys_title,
                         (left_x_alignment, self.settings.height * 0.2))

        # Display the player A keys text
        playerA_keys = body_font.render('Player A - Captain America', True, self.settings.WHITE)
        self.screen.blit(playerA_keys,
                         (left_x_alignment, self.settings.height * 0.27))
        # Display the player A key icons
        self.screen.blit(self.settings.player_a_up.convert_alpha(),
                         (left_x_alignment, self.settings.height * 0.32))
        self.screen.blit(self.settings.player_a_down.convert_alpha(),
                         (left_x_alignment + self.settings.width / 22,
                          self.settings.height * 0.32))

        # Display the player B keys text
        playerB_keys = body_font.render('Player B - Iron Man', True, self.settings.WHITE)
        self.screen.blit(playerB_keys,
                         (left_x_alignment, self.settings.height * 0.42))
        # Display the player B key icons
        self.screen.blit(self.settings.player_b_up.convert_alpha(),
                         (left_x_alignment, self.settings.height * 0.47))
        self.screen.blit(self.settings.player_b_down.convert_alpha(),
                         (left_x_alignment + self.settings.width / 22,
                          self.settings.height * 0.47))

    # Screen (Instructions)
    def instructions(self) -> None:
        """
        Displays the instructions screen for the game.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        # Loop that carries on until the user exits the instructions screen
        instructionsON: int = 1

        # Instructions Fonts
        title_font: pygame.font = pygame.font.Font(self.settings.FONT_TYPE_DEFAULT, self.settings.title_size)
        subtitle_font: pygame.font = pygame.font.Font(self.settings.FONT_TYPE_DEFAULT,
                                                      self.settings.subtitle_size)
        body_font: pygame.font = pygame.font.Font(self.settings.FONT_TYPE_MENU, self.settings.body_size)
        small_body_font: pygame.font = pygame.font.Font(self.settings.FONT_TYPE_MENU,
                                                        self.settings.small_body_size)

        # -------- Main Program Loop -----------
        while instructionsON:

            # --- Main event loop
            for event in pygame.event.get():

                # User clicked close
                if event.type == pygame.QUIT:
                    pygame.quit(), sys.exit()  # Close the window and quit

                # Or they used the keyboard
                if event.type == pygame.KEYDOWN:
                    # Pressing the Space key will start the game
                    if event.key == pygame.K_SPACE:
                        # Quit the loop
                        instructionsON = 0
                        # Start the game
                        self.play()

                    # Pressing the Escape Key will quit to the main menu
                    if event.key == pygame.K_ESCAPE:
                        # Quit the loop
                        instructionsON = 0

            if self.vanilla:
                # Vanilla Game title
                pygame.display.set_caption(self.settings.INSTRUCTIONS_TITLE_VANILLA)
                title = title_font.render('Instructions - Vanilla Edition', True, self.settings.WHITE)
                left_x_alignment = self.settings.right_x_alignment  # Keys and Text aligned on the right side

            else:
                # Game title
                pygame.display.set_caption(self.settings.INSTRUCTIONS_TITLE)
                title = title_font.render('Instructions', True, self.settings.WHITE)
                left_x_alignment = self.settings.left_x_alignment  # Keys and Text aligned on the left side

            # Background image
            self.screen.blit(self.settings.background_img, (0, 0))
            # Display the title on the screen
            self.screen.blit(title, (self.settings.width * 0.07, self.settings.height * 0.05))

            # Display text to return to the main menu
            self.screen.blit(self.settings.escape_key[0].convert_alpha(), self.settings.escape_key[1])
            return_text = small_body_font.render('To return press', True, self.settings.WHITE)
            # Position the text
            self.screen.blit(return_text,
                             (self.settings.width * 0.87, self.settings.height * 0.05))

            # Call a function to display the instructions for the powerups
            self.displayPowerupsInstructions(body_font, small_body_font, subtitle_font)
            # Call a function to display the player keys
            self.displayPlayerKeysInstructions(body_font, subtitle_font, left_x_alignment)
            # Call a function to display the win condition
            self.displayWinConditionInstructions(body_font, subtitle_font, left_x_alignment)

            # Display text to start the game
            start_game_text = body_font.render("Press SPACE to start the game", True, self.settings.WHITE)
            start_game_text_rect = start_game_text.get_rect()
            # Center that text
            self.screen.blit(start_game_text, (self.settings.width / 2 - start_game_text_rect.center[0],
                                               self.settings.height * 0.9))

            # --- Update the screen with what was drawn
            pygame.display.update()

            # --- Limit the game to 30 frames per second
            self.clock.tick(30)

    # Keys used to move the paddles
    def pressedKeys(self, keys: pygame.key, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Defines the keys used to move the paddles.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        keys : pygame.Key
            The keys pressed by the user.
        paddleA : Paddle
            The paddle controlled by player A.
        paddleB : Paddle
            The paddle controlled by player B.

        Return
        ----------
        None
        """

        # Move the paddles when the user hits W/S (player A) or up/down (player B)
        if keys[pygame.K_w]:
            paddleA.moveUp(self.settings.paddle_speed_a)  # Move the paddle up
            self.triggered = True
        if keys[pygame.K_s]:
            paddleA.moveDown(self.settings.paddle_speed_a, self.settings.height)  # Move the paddle down
            self.triggered = True
        if keys[pygame.K_UP]:
            paddleB.moveUp(self.settings.paddle_speed_b)  # Move the paddle up
            self.triggered = True
        if keys[pygame.K_DOWN]:
            paddleB.moveDown(self.settings.paddle_speed_b, self.settings.height)  # Move the paddle down
            self.triggered = True

    # Set powerup icon to be displayed
    def setPowerupVisible(self, timer: pygame.time) -> None:
        """
        Sets the powerup visible if there is no active powerup but a ball owner and timer has reached a certain second.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        timer : pygame.Time
            The timer used to spawn a powerup icon.

        Return
        ----------
        None
        """

        # Checks if a powerup is invisible and inactive and if there is a ball owner
        if self.powerup_visible is None and self.powerup_active is None and self.ball_owner is not None:
            # List of powerup probabilities
            PowerUps_Probabilities = [val.probability for val in PowerUps.values()]
            if timer % self.random_second == 0:  # If the timer is divisible by the random second
                # Choose a random powerup
                chosen_powerup = choices(PowerUps, PowerUps_Probabilities)[0]
                # Instantiate the powerup
                powerup = chosen_powerup(None, self.settings.powerup_width, self.settings.powerup_height,
                                         self.settings)
                # Powerup added to sprites
                self.all_sprites_list.add(powerup)
                # Powerup icon visible for 5 seconds
                self.powerup_visible, self.powerup_visible_time = powerup, pygame.time.get_ticks()

    # Powerup icon disappears after 5 seconds
    def setPowerupInvisible(self) -> None:
        """
        Sets the powerup icon invisible after 5 seconds.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        self.powerup_visible.kill()  # Erase powerup icon
        self.powerup_visible, self.powerup_visible_time = None, None  # Set powerup icon invisible

    # Powerup is activated
    def setPowerupActive(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Sets the powerup active if a ball collided with an icon and has owner.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        paddleA : Paddle
            The paddle controlled by player A.
        paddleB : Paddle
            The paddle controlled by player B.

        Return
        ----------
        None
        """

        self.powerup_active = self.powerup_visible  # Set powerup active as the powerup visible
        self.powerup_visible.kill()  # Erase powerup icon
        self.powerup_active.owner = self.powerup_owner  # Set the powerup_active ball owner as the powerup owner
        self.powerup_active.run_powerup(paddleA, paddleB)  # Activate powerup
        self.powerup_active_time = pygame.time.get_ticks()  # Set powerup active timer

    # Powerup is deactivated
    def setPowerupInactive(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Sets the powerup inactive if the active time has reached the powerup's active time.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        paddleA : Paddle
            The paddle controlled by player A.
        paddleB : Paddle
            The paddle controlled by player B.

        Return
        ----------
        None
        """

        self.powerup_active.revert_powerup(paddleA, paddleB)  # Revert powerup effect
        self.powerup_active, self.powerup_active_time, self.powerup_owner = None, None, None  # Set powerup inactive

    # Handle visible powerup
    def handleVisiblePowerup(self, ball: Ball, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Handles the visible powerup icon if there is one and checks if it collides with the ball.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        ball : Ball
            The ball object.
        paddleA : Paddle
            The paddle controlled by player A.
        paddleB : Paddle
            The paddle controlled by player B.

        Return
        ----------
        None
        """

        # Check powerup visibility
        if self.powerup_visible_time is not None:
            # Variable to store the time the powerup has been visible
            visible = (pygame.time.get_ticks() - self.powerup_visible_time) / 1000
            # Check if the visible time is not over
            if int(visible) < self.powerup_visible.visible_time:
                # If visible, check if it collides with the ball
                if pygame.sprite.collide_mask(ball,
                                              self.powerup_visible) and self.ball_owner is not None and self.powerup_active is None:
                    self.powerup_owner = self.ball_owner  # Powerup owner (doesn't change when hitting a paddle)
                    self.powerupActivatedSound()  # Play sound
                    self.setPowerupActive(paddleA, paddleB)  # Powerup active
            else:
                self.setPowerupInvisible()  # Powerup invisible (visible time is over)

    # Handle active powerup
    def handleActivePowerup(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Handles the active powerup if there is one, also shows powerup name and description.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        paddleA : Paddle
            The paddle controlled by player A.
        paddleB : Paddle
            The paddle controlled by player B.

        Return
        ----------
        None
        """

        # Check if a powerup is active
        if self.powerup_active_time is not None:
            # Variable to store the time the powerup has been active
            activated = (pygame.time.get_ticks() - self.powerup_active_time) / 1000
            # If powerup name visible time is not over, it displays the name of the powerup
            if int(activated) < self.settings.POWERUP_NAME_VISIBLE_TIME:
                # Display active powerup name
                display_powerup_name = self.powerup_font.render(str(self.powerup_active.name), True,
                                                                self.settings.WHITE)
                # Get powerup name rectangle
                display_powerup_name_rect = display_powerup_name.get_rect()
                self.screen.blit(display_powerup_name, (
                    self.settings.width / 2 - display_powerup_name_rect.center[0],
                    self.settings.height * 0.85))
                # Display active powerup description
                display_powerup_description = self.small_powerup_font.render(str(self.powerup_active.description), True,
                                                                             self.settings.WHITE)
                # Gets the rectangle of the powerup name
                display_powerup_description_rect = display_powerup_description.get_rect()
                self.screen.blit(display_powerup_description, (
                    self.settings.width / 2 - display_powerup_description_rect.center[0],
                    self.settings.height * 0.94))
            # Check if the active time is over
            if int(activated) == self.powerup_active.active_time:
                self.setPowerupInactive(paddleA, paddleB)  # Powerup inactive

    # Handle additional balls
    def handleMultipleBalls(self, paddleA: Paddle, paddleB: Paddle) -> None:
        """
        Handles the additional balls if there are any.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        paddleA : Paddle
            The paddle controlled by player A.
        paddleB : Paddle
            The paddle controlled by player B.

        Return
        ----------
        None
        """

        if self.powerup_active is not None and self.powerup_active.name == MultipleBalls.name:
            self.triggered = True  # avoid triggering and stopping the screen if a ball scores
            if len(self.additional_balls) == 0:  # if there are no additional balls
                ball_count = randint(self.settings.MIN_ADDITIONAL_BALLS, self.settings.MAX_ADDITIONAL_BALLS)
                for i in range(ball_count):  # create a random number of additional balls
                    additional_ball = self.instanceNewBall()  # create a new ball
                    self.all_sprites_list.add(additional_ball)  # add the ball to the sprite list
                    self.additional_balls.append(additional_ball)  # add the ball to the additional balls list
            else:  # if there are additional balls
                for additional_ball in self.additional_balls:
                    additional_ball.handleBallCollision(self.ball_owner, paddleA, paddleB)  # handle ball collisions
                    # handle ball motion
                    self.scoreA, self.scoreB, should_kill = additional_ball.handleMultipleBallsMotion(
                        self.powerup_owner,
                        self.scoreA,
                        self.scoreB)
                    if should_kill:
                        self.additional_balls.remove(additional_ball)  # remove the ball from the additional balls list
                        self.all_sprites_list.remove(additional_ball)  # remove the ball from the sprite list
                if len(self.additional_balls) == 0:  # if there are no additional balls
                    self.setPowerupInactive(paddleA, paddleB)  # deactivate the powerup

    # Manage Scores
    def displayScores(self) -> None:
        """
        Displays the scores of the players.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        color_A, color_B = self.settings.WHITE, self.settings.WHITE

        if self.powerup_active is not None:  # if a powerup is active (Color Red)
            color_A = self.settings.RED
            color_B = self.settings.RED
        elif self.scoreA < self.scoreB:  # if player B is winning (Color Golden)
            color_B = self.settings.GOLDEN
        elif self.scoreA > self.scoreB:  # if player A is winning (Color Blue)
            color_A = self.settings.BLUE

        # Display scores
        text_A = self.default_font.render(str(self.scoreA), False, color_A)
        text_B = self.default_font.render(str(self.scoreB), False, color_B)
        self.screen.blit(text_A, self.settings.pos_score_a)
        self.screen.blit(text_B, self.settings.pos_score_b)

    # Display Static Elements
    def setStaticElements(self, background_img: pygame.image, playerA_icon: pygame.transform,
                          playerB_icon: pygame.transform) -> None:
        """
        Sets the static elements of the game and shows them, background and players' icons.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.
        background_img : pygame.Image
            The background image of the game.
        playerA_icon : pygame.Transform
            The player A icon.
        playerB_icon : pygame.Transform
            The player B icon.

        Return
        ----------
        None
        """

        background: any = pygame.transform.scale(background_img, [self.settings.width,
                                                                  self.settings.height])  # Scale background image
        self.screen.blit(background, (0, 0))  # Display background image
        self.screen.blit(playerA_icon, self.settings.player_a_icon_pos)  # Display player A icon
        self.screen.blit(playerB_icon, self.settings.player_b_icon_pos)  # Display player B icon
        if self.powerup_active is not None:  # if active powerup (Field divider w/ Color Red)
            pygame.draw.line(self.screen, self.settings.RED, self.settings.field_divider_initial_pos,
                             self.settings.field_divider_max_pos, 5)
        else:  # no active powerup (Field divider w/ Color White)
            pygame.draw.line(self.screen, self.settings.WHITE, self.settings.field_divider_initial_pos,
                             self.settings.field_divider_max_pos, 5)

    # Create ball
    def instanceNewBall(self) -> Ball:
        """
        Creates a new ball and returns it.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.

        Return
        ----------
        ball : Ball
            The new ball object.
        """

        ball = Ball("img/icons/ball.png", self.settings.ball_width, self.settings.ball_height, self.settings)  # Ball
        ball.rect.x, ball.rect.y = (self.settings.initial_pos_x, self.settings.initial_pos_y)  # Initial position
        return ball

    # Sound when a Powerup is activated
    def powerupActivatedSound(self) -> None:
        """
        Plays a sound when a powerup is activated.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        if self.settings.music_on:
            pygame.mixer.Sound('sound/powerup_activated_sound.wav').play()

    # Sound when a Player Wins
    def winnerSound(self) -> None:
        """
        Plays a sound when a player wins.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        if self.settings.music_on:
            pygame.mixer.Sound('sound/winner_sound.wav').play()

    # Screen (PlayPong)
    def play(self) -> None:
        """
        Starts the game and manages everything since paddles, ball to powerups.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        paddleA = Paddle(self.settings.BLUE, self.settings.paddle_width_a, self.settings.paddle_height_a,
                         self.settings.PADDLE_ROUND_CORNERS_A)  # Paddle A
        paddleA.rect.x, paddleA.rect.y = (
            self.settings.initial_pos_x_a, self.settings.initial_pos_y_a)  # Initial position
        paddleB = Paddle(self.settings.GOLDEN, self.settings.paddle_width_b, self.settings.paddle_height_b,
                         self.settings.PADDLE_ROUND_CORNERS_B)  # Paddle B
        paddleB.rect.x, paddleB.rect.y = (
            self.settings.initial_pos_x_b, self.settings.initial_pos_y_b)  # Initial position

        ball = self.instanceNewBall()  # Instance a new ball
        self.all_sprites_list.add(paddleA, paddleB, ball)  # Add sprites to the sprite list
        background_img_load = pygame.image.load("img/background/background_pong.jpg").convert()  # Load background image

        # Load and scale Players Icons
        playerA_icon_load: pygame.image = pygame.image.load("img/icons/playerA_icon.png").convert_alpha()
        playerA_icon: any = pygame.transform.scale(playerA_icon_load, self.settings.player_icon_size)
        playerB_icon_load: pygame.image = pygame.image.load("img/icons/playerB_icon.png").convert_alpha()
        playerB_icon: any = pygame.transform.scale(playerB_icon_load, self.settings.player_icon_size)

        # Loop that carries on until the user exits the game
        carryOn: int = 1

        # -------- Main Program Loop -----------
        while carryOn:

            # --- Main event loop
            for event in pygame.event.get():

                # User clicked close
                if event.type == pygame.QUIT:
                    pygame.quit(), sys.exit()  # Exit the program

                    # Or they used the keyboard
                elif event.type == pygame.KEYDOWN:
                    # Pressing the Escape Key will quit to the main menu
                    if event.key == pygame.K_ESCAPE:
                        carryOn = 0  # Exit the loop

                # Player hits the win score
                elif self.scoreA >= self.settings.WIN_SCORE or self.scoreB >= self.settings.WIN_SCORE:
                    # Quit the loop
                    carryOn = 0
                    # Call winner screen
                    self.winnerSound(), self.winnerScreen()

            # --- Game logic starts here

            timer = int(pygame.time.get_ticks() / 1000)  # Create a timer

            if self.vanilla:  # if vanilla mode
                pygame.display.set_caption(self.settings.GAME_TITLE_VANILLA)  # Set title
            else:
                pygame.display.set_caption(self.settings.GAME_TITLE)  # Set title

            keys = pygame.key.get_pressed()  # Get pressed keys
            self.pressedKeys(keys, paddleA, paddleB)  # Pressed keys to move paddles
            self.setStaticElements(background_img_load, playerA_icon, playerB_icon)  # Display static elements
            self.displayScores()  # Display scores
            self.all_sprites_list.update(move=self.triggered)  # Update sprites
            self.ball_owner = ball.handleBallCollision(self.ball_owner, paddleA, paddleB)  # Handle ball collision

            # Handle ball motion
            self.scoreA, self.scoreB, self.ball_owner, self.triggered = ball.handleBallMotion(self.scoreA,
                                                                                              self.scoreB,
                                                                                              self.ball_owner,
                                                                                              self.triggered)

            self.all_sprites_list.draw(self.screen)  # Draw sprites

            if not self.vanilla:  # if not vanilla mode, display powerups
                self.setPowerupVisible(timer)  # Set powerup visible
                self.handleVisiblePowerup(ball, paddleA, paddleB)  # Handle visible powerup
                self.handleActivePowerup(paddleA, paddleB)  # Handle active powerup
                self.handleMultipleBalls(paddleA, paddleB)  # Handle multiple balls

            # --- Update the screen with what was drawn
            pygame.display.update()

            # --- Limit the game to 60 frames per second
            self.clock.tick(60)

    # Screen (Winning)
    def winnerScreen(self) -> None:
        """
        Displays the winner screen.

        Parameters
        ----------
        self : PongVerse
            The PongVerse object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        # Loop that carries on until the user exits the win screen
        winner_screenON: int = 1

        winner: any = None  # Winner
        winner_score: int = 0  # Winner score

        # Background image load and scale for each player
        backgroundA_img_load: pygame.image = pygame.image.load("img/background/background_winA.jpg").convert()
        backgroundA_img: pygame.transform = pygame.transform.scale(backgroundA_img_load,
                                                                   (self.settings.width,
                                                                    self.settings.height))
        backgroundB_img_load: pygame.image = pygame.image.load("img/background/background_winB.jpg").convert()
        backgroundB_img: pygame.transform = pygame.transform.scale(backgroundB_img_load,
                                                                   (self.settings.width,
                                                                    self.settings.height))

        # Icons load and scale for each player
        winnerA_icon_load: pygame.image = pygame.image.load("img/icons/winner_iconA.png").convert_alpha()
        winnerA_icon: pygame.transform = pygame.transform.scale(winnerA_icon_load, self.settings.winner_icon_size)
        winnerA_icon_rect: pygame.rect = winnerA_icon.get_rect()  # Get rect of winnerA icon
        winnerB_icon_load: pygame.image = pygame.image.load("img/icons/winner_iconB.png").convert_alpha()
        winnerB_icon: pygame.transform = pygame.transform.scale(winnerB_icon_load, self.settings.winner_icon_size)
        winnerB_icon_rect: pygame.rect = winnerB_icon.get_rect()  # Get rect of winnerB icon

        # -------- Main Program Loop -----------
        while winner_screenON:

            # --- Main event loop
            for event in pygame.event.get():

                # User clicked close
                if event.type == pygame.QUIT:
                    # Close the window and quit
                    pygame.quit(), sys.exit()

                # Or they used the keyboard
                if event.type == pygame.KEYDOWN:
                    # Pressing the Escape Key will quit to the main menu
                    if event.key == pygame.K_ESCAPE:
                        winner_screenON = 0  # Quit the loop

            if self.scoreA > self.scoreB:  # If player A wins
                winner = "Captain America"
                winner_score = self.scoreA  # Set winner score
                self.screen.blit(backgroundA_img, (0, 0))  # Display background
                self.screen.blit(winnerA_icon,
                                 (self.settings.width * 0.95 - winnerA_icon_rect.width,
                                  self.settings.height * 0.7))  # Display icon

            elif self.scoreA < self.scoreB:  # If player B wins
                winner = 'Iron Man'
                winner_score = self.scoreB  # Set winner score
                self.screen.blit(backgroundB_img, (0, 0))  # Set background
                self.screen.blit(winnerB_icon,
                                 (self.settings.width * 0.95 - winnerB_icon_rect.width,
                                  self.settings.height * 0.7))  # Display icon

            # Display winner text
            winner_text = self.default_font.render(winner + " your team wins!", False, self.settings.WHITE)
            winner_text_rect = winner_text.get_rect()
            winner_score_text = self.powerup_font.render('Congratulations. Your Score : ' + str(winner_score), False,
                                                         self.settings.WHITE)
            winner_score_text_rect = winner_score_text.get_rect()  # Get rect of winner score text
            self.screen.blit(winner_text,
                             ((self.settings.width / 2 - winner_text_rect.center[0]), self.settings.height * 0.17))
            self.screen.blit(winner_score_text, ((self.settings.width / 2 - winner_score_text_rect.center[0]),
                                                 self.settings.height * 0.30))

            # --- Update the screen with what was drawn
            pygame.display.update()

            # --- Limit the game to 30 frames per second
            self.clock.tick(30)
