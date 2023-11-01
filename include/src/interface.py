import os, sys, main, pygame.mixer
from .config import *
from .pong import PongVerse


class Interface:
    """
    The Interface class displays the game interface and handles events.

    Attributes
    ----------
    settings: GlobalSettings
        An instance of the `GlobalSettings` class that stores the game settings.
    screen: pygame.Display
        Game window with resolution.
    clock: pygame.Time
        The game clock to set the FPS.
    background_img: pygame.Transform
        The background image.
    default_font: pygame.Font
        The default font used for the game.
    menu_font: pygame.Font
        The font used for the menu options.
    button_width_center: int
        Define the center of the button on the x-axis. (screen)
    button_height_pos: int
        Define the initial position of the button on the y-axis. (screen)
    width_center: int
        Define the center of the screen on the x-axis. (screen)

    Methods
    ----------
    setWindowTitle(title: str) -> None
        Set the title of the game window.

    clickSound(self) -> None
        Used to play the click sound effect.

    drawRect(self, color: tuple, width: float, height: float, default_size: bool) -> pygame.rect
        Draw a rectangle on the game screen for the menu options.

    displayReturnButton(self, mouse_pos: tuple, return_rect: pygame.rect, return_text_rect: pygame.Rect,
                            return_text: pygame.surface.Surface) -> None
        Used to display a return button on Settings and Creators game screen.

    setTitle(self, title: str) -> tuple[pygame.font, pygame.Rect]
        Set the title of each screen of the game.

    mainProgramLoop(self, main_loop: int, return_rect: pygame.rect) -> tuple[int, tuple]
        Runs the main loop of the program, it allows to quit the loop and the game.

    getResolutionDict(self) -> list
        Get the resolution dictionary.

    mainMenu(self) -> None
        Loads the main menu for the pong game. It shows the game title, the game logo, and the game options.

    creatorsScreen(self) -> None
        Loads the creators screen for the pong game. It shows the game creators and the game credits.

    settingsScreen(self) -> None
        Loads the settings menu for the pong game. The user can change game resolution, and turn on/off the sound.

    """

    def __init__(self, settings: GlobalSettings):
        """
        Initialize the game interface and its respective settings.

        Parameters
        ----------
        settings : GlobalSettings
            An instance of the GlobalSettings class containing the game settings.
        """

        pygame.init(), pygame.mixer.init()  # initialize pygame and pygame mixer
        self.settings: GlobalSettings = settings  # Settings for the game
        if self.settings.music_on:  # Music and Sound Effects
            pygame.mixer.music.load('sound/main_theme.mp3')
            pygame.mixer.music.play(-1)
        self.screen: pygame.display = pygame.display.set_mode(settings.resolution)  # Set the screen
        self.clock: pygame.time = pygame.time.Clock()  # Set the clock
        icon: pygame.image = pygame.image.load("img/icons/main_icon.png").convert_alpha()  # Load the icon
        pygame.display.set_icon(icon)  # Set the icon
        background_img_load: pygame.image = pygame.image.load(
            "img/background/background_interface.jpg").convert()  # Load the background image
        self.background_img: pygame.transform = pygame.transform.scale(background_img_load, (self.settings.width,
                                                                                             self.settings.height))  # Set the background image
        self.default_font = pygame.font.Font(settings.FONT_TYPE_DEFAULT,
                                             settings.font_size_default)  # Set the default font
        self.menu_font = pygame.font.Font(settings.FONT_TYPE_MENU,
                                          settings.subtitle_size)  # Set the font for the menu options
        self.button_width_center: int = int(
            self.settings.width * 0.5 - settings.button_width * 0.5)  # Set the button width center
        self.button_height_pos: int = int(self.settings.height * 0.3)  # Set the button height position
        self.width_center: int = int(self.settings.width / 2)  # Set the width center

    @staticmethod
    def setWindowTitle(title: str) -> None:  # Set the window title
        """
        Set the title of the game window.

        Return
        ----------
        None
        """

        pygame.display.set_caption(title)

    # Click sound activation
    def clickSound(self) -> None:
        """
        Used to play the click sound effect.

        Parameters
        ----------
        self : Interface
            The interface object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        if self.settings.music_on:
            pygame.mixer.Sound('sound/click_sound.wav').play()

    # Draw a rectangle with the specified color and position
    def drawRect(self, color: tuple, width: float, height: float, default_size: bool) -> pygame.rect:
        """
        Draw a rectangle on the game screen for the menu options.

        Parameters
        ----------
        color : tuple
            The color of the rectangle in an RGB tuple.
        width : float
            The width of the rectangle.
        height : float
            The height of the rectangle.
        default_size : bool
            Check if user wants to use the button with its default size or with a smaller size.

        Return
        ----------
        pygame.draw.rect : pygame.Rect
            The rectangle object.
        """

        if default_size:  # If the size is the default size
            return pygame.draw.rect(self.screen, color,
                                    [width, height, self.settings.button_width, self.settings.button_height],
                                    border_radius=15)
        else:  # If the size is not the default size
            return pygame.draw.rect(self.screen, color,
                                    [width, height, self.settings.small_button_width,
                                     self.settings.small_button_height],
                                    border_radius=15)

    # Display Return Button
    def displayReturnButton(self, mouse_pos: tuple, return_rect: pygame.rect, return_text_rect: pygame.rect,
                            return_text: pygame.surface.Surface) -> None:
        """
        Used to display a return button on Settings and Creators game screen.

        Parameters
        ----------
        self : Interface
            The interface object containing the class attributes and game settings.
        mouse_pos : tuple
            Current mouse position as a tuple of integers representing the x and y coordinates.
        return_rect : pygame.Rect
            The rectangular region that surrounds the return button.
        return_text_rect : pygame.Rect
            The rectangular region that surrounds the return text.
        return_text : pygame.Surface
            The text that will be displayed on the return button.

        Return
        ----------
        None
        """

        if return_rect.collidepoint(mouse_pos):  # If the mouse is over the return button
            self.drawRect(self.settings.RED, self.settings.width * 0.85,
                          self.settings.height * 0.88, False)
        else:  # If the mouse is not over the return button
            self.drawRect(self.settings.GRAY, self.settings.width * 0.85,
                          self.settings.height * 0.88, False)
        self.screen.blit(return_text,
                         (self.settings.width - return_rect.width - return_text_rect.center[0],
                          self.settings.height * 0.885))  # Display the return button text

    def setTitle(self, title: str) -> tuple[pygame.font, pygame.rect]:  # Set the title
        """
        Set the title of each screen of the game.

        Parameters
        ----------
        self : Interface
            The interface object containing the class attributes and game settings.
        title : str
            The title of the screen.

        Return
        ----------
        title_text : pygame.font.Font.render
            The title text object.
        title_text_rect : pygame.Rect
            The rectangular region that surrounds the title text, used to center the text.
        """

        text_title = self.default_font.render(title, True, self.settings.RED)  # Set the title text
        title_rect = text_title.get_rect()  # Get the text rectangle
        return text_title, title_rect

    def mainProgramLoop(self, main_loop: int, return_rect: pygame.rect) -> tuple[int, tuple]:  # Main program loop
        """
        Runs the main loop of the program, it allows to quit the loop and the game.

        Parameters
        ----------
        self : Interface
            The interface object containing the class attributes and game settings.
        main_loop : int
            The main loop of the program indicates if the loop should continue to run.
        return_rect : pygame.Rect
            The rectangular region representing the return button.

        Return
        ----------
        main_loop : int
            The main loop of the program indicates if the loop should continue to run.
        mouse_pos : tuple
            The current position of the mouse as a tuple with x and y coordinates.
        """

        mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        if pygame.event.get(pygame.QUIT):  # If the user clicks the close button
            pygame.quit(), sys.exit()
        if return_rect.collidepoint(mouse_pos) and pygame.event.get(
                pygame.MOUSEBUTTONDOWN):  # If the user clicks the return button
            self.clickSound()
            main_loop = 0 and self.mainMenu()  # Return to the main menu
        return main_loop, mouse_pos

    def getResolutionDict(self) -> list:  # Get the resolution dictionary
        """
        Get the resolution dictionary.

        Parameters
        ----------
        self : Interface
            The interface object containing the class attributes and game settings.

        Return
        ----------
        resolution_rect_list : list
            A list of tuples with the text of the selected resolution, a text rectangle, button rectangle,
            the height position, and a tuple with selected resolution.
        """

        resolution_rect_list = []  # List of resolution rectangles
        resolution_pos_height = self.settings.height * 0.18  # Set the resolution height position
        for resolution_name, resolution in Screen_Resolution.items():
            resolution_pos_height += self.settings.button_gap
            resolution_text = self.menu_font.render(resolution_name, True, self.settings.WHITE)
            resolution_text_rect = resolution_text.get_rect()
            resolution_rect = self.drawRect(self.settings.GRAY, self.button_width_center,
                                            resolution_pos_height, True)
            resolution_rect_list.append(
                (resolution_text, resolution_text_rect, resolution_rect, resolution_pos_height,
                 resolution))  # Add the resolution to the list
        return resolution_rect_list

    # Screen (Main Menu)
    def mainMenu(self) -> None:  # Main menu
        """
        Loads the main menu for the pong game. It shows the game title, the game logo, and the game options.

        Parameters
        ----------
        self : Interface
            The interface object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        # Loop that carries on until the user exits the game
        mainMenuOn: int = 1

        # Create text-labels and get their rectangle
        text_title, title_rect = self.setTitle('The PongVerse - OOP PyGame')  # Set the title

        # PongVerse
        text_play_pongVerse = self.menu_font.render('The PongVerse', True, self.settings.WHITE)
        play_pong_rect = text_play_pongVerse.get_rect()
        play_pongVerse_rect = self.drawRect(self.settings.GRAY, self.button_width_center, self.button_height_pos, True)

        # PongVerse Vanilla Edition
        text_play_pongVerse_vanilla = self.menu_font.render('PongVerse - Vanilla', True, self.settings.WHITE)
        play_pong_vanilla_rect = text_play_pongVerse_vanilla.get_rect()
        play_pongVerse_vanilla_rect = self.drawRect(self.settings.GRAY, self.button_width_center,
                                                    self.button_height_pos + self.settings.button_gap, True)
        # Settings
        text_settings = self.menu_font.render('Settings', True, self.settings.WHITE)
        settings_text_rect = text_settings.get_rect()
        settings_rect = self.drawRect(self.settings.GRAY, self.button_width_center,
                                      self.button_height_pos + self.settings.button_gap * 2, True)
        # Creators
        text_creators = self.menu_font.render('Creators', True, self.settings.WHITE)
        creators_text_rect = text_creators.get_rect()
        creators_rect = self.drawRect(self.settings.GRAY, self.button_width_center,
                                      self.button_height_pos + self.settings.button_gap * 3, True)
        # Quit
        text_quit = self.menu_font.render('Quit', True, self.settings.WHITE)
        quit_text_rect = text_quit.get_rect()
        quit_rect = self.drawRect(self.settings.GRAY, self.button_width_center,
                                  self.button_height_pos + self.settings.button_gap * 4, True)

        # -------- Main Program Loop -----------
        while mainMenuOn:
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position

            if pygame.event.get(pygame.QUIT):  # press on exit button
                pygame.quit(), sys.exit()
            if pygame.event.get(pygame.MOUSEBUTTONDOWN):  # press on mouse button
                if play_pongVerse_rect.collidepoint(mouse_pos):  # Mouse click on Pong button
                    self.clickSound(), PongVerse(vanilla=False, settings=self.settings).instructions()
                elif play_pongVerse_vanilla_rect.collidepoint(mouse_pos):  # Mouse click on Vanilla Pong button
                    self.clickSound(), PongVerse(vanilla=True, settings=self.settings).instructions()
                elif settings_rect.collidepoint(mouse_pos):  # Mouse click on Settings button
                    self.clickSound(), self.settingsScreen()
                elif creators_rect.collidepoint(mouse_pos):  # Mouse click on Creators button
                    self.clickSound(), self.creatorsScreen()
                elif quit_rect.collidepoint(mouse_pos):  # Mouse click on quit button
                    self.clickSound(), pygame.quit(), sys.exit()

            # --- Main Menu logic starts here

            self.setWindowTitle(self.settings.MENU_TITLE)  # Set the title of the window
            self.screen.blit(self.background_img, (0, 0))  # Display the background image

            # Display the title of the game
            self.screen.blit(text_title, (
                self.settings.width / 2 - title_rect.center[0],
                self.settings.height * 0.05))

            # On Hover, button changes color
            # Play PongVerse Button
            if play_pongVerse_rect.collidepoint(mouse_pos):
                self.drawRect(self.settings.BLUE, self.button_width_center, self.button_height_pos, True)
            else:
                self.drawRect(self.settings.GRAY, self.button_width_center, self.button_height_pos, True)
            self.screen.blit(text_play_pongVerse,
                             (self.width_center - play_pong_rect.center[0],
                              self.button_height_pos + self.settings.button_gap * 0.05))
            # Play PongVerse Vanilla Edition Button
            if play_pongVerse_vanilla_rect.collidepoint(mouse_pos):
                self.drawRect(self.settings.BLUE, self.button_width_center,
                              self.button_height_pos + self.settings.button_gap, True)
            else:
                self.drawRect(self.settings.GRAY, self.button_width_center,
                              self.button_height_pos + self.settings.button_gap, True)
            self.screen.blit(text_play_pongVerse_vanilla,
                             (self.width_center - play_pong_vanilla_rect.center[0],
                              self.button_height_pos + self.settings.button_gap * 1.05))

            # Enter Settings Button
            if settings_rect.collidepoint(mouse_pos):
                self.drawRect(self.settings.BLUE, self.button_width_center,
                              self.button_height_pos + self.settings.button_gap * 2, True)
            else:
                self.drawRect(self.settings.GRAY, self.button_width_center,
                              self.button_height_pos + self.settings.button_gap * 2, True)
            self.screen.blit(text_settings,
                             (self.width_center - settings_text_rect.center[0],
                              self.button_height_pos + self.settings.button_gap * 2.05))

            # Enter Creators Button
            if creators_rect.collidepoint(mouse_pos):
                self.drawRect(self.settings.BLUE, self.button_width_center,
                              self.button_height_pos + self.settings.button_gap * 3, True)
            else:
                self.drawRect(self.settings.GRAY, self.button_width_center,
                              self.button_height_pos + self.settings.button_gap * 3, True)
            self.screen.blit(text_creators,
                             (self.width_center - creators_text_rect.center[0],
                              self.button_height_pos + self.settings.button_gap * 3.05))

            # Quit Button
            if quit_rect.collidepoint(mouse_pos):
                self.drawRect(self.settings.RED, self.button_width_center,
                              self.button_height_pos + self.settings.button_gap * 4, True)
            else:
                self.drawRect(self.settings.GRAY, self.button_width_center,
                              self.button_height_pos + self.settings.button_gap * 4, True)
            self.screen.blit(text_quit,
                             (self.width_center - quit_text_rect.center[0],
                              self.button_height_pos + self.settings.button_gap * 4.05))

            # --- Update the screen with what was drawn
            pygame.display.update()

            # --- Limit the game to 30 frames per second
            self.clock.tick(30)

    # Screen (Creators)
    def creatorsScreen(self) -> None:  # Display the Creators Screen
        """
        Loads the creators menu for the pong game. It shows the creators of the game and, the university.

        Parameters
        ----------
        self : Interface
            The interface object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        # Loop that carries on until the user exits the main menu
        creatorsON: int = 1

        creators_body_font = pygame.font.Font(self.settings.FONT_TYPE_MENU, self.settings.subtitle_size)  # Body font
        nova_text_font = pygame.font.Font(self.settings.FONT_TYPE_MENU, self.settings.body_size)  # Nova text font

        name_height_pos: int = int(self.settings.height * 0.35)  # Position of the first name

        creator_icon_rect = self.settings.creator_1_img_load.get_rect()  # Get the rect of the icons
        left_icon_alignment = self.settings.width * 0.07  # Left alignment of the icons
        right_icon_alignment = self.settings.width * 0.93 - creator_icon_rect.width  # Right alignment of the icons
        top_icon_alignment = self.settings.height * 0.25  # Top alignment of the icons
        bottom_icon_alignment = self.settings.height * 0.75 - creator_icon_rect.height  # Bottom alignment of the icons

        # Create text-labels and get their rectangle
        text_title, title_rect = self.setTitle('Our Team of Creators')  # Title

        # Body
        professors_text = nova_text_font.render('Base code provided by our well Respected Professors', True,
                                                self.settings.WHITE)  # Professors text
        professors_text_rect = professors_text.get_rect()  # Professors text rectangle

        # Creators text
        creator_1 = creators_body_font.render('Leonor Costa | 20211649@novaims.unl.pt', True, self.settings.WHITE)
        creator_1_rect = creator_1.get_rect()  # Creator 1 rectangle
        creator_2 = creators_body_font.render('Osmáiny Raimundo | e20191506@novaims.unl.pt', True, self.settings.WHITE)
        creator_2_rect = creator_2.get_rect()  # Creator 2 rectangle
        creator_3 = creators_body_font.render('Sara Lyra | 20211565@novaims.unl.pt', True, self.settings.WHITE)
        creator_3_rect = creator_3.get_rect()  # Creator 3 rectangle
        creator_4 = creators_body_font.render('Tiago Valente | 20211650@novaims.unl.pt', True, self.settings.WHITE)
        creator_4_rect = creator_4.get_rect()  # Creator 4 rectangle

        return_text = self.menu_font.render('Return', True, self.settings.WHITE)  # Return text
        return_text_rect = return_text.get_rect()  # Return text rectangle
        return_rect = self.drawRect(self.settings.GRAY, self.settings.width * 0.85,
                                    self.settings.height * 0.88, False)  # Return rectangle

        novaims_text = nova_text_font.render('NovaIMS - Information Management School', True,
                                             self.settings.WHITE)  # NovaIMS text

        # -------- Main Program Loop -----------
        while creatorsON:
            creatorsON, mouse_pos = self.mainProgramLoop(creatorsON, return_rect)

            # --- Creators screen logic starts here

            self.setWindowTitle(self.settings.CREDITS_TITLE)  # Title of the window
            self.screen.blit(self.background_img, (0, 0))  # Display background image

            # Display Title text
            self.screen.blit(text_title, (
                self.settings.width / 2 - title_rect.center[0],
                self.settings.height * 0.05))

            # Display Professors text
            self.screen.blit(professors_text, (self.settings.width / 2 - professors_text_rect.center[0],
                                               self.settings.height * 0.17))

            # Display Creators text
            self.screen.blit(creator_1, (self.width_center - creator_1_rect.center[0], name_height_pos))  # Creator 1
            self.screen.blit(creator_2, (
                self.width_center - creator_2_rect.center[0],
                name_height_pos + self.settings.button_gap * 0.75))  # Creator 2
            self.screen.blit(creator_3, (
                self.width_center - creator_3_rect.center[0],
                name_height_pos + self.settings.button_gap * 1.5))  # Creator 3
            self.screen.blit(creator_4, (
                self.width_center - creator_4_rect.center[0],
                name_height_pos + self.settings.button_gap * 2.25))  # Creator 4

            # Display Creators Icons
            # Creator 1
            self.screen.blit(self.settings.creator_1_img_load, (left_icon_alignment, top_icon_alignment))  # Left top
            # Creator 2
            self.screen.blit(self.settings.creator_2_img_load,
                             (left_icon_alignment, bottom_icon_alignment))  # Left bottom
            # Creator 3
            self.screen.blit(self.settings.creator_3_img_load, (right_icon_alignment, top_icon_alignment))  # Right top
            # Creator 4
            self.screen.blit(self.settings.creator_4_img_load,
                             (right_icon_alignment, bottom_icon_alignment))  # Right bottom
            # Display Return button
            self.displayReturnButton(mouse_pos, return_rect, return_text_rect, return_text)  # Display return button

            # Display NovaIMS text and Icon
            novaims_img_rect = self.settings.novaims_img_load.get_rect()
            self.screen.blit(self.settings.novaims_img_load.convert_alpha(), (
                self.settings.width * 0.03,
                self.settings.height * 0.97 - novaims_img_rect.height))
            self.screen.blit(novaims_text, (self.settings.width * 0.03 + novaims_img_rect.width,
                                            self.settings.height * 1.04 - novaims_img_rect.height))

            # --- Update the screen with what was drawn
            pygame.display.update()

            # --- Limit the game to 30 frames per second
            self.clock.tick(30)

    # Screen (Settings)
    def settingsScreen(self) -> None:  # Settings screen
        """
        Loads the settings menu for the pong game. The user can change game resolution, and turn on/off the sound.

        Parameters
        ----------
        self : Interface
            The interface object containing the class attributes and game settings.

        Return
        ----------
        None
        """

        # Loop that carries on until the user exits the main menu
        settingsOn: int = 1

        # Create text-labels and get their rectangle
        text_title, title_rect = self.setTitle('Settings')  # Title

        # Return text
        return_text = self.menu_font.render('Return', True, self.settings.WHITE)
        return_text_rect = return_text.get_rect()
        return_rect = self.drawRect(self.settings.GRAY, self.settings.width * 0.85,
                                    self.settings.height * 0.88, False)

        # Sound On/Off text
        sound_text = self.menu_font.render('On/Off', True, self.settings.WHITE)
        sound_text_rect = return_text.get_rect()
        sound_rect = self.drawRect(self.settings.GRAY, self.settings.width * 0.04,
                                   self.settings.height * 0.88, False)

        resolutions_rect_list = self.getResolutionDict()  # Get the list of resolutions

        # -------- Main Program Loop -----------
        while settingsOn:
            settingsOn, mouse_pos = self.mainProgramLoop(settingsOn, return_rect)

            # --- Settings screen logic starts here

            self.screen.blit(self.background_img, (0, 0))  # Display Background image
            self.setWindowTitle(self.settings.SETTINGS_TITLE)  # Set the title of the window
            self.screen.blit(text_title, (
                self.settings.width / 2 - title_rect.center[0],
                self.settings.height * 0.05))  # Display Title text

            # Display Resolution buttons
            for screen_resolution_text, screen_resolution_text_rect, \
                    screen_resolution_rect, screen_resolution_pos_height, screen_resolution in resolutions_rect_list:
                if screen_resolution_rect.collidepoint(mouse_pos):
                    self.drawRect(self.settings.BLUE, self.button_width_center, screen_resolution_pos_height, True)
                    if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                        self.clickSound()  # Play click sound
                        sys.argv = [sys.argv[0], int(screen_resolution[0]), int(screen_resolution[1]),
                                    self.settings.music_on]  # Set new resolution
                        os.execv(main.main(), sys.argv)  # Restart the game with new resolution
                else:
                    self.drawRect(self.settings.GRAY, self.button_width_center, screen_resolution_pos_height, True)
                self.screen.blit(screen_resolution_text, (
                    self.width_center - screen_resolution_text_rect.center[0],
                    screen_resolution_pos_height + self.settings.button_gap * 0.05))

            # Display Sound On/Off icon
            self.screen.blit(self.settings.sound_on_img_load.convert_alpha(),
                             (sound_rect.width * 1.5, self.settings.height * 0.885))

            # Display Sound On/Off button
            if sound_rect.collidepoint(mouse_pos):  # If mouse is over the button
                self.drawRect(self.settings.BLUE, self.settings.width * 0.04, self.settings.height * 0.88, False)
                if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                    if self.settings.music_on:
                        pygame.mixer.music.pause()  # Pause music
                        pygame.mixer.stop()  # Stop music
                        self.settings.music_on = False  # Set music_on to False
                    else:
                        pygame.mixer.music.unpause()  # Unpause music
                        self.settings.music_on = True  # Set music_on to True
            else:
                self.drawRect(self.settings.GRAY, self.settings.width * 0.04, self.settings.height * 0.88, False)
            self.screen.blit(sound_text,
                             (sound_rect.center[0] - sound_text_rect.center[0], self.settings.height * 0.885))

            self.displayReturnButton(mouse_pos, return_rect, return_text_rect, return_text)  # Display Return button

            # --- Update the screen with what was drawn
            pygame.display.update()

            # --- Limit the game to 30 frames per second
            self.clock.tick(30)
