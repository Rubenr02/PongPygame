# Import the pygame library and initialise the game engine
import pygame
from ball import Ball
from paddle import Paddle
from powers import Colision_power
from big_paddle import BigPaddle
from pygame import mixer
from random import randint, choices
import random
from Button_class import Button
import sys

pygame.init()

paddle_sizeA = 100
playsound = 1
lastplayerhit = 0
powerballtimer = 0

PaddleAcolour = [randint(1, 255), randint(1, 255), randint(1, 255)]
PaddleBcolour = [randint(1, 255), randint(1, 255), randint(1, 255)]

WHITE = (255, 255, 255)


def play_pong():
    global playsound
    global powerballtimer
    global lastplayerhit
    # Initialize pygames
    pygame.mixer.init()
    triggered = False
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Open a new window
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")

    BigPaddle().affect_player_A()

    # setting up the paddle for player A
    paddleA = Paddle(PaddleAcolour, 10, paddle_sizeA)
    paddleA.rect.x = 20
    paddleA.rect.y = 200

    # setting up the shrinked paddle for player A
    smallA = Paddle(PaddleAcolour, 10, 50)
    smallA.rect.x = 20
    smallA.rect.y = 200

    # setting up the enlarged paddle for player A
    bigA = Paddle(PaddleAcolour, 10, 150)
    bigA.rect.x = 20
    bigA.rect.y = 200

    # setting up the paddle for player B
    paddleB = Paddle(PaddleBcolour, 10, 100)
    paddleB.rect.x = 670
    paddleB.rect.y = 200

    # setting up the shrinked paddle for player B
    smallB = Paddle(PaddleBcolour, 10, 50)
    smallB.rect.x = 670
    smallB.rect.y = 200

    # setting up the enlarged paddle for player B
    bigB = Paddle(PaddleBcolour, 10, 150)
    bigB.rect.x = 670
    bigB.rect.y = 200

    # setting up the ball and its position
    ball = Ball(WHITE, 14, 14)

    # setting up the ball that will be invisible
    ball2 = Ball(BLACK, 14, 14)

    # setting up the ball speed
    ball.velocity = [randint(4, 4), randint(-4, 4)]

    # setting up the invisible ball speed
    ball2.velocity = [randint(4, 4), randint(-4, 4)]

    # setting up the initial ball position
    ball.rect.x = 343
    ball.rect.y = 220

    # setting up the powers and its position
    powers = Colision_power([randint(1, 255), randint(1, 255), randint(1, 255)], 40, 40)
    powers.spawn_pos()

    # This will be a list that will contain all the sprites  we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()

    # Add the 2 paddles, the ball and the powers to the list of objects
    all_sprites_list.add(paddleA)
    all_sprites_list.add(paddleB)
    all_sprites_list.add(ball)
    all_sprites_list.add(powers)

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
    powers.spawn_pos()
    # Initialise player scores
    scoreA = 0
    scoreB = 0

    # Resets the ball position after a point is scored
    def reset():
        ball.rect.x = 343
        ball.rect.y = 220
        ball.velocity = [randint(4, 4), randint(-4, 4)]
        all_sprites_list.add(ball)
        all_sprites_list.remove(ball2)
        paddleA.freeze_duration = 0
        paddleB.freeze_duration = 0

    # related to sounds
    def play_sound():

        global playsound
        if playsound == 1:
            pygame.mixer.Sound(file='assets/sound 1.wav').play()
            playsound = 0
        else:
            pygame.mixer.Sound(file='assets/sound 2.wav').play()
            playsound = 1

    # -------- Main Program Loop -----------
    while carryOn:
        BigPaddle().affect_player_A()
        # --- Main event loop - See if I continue with the game
        # User did something
        for event in pygame.event.get():
            # If user clicked close
            if event.type == pygame.QUIT:
                # Flag that we are done so we exit this loop
                carryOn = False
            # Or he used the keyboard
            elif event.type == pygame.KEYDOWN:
                # Pressing the x Key will quit the game
                if event.key == pygame.K_x:
                    # quit the loop
                    carryOn = False
                if event.key == pygame.K_ESCAPE:
                    resume_()

        timer = int(pygame.time.get_ticks() / 1000)  # Create a timer

        # Actually performing game-like things:
        # Moving the paddles when the use uses the arrow keys (player B) or "W/S" keys (player A)
        keys = pygame.key.get_pressed()
        # this built-in method saves the user input from the keyboard

        # moving the paddles when the user hits W/S (player A) or arrow up/arrow down (player B)
        if keys[pygame.K_w]:
            paddleA.moveUp(7)
            triggered = True

        if keys[pygame.K_s]:
            paddleA.moveDown(7)
            triggered = True

        if keys[pygame.K_UP]:
            paddleB.moveUp(7)
            triggered = True

        if keys[pygame.K_DOWN]:
            paddleB.moveDown(7)
            triggered = True

        # Game logic
        ball.move(move=triggered)

        # Checking if the ball was scored and changing the speed accordingly while playing a sound
        if ball.rect.x >= 690:
            scoreA += 1
            pygame.mixer.Sound(file='assets/Goal.wav').play()
            reset()
            triggered = False
            ball.velocity[0] = -ball.velocity[0]

        if ball.rect.x <= 0:
            scoreB += 1
            pygame.mixer.Sound(file='assets/Goal.wav').play()
            reset()
            triggered = False
            ball.velocity[0] = -ball.velocity[0]
        # when score reaches 10, game ends and goes back to the interface
        if scoreA >= 10 or scoreB >= 10:
            interface()

        # Checking if the ball bounced on the walls

        if ball.rect.y > 480:
            ball.velocity[1] = -ball.velocity[1]
            play_sound()

        if ball.rect.y <= 0:
            ball.velocity[1] = -ball.velocity[1]
            play_sound()

        # Detect collisions between the ball and the paddles and change its speed accordingly(use the method we created)
        if pygame.sprite.collide_rect(ball, paddleA):
            play_sound()
            ball.velocity = [random.randint(8, 8), random.randint(-8, 8)]
            ball.lastplayerhit = "paddleA"
            # Registers from which player the last hit on the ball was


        elif pygame.sprite.collide_rect(ball, paddleB):
            ball.velocity = [random.randint(8, 8), random.randint(-8, 8)]
            play_sound()
            ball.lastplayerhit = "paddleB"
            ball.bounce()

        power_names = ["freeze", "freeze", "shrink", "shrink", "shrink", "enlarge", "enlarge", "enlarge",
                       "bounce", "bounce", "bounce", "invisible", "rapid ball", "rapid ball"]

        # making a random choice of the existing powers
        power_ups = random.choice(power_names)
        if timer % 9 == 0:  # divides the milliseconds with the desired time
            if powerballtimer == 0:  # a condition that makes the timer not set off the function 60 times per second
                all_sprites_list.add(powers)
                powercolour = [randint(1, 255), randint(1, 255), randint(1, 255)]
                powers.spawn_pos()
                powerballtimer += 1
            else:
                powerballtimer += 1
        if powerballtimer > 62:  # a counter so the function correctly activates in the next 'activation' of the timer
            powerballtimer = 0

        # checking collision between ball and powers(ball)
        collision1_power = pygame.sprite.collide_mask(ball, powers)

        # if the chosen power is freeze, then:
        if power_ups == "freeze":

            # if there is collision between ball and powers(ball) and the last registered hit is from player B
            if collision1_power and ball.lastplayerhit == "paddleB":
                paddleA.freeze_duration = 75  # The freeze time duration is activated and player A is affected
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.add(ball)  # Adds the ball again, after colliding with a paddle

                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/Freeze.wav').play()
            # if there is collision between ball and powers(ball) and the last registered hit is from player A
            elif collision1_power and ball.lastplayerhit == "paddleA":
                paddleB.freeze_duration = 75  # The freeze time duration is activated and player B is affected
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.add(ball)  # Adds the ball again, after colliding with a paddle
                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/Freeze.wav').play()

        # if the chosen power is bounce, then:
        if power_ups == "bounce":

            # if there is collision between ball and powers(ball)
            if collision1_power:
                ball.bounce()  # The ball bounces
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/Bounce.wav').play()
        # This power-up works as a power for both players
        # This means that there is no distinction between the affected players, it can be good or bad for you

        # if the chosen power is shrink, then:
        if power_ups == "shrink":

            # if there is collision between ball and powers(ball) and the last registered hit is from player A
            if collision1_power and ball.lastplayerhit == "paddleA":
                all_sprites_list.remove(paddleB)  # Paddle B is removed
                all_sprites_list.add(smallB)  # A new smaller version of Paddle B is added
                paddleB = smallB  # Old paddle B becomes new smaller paddle B
                paddleB.update()  # Values are updated
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/Bigger.wav').play()
                
            elif collision1_power and ball.lastplayerhit == "paddleB":
                # if there is collision between ball and powers(ball) and the last registered hit is from player B
                all_sprites_list.remove(paddleA)  # Paddle A is removed
                all_sprites_list.add(smallA)  # A new smaller version of Paddle A is added
                paddleA = smallA  # Old paddle A becomes new smaller paddle A
                paddleA.update()  # Values are updated
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/Bigger.wav').play()

        if power_ups == "enlarge":
            # if there is collision between ball and powers(ball) and the last registered hit is from player B
            if collision1_power and ball.lastplayerhit == "paddleB":
                all_sprites_list.remove(paddleA)  # Paddle A is removed
                all_sprites_list.add(bigA)  # A new larger version of Paddle A is added
                paddleA = bigA  # Old paddle A becomes new larger paddle A
                paddleA.update()  # Values are updated
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/Bigger.wav').play()

            elif collision1_power and ball.lastplayerhit == "paddleA":
                # if there is collision between ball and powers(ball) and the last registered hit is from player A
                all_sprites_list.remove(paddleB)  # Paddle B is removed
                all_sprites_list.add(bigB)  # A new larger version of Paddle B is added
                paddleB = bigB  # Old paddle A becomes new larger paddle B
                paddleB.update()  # Values are updated
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/Bigger.wav').play()

        # if the chosen power is freeze, then:
        if power_ups == "invisible":
            # if there is collision between ball and powers(ball)
            if collision1_power:
                all_sprites_list.remove(ball)  # The ball is removed
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/invisible.wav').play()

        # if the chosen power is rapid ball, then:
        if power_ups == "rapid ball":
            # if there is collision between ball and powers(ball)
            if collision1_power:
                ball.velocity = [random.randint(15, 15), random.randint(-15, 15)]  # The ball speed will be increased to 15, almost double as possible
                powers.spawn_pos()  # The power-up ball will re-spawn in a random position
                all_sprites_list.remove(powers)  # The power-up ball is removed from the screen
                pygame.mixer.Sound(file='assets/Fast.wav').play()

        # Set a flag to track whether the collision has occurred

        # if not collided:
        #   timer += pygame.time.get_ticks()
        #  print(timer)

        # if timer1 == timer3:
        #    all_sprites_list.add(powers)
        #   powers.affect_player_A()
        #  timer3 += 10000
        #     collided = False

        # Drawing code should go here
        # First, clear the screen to black.
        screen.fill(BLACK)
        # Draw the net A WHITE LINE FROM TOP TO BOTTOM (USE PYGAME BUILT-IN METHOD)
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen)

        # Display scores:
        pygame.font.get_fonts()
        font = pygame.font.Font(None, 74)
        text = font.render(str(scoreA), 1, (PaddleAcolour))
        screen.blit(text, (250, 10))
        text = font.render(str(scoreB), 1, (PaddleBcolour))
        screen.blit(text, (420, 10))

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Once we have exited the main program loop we can stop the game engine:
    pygame.quit()


