import pygame, sys
import random
from modules.constants import *
from modules import utils
from modules.car import Car
from modules.block import Block


pygame.init()
pygame.mixer.music.load("audio/HandClap.wav")
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Race Car')
pygame.display.set_icon(pygame.image.load('img/car_icon.png').convert_alpha())

# Global Variable
crash_sound = pygame.mixer.Sound("audio/Crash.wav")
clock = pygame.time.Clock()
# key lock
left_key_pressed = False
right_key_pressed = False
# game object
car1 = None
block_list = []
score = 0
level = 1


def display_score(score):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Score: " + str(score), True, BLACK)
    display.blit(text, (0, 0))


def display_level(level):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Level: " + str(level), True, BLACK)
    display.blit(text, (0, 30))


def display_block(blocks):
    for b in blocks:
        display.blit(b.img, (b.x, b.y))


def display_car(car):
    display.blit(car.img, (car.x, car.y))


def display_message(msg):
    text_style = pygame.font.Font('fonts/freesansbold.ttf', 100)
    text_surf = text_style.render(msg, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    display.blit(text_surf, text_rect)
    pygame.display.update()


def display_button(x, y, width, height, text, normal_color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(display, hover_color, (x, y, width, height))
        if click[0]:
            return 1
    else:
        pygame.draw.rect(display, normal_color, (x, y, width, height))

    text_style = pygame.font.Font('fonts/freesansbold.ttf', 20)
    text_surf = text_style.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (x + width / 2, y + height / 2)
    display.blit(text_surf, text_rect)


def frame_start_menu():
    start_game = False
    btn_width = 100
    btn_height = 50
    start_btn_x = WINDOW_WIDTH / 4
    quit_btn_x = WINDOW_WIDTH - WINDOW_WIDTH / 4 - btn_width
    start_btn_y = quit_btn_y = WINDOW_HEIGHT / 6 * 4

    while not start_game:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # display
        display.fill(WHITE)
        text_style = pygame.font.Font('fonts/freesansbold.ttf', 60)
        text_surf = text_style.render("A Racing Car Game", True, BLACK)
        text_rect = text_surf.get_rect()
        text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        display.blit(text_surf, text_rect)
        clicked = display_button(start_btn_x, start_btn_y, btn_width, btn_height, "GO!", DARK_GREEN, GREEN)
        if clicked:
            start_game = True
        clicked = display_button(quit_btn_x, quit_btn_y, btn_width, btn_height, "QUIT!", DARK_RED, RED)
        if clicked:
            pygame.quit()
            sys.exit()
        pygame.display.update()

        # FPS
        clock.tick(FPS)


def frame_pause():
    paused = True
    btn_width = 100
    btn_height = 50
    pause_btn_x = WINDOW_WIDTH / 4
    quit_btn_x = WINDOW_WIDTH - WINDOW_WIDTH / 4 - btn_width
    pause_btn_y = quit_btn_y = WINDOW_HEIGHT / 6 * 4

    pygame.mixer.music.pause()
    display_message("Paused!")

    while paused:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # display
        clicked = display_button(pause_btn_x, pause_btn_y, btn_width, btn_height, "Continue!", DARK_GREEN, GREEN)
        if clicked:
            paused = False
        clicked = display_button(quit_btn_x, quit_btn_y, btn_width, btn_height, "QUIT!", DARK_RED, RED)
        if clicked:
            pygame.quit()
            sys.exit()
        pygame.display.update()

        # FPS
        clock.tick(FPS)

    pygame.mixer.music.unpause()


def frame_crash():
    crashed = True
    btn_width = 120
    btn_height = 50
    play_btn_x = WINDOW_WIDTH / 4
    quit_btn_x = WINDOW_WIDTH - WINDOW_WIDTH / 4 - btn_width
    play_btn_y = quit_btn_y = WINDOW_HEIGHT / 6 * 4

    display_message('You Crashed!')
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    while crashed:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # display
        clicked = display_button(play_btn_x, play_btn_y, btn_width, btn_height, "Play Again!", DARK_GREEN, GREEN)
        if clicked:
            crashed = False
            return False
        clicked = display_button(quit_btn_x, quit_btn_y, btn_width, btn_height, "QUIT!", DARK_RED, RED)
        if clicked:
            pygame.quit()
            sys.exit()
        pygame.display.update()

        # FPS
        clock.tick(FPS)


def game_init():
    globals()['left_key_pressed'] = False
    globals()['right_key_pressed'] = False
    globals()['car1'] = Car(pygame.image.load('img/car2.png').convert_alpha(), 0.45, 0.85, 0)
    if len(globals()['block_list']) == 0:
        globals()['block_list'].append(Block(pygame.image.load('img/brick-1.png').convert_alpha(),
                                             random.randint(0, WINDOW_WIDTH), -WINDOW_HEIGHT, 3))
        globals()['block_list'].append(Block(pygame.image.load('img/brick-1.png').convert_alpha(),
                                             random.randint(0, WINDOW_WIDTH), -WINDOW_HEIGHT, 7))
    else:
        for b in globals()['block_list']:
            b.restore()
    globals()['score'] = 0
    globals()['level'] = 1

    pygame.mixer.music.play(-1)


def check_crash(car, blocks):
    for b in blocks:
        if utils.crash_detection(car, b):
            return True
    return False


def game_loop():
    game_init()
    global left_key_pressed, right_key_pressed, score, level, car1, block_list
    game_exit = False
    level_up = False

    while not game_exit:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_key_pressed = True
                    car1.x_move = -5
                elif event.key == pygame.K_RIGHT:
                    right_key_pressed = True
                    car1.x_move = 5
                elif event.key == pygame.K_p:
                    frame_pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and left_key_pressed:
                    right_key_pressed = False
                    car1.x_move = -5
                elif event.key == pygame.K_RIGHT:
                    right_key_pressed = False
                    car1.x_move = 0
                if event.key == pygame.K_LEFT and right_key_pressed:
                    left_key_pressed = False
                    car1.x_move = 5
                elif event.key == pygame.K_LEFT:
                    left_key_pressed = False
                    car1.x_move = 0

        # movement variable
        car1.change_x()
        for b in block_list:
            b.change_y()

        # movement variable handling
        # car crashes on edge
        if car1.x < 0 or car1.x > (WINDOW_WIDTH - car1.get_width()):
            # frame_crash() return False, restart game
            if not frame_crash():
                game_init()
        # car crashes on blocks
        if check_crash(car1, block_list):
            # frame_crash() return False, restart game
            if not frame_crash():
                game_init()
        # block passes car, initialize block position
        for b in block_list:
            if b.y > WINDOW_HEIGHT:
                b.y = -WINDOW_HEIGHT
                b.x = random.randint(0, WINDOW_WIDTH)
                score += 1
                level = utils.calculate_level(score)

        # display
        display.fill(WHITE)
        display_car(car1)
        display_block(block_list)
        display_score(score)
        display_level(level)
        pygame.display.update()

        # FPS
        clock.tick(FPS)


if __name__ == "__main__":
    frame_start_menu()
    game_loop()
    pygame.quit()
    sys.exit()
