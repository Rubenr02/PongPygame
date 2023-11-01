import pygame
import sys
#from pong import play_pong
from random import randint

nice_blue = (93, 131, 179)
res = (720, 720)
screen = pygame.display.set_mode(res)
pygame.init()
carryon = True
playmusic = randint(1, 4)
mute = 0
# colours
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
black = (0, 0, 0)

main_font = pygame.font.Font("assets/titulo.otf", 60)
rule_font = pygame.font.Font("assets/titulo.otf", 40)
lines_font = pygame.font.Font("assets/titulo.otf", 20)


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# Creating a function that creates the GUI
def interface():
    global playmusic
    global mute
    pygame.mixer.init()

    title_text = main_font.render('PING PONG 3000', True, white)

    def play_music():
        if playmusic == 1:
            pygame.mixer.music.load(filename='assets/Street Sweeper - Marc Russo.mp3')
            pygame.mixer.music.play()
        elif playmusic == 2:
            pygame.mixer.music.load(filename='assets/Garbage Golf - Douglas Holmquist.mp3')
            pygame.mixer.music.play()
        elif playmusic == 3:
            pygame.mixer.music.load(filename='assets/Night Owl - Kirk Casey.mp3')
            pygame.mixer.music.play()
        elif playmusic == 4:
            pygame.mixer.music.load(filename='assets/City - Douglas Holmquist.mp3')
            pygame.mixer.music.play()
        elif playmusic == 5:
            pygame.mixer.music.stop()

    play_music()
    # interface loop
    while True:
        screen.fill(nice_blue)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        byron_pong = pygame.font.Font("assets/Byron.ttf", 70)
        byron_2 = pygame.font.Font("assets/Byron.ttf", 45)
        byron_3 = pygame.font.Font("assets/Byron.ttf", 30)
        PLAY_BUTTON = Button(image=pygame.image.load("../pong/assets/Play Rect-modified.png"), pos=(360, 250),
                             text_input="PLAY", font=byron_pong, base_color="#000000", hovering_color="White")
        RULES_BUTTON = Button(image=pygame.image.load("../pong/assets/Options Rect-modified.png"), pos=(360, 400),
                              text_input="Rules", font=byron_2, base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("../pong/assets/Quit Rect-modified.png"), pos=(540, 550),
                             text_input="QUIT", font=byron_3, base_color="#000000", hovering_color="White")
        CREDITS_BUTTON = Button(image=pygame.image.load("../pong/assets/Quit Rect-modified.png"), pos=(180, 550),
                                text_input="CREDITS", font=byron_3, base_color="#000000", hovering_color="White")
        NEXT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect-modified.png"), pos=(180, 650),
                             text_input="NEXT MUSIC", font=byron_3, base_color="#000000", hovering_color="White")
        MUTE_BUTTON = Button(image=pygame.image.load("assets/Quit Rect-modified.png"), pos=(540, 650),
                             text_input="MUTE", font=byron_3, base_color="#000000", hovering_color="White")

        for button in [PLAY_BUTTON, RULES_BUTTON, QUIT_BUTTON, CREDITS_BUTTON, NEXT_BUTTON, MUTE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_pong()
                if RULES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rules()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credits_()
                if MUTE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if mute == 0:
                        mute = 1
                        pygame.mixer.music.stop()
                    elif mute == 1:
                        play_music()
                        mute = 0
                if NEXT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if playmusic == 1:
                        playmusic = 2
                    elif playmusic == 2:
                        playmusic = 3
                    elif playmusic == 3:
                        playmusic = 4
                    elif playmusic == 4:
                        playmusic = 1
                    play_music()
        screen.blit(title_text, (100, 55))

        pygame.display.update()


def resume_():
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    byron_3 = pygame.font.Font("assets/Byron.ttf", 30)
    nice_blue = (93, 131, 179)
    title_text = main_font.render('Computation III - Project', True, white)


    while True:
        screen.fill(nice_blue)
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        RESUME_BUTTON = Button(image=pygame.image.load("../pong/assets/Quit Rect-modified.png"), pos=(350, 250),
                               text_input="BACK", font=byron_3, base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("../pong/assets/Quit Rect-modified.png"), pos=(350, 350),
                               text_input="QUIT", font=byron_3, base_color="#d7fcd4", hovering_color="White")

        for button in [RESUME_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    play_pong()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    interface()

        screen.blit(title_text, (80, 15))

        pygame.display.update()


def credits_():
    credits_text = main_font.render('Credits', True, white)

    line1_text = lines_font.render('Davide Farinati, dfarinati@novaims.unl.pt', True, white)
    line2_text = lines_font.render('Ilya Bakurov, ibakurov@novaims.unl.pt', True, white)
    line3_text = lines_font.render('Liah Rosenfeld, lrosenfeld@novaims.unl.pt', True, white)
    byron_3 = pygame.font.Font("assets/Byron.ttf", 30)

    while True:
        screen.fill(nice_blue)
        # credits text
        screen.blit(line1_text, (15, 100))
        screen.blit(line2_text, (15, 125))
        screen.blit(line3_text, (15, 150))
        screen.blit(credits_text, (300, 15))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect-modified.png"), pos=(150, 650),
                             text_input="BACK", font=byron_3, base_color="#000000", hovering_color="White")

        for button in [BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    interface()

        pygame.display.update()


def rules():
    byron_3 = pygame.font.Font("assets/Byron.ttf", 30)
    rules_text = rule_font.render('Welcome to a better pong', True, white)
    rule6 = lines_font.render('Please have your sound on, there are various sound effects.', True, white)
    rule1 = lines_font.render('The game can be played by 2 players', True, white)
    rule2 = lines_font.render('In order to move player 1 you need to use the keys "W" and "S".', True, white)
    rule3 = lines_font.render('In order to move player 2 you need to use the arrows "UP" and "DOWN".', True, white)
    rule4 = lines_font.render('Freeze Power-Up will make you unable to move your paddle for 3 seconds.', True, white)
    rule5 = lines_font.render('Shrink and Enlarge will make your paddle super small or supper large.', True, white)

    while True:
        screen.fill(nice_blue)
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect-modified.png"), pos=(150, 650),
                             text_input="BACK", font=byron_3, base_color="#000000", hovering_color="White")

        screen.blit(rules_text, (100, 15))
        screen.blit(rule1, (15, 100))
        screen.blit(rule2, (15, 125))
        screen.blit(rule3, (15, 150))
        screen.blit(rule4, (15, 175))
        screen.blit(rule5, (15, 200))
        screen.blit(rule6, (90, 75))

        for button in [BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    interface()

        pygame.display.update()