# a nice color
nice_blue = (93, 131, 179)

res = (720, 720)
screen = pygame.display.set_mode(res)

playmusic = randint(1, 4)
mute = 0
# fonts which are used throughout the code
main_font = pygame.font.Font("assets/titulo.otf", 60)
rule_font = pygame.font.Font("assets/titulo.otf", 40)
lines_font = pygame.font.Font("assets/titulo.otf", 20)


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


# Creating a function that creates the GUI
def interface():
    """The user can play the game,
    mute the game's music, switch to the next music track, go to the credits, to the rules
    and quit the game
    """
    global playmusic
    global mute
    # initializes the mixer
    pygame.mixer.init()
    # Set the size of the screen and create it
    size = (720, 720)
    screen = pygame.display.set_mode(size)
    title_text = main_font.render('PING PONG 3000', True, WHITE)
    play_music()
    # interface loop
    while True:
        # Set the background color of the screen
        screen.fill(nice_blue)

        # Get the current position of the mouse
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Some fonts
        byron_pong = pygame.font.Font("assets/Byron.ttf", 70)
        byron_2 = pygame.font.Font("assets/Byron.ttf", 45)
        byron_3 = pygame.font.Font("assets/Byron.ttf", 30)

        # Create 'PLAY', 'RULES', 'QUIT', 'CREDITS', 'NEXT' AND 'MUTE' buttons
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

        # Update the color of the buttons based on whether the mouse is hovering over it
        for button in [PLAY_BUTTON, RULES_BUTTON, QUIT_BUTTON, CREDITS_BUTTON, NEXT_BUTTON, MUTE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # when the button are clicked, each will give different sounds
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    play_pong()  # will return to the game
                if RULES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    rules()  # will return to the rules
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    pygame.quit()  # quits the game
                    sys.exit()
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    credits_()  # will return to the credits
                if MUTE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    if mute == 0:
                        mute = 1
                        pygame.mixer.music.stop()
                    elif mute == 1:
                        play_music()
                        mute = 0
                if NEXT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
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
        # Update the display
        pygame.display.update()


def resume_():
    """
    Displays the pause menu for the game.

    The user can return to the main menu by clicking the 'BACK' button.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    global playmusic
    global mute

    # Set the size of the screen and create it
    size = (700, 500)
    screen = pygame.display.set_mode(size)

    # Set the font for the buttons
    byron_3 = pygame.font.Font("assets/Byron.ttf", 30)

    # Set the background color of the screen
    nice_blue = (93, 131, 179)

    while True:
        # Fill the screen with the nice_blue color
        screen.fill(nice_blue)

        # Get the current position of the mouse
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Create 'BACK', 'QUIT', 'NEXT MUSIC', and 'MUTE' buttons
        RESUME_BUTTON = Button(image=pygame.image.load("../pong/assets/Quit Rect-modified.png"), pos=(350, 130),
                               text_input="BACK", font=byron_3, base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("../pong/assets/Quit Rect-modified.png"), pos=(350, 200),
                             text_input="QUIT", font=byron_3, base_color="#000000", hovering_color="White")
        NEXT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect-modified.png"), pos=(350, 270),
                             text_input="NEXT MUSIC", font=byron_3, base_color="#000000", hovering_color="White")
        MUTE_BUTTON = Button(image=pygame.image.load("assets/Quit Rect-modified.png"), pos=(350, 340),
                             text_input="MUTE", font=byron_3, base_color="#000000", hovering_color="White")

        # Update the color of the buttons based on whether the mouse is hovering over it
        for button in [RESUME_BUTTON, QUIT_BUTTON, NEXT_BUTTON, MUTE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # Check for events such as quitting the game or clicking the 'RESUME' button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # when the button are clicked, each will give different sounds
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    play_pong()  # will return to the game
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    interface()  # will return to the interface
                if MUTE_BUTTON.checkForInput(MENU_MOUSE_POS):

                    pygame.mixer.Sound(file='assets/click.wav').play()
                    if mute == 0:
                        mute = 1
                        pygame.mixer.music.stop()
                    elif mute == 1:
                        play_music()
                        mute = 0
                if NEXT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    if playmusic == 1:
                        playmusic = 2
                    elif playmusic == 2:
                        playmusic = 3
                    elif playmusic == 3:
                        playmusic = 4
                    elif playmusic == 4:
                        playmusic = 1
                    play_music()
        # Update the display
        pygame.display.update()


def credits_():
    """
    Displays the credits of the game to the user.

    The user can return to the main menu by clicking the 'BACK' button.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # some texts
    line1_text = lines_font.render('Davide Farinati, dfarinati@novaims.unl.pt', True, WHITE)
    line2_text = lines_font.render('Ilya Bakurov, ibakurov@novaims.unl.pt', True, WHITE)
    line3_text = lines_font.render('Liah Rosenfeld, lrosenfeld@novaims.unl.pt', True, WHITE)
    credits_text = main_font.render('Credits', True, WHITE)
    # a font
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

        # Update the color of the 'BACK' button based on whether the mouse is hovering over it
        for button in [BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # Check for events such as quitting the game or clicking the 'BACK' button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    interface()
        # Update the display
        pygame.display.update()


def rules():
    """
    Displays the rules of the game to the user.

    The user can return to the main menu by clicking the 'BACK' button.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # several fonts and text
    byron_3 = pygame.font.Font("assets/Byron.ttf", 30)
    rules_text = rule_font.render('Welcome to a better pong', True, WHITE)
    rule9 = lines_font.render('Please have your sound on, there are various sound effects.', True, WHITE)
    rule1 = lines_font.render('The game can be played by 2 players. The first to reach 10 poits i', True, WHITE)
    rule2 = lines_font.render('In order to move player 1 you need to use the keys "W" and "S".', True, WHITE)
    rule3 = lines_font.render('In order to move player 2 you need to use the arrows "UP" and "DOWN".', True, WHITE)
    rule4 = lines_font.render('Freeze Power-Up will make you unable to move your paddle for 3 seconds.', True, WHITE)
    rule5 = lines_font.render('Shrink and Enlarge will make your paddle super small or supper large.', True, WHITE)
    rule6 = lines_font.render('Invisible Power-Up will make your ball go invisible. Try to catch it!', True, WHITE)
    rule7 = lines_font.render('Bounce is dangerous!! It will make the ball go back to you. ', True, WHITE)
    rule8 = lines_font.render('Speed Power-Up will make your ball go super fast. ', True, WHITE)

    while True:
        # Fill the screen with the nice_blue color
        screen.fill(nice_blue)

        # Get the current position of the mouse
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Create a 'BACK' button
        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect-modified.png"), pos=(150, 650),
                             text_input="BACK", font=byron_3, base_color="#000000", hovering_color="White")

        # Render the rules and buttons to the screen
        screen.blit(rules_text, (100, 15))
        screen.blit(rule1, (15, 100))
        screen.blit(rule2, (15, 125))
        screen.blit(rule3, (15, 150))
        screen.blit(rule4, (15, 175))
        screen.blit(rule5, (15, 200))
        screen.blit(rule6, (15, 225))
        screen.blit(rule7, (15, 250))
        screen.blit(rule8, (15, 275))
        screen.blit(rule9, (15, 300))

        # Update the color of the 'BACK' button based on whether the mouse is hovering over it
        for button in [BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # Check for events such as quitting the game or clicking the 'BACK' button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(file='assets/click.wav').play()
                    interface()
        # Update the display
        pygame.display.update()
