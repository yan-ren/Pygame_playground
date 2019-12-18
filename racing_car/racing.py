import pygame, sys
import random
from modules.constants import *
from modules import utils

pygame.init()
crash_sound = pygame.mixer.Sound("audio/Crash.wav")
pygame.mixer.music.load("audio/HandClap.wav")
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Race Car')
clock = pygame.time.Clock()
car = pygame.image.load('img/car1.png').convert_alpha()
pygame.display.set_icon(pygame.image.load('img/car_icon.png').convert_alpha())


def display_score(score):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Score: " + str(score), True, BLACK)
    display.blit(text, (0, 0))


def display_level(level):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Level: " + str(level), True, BLACK)
    display.blit(text, (0, 30))


def draw_block(x, y, width, height, color):
    pygame.draw.rect(display, color,(x, y, width, height))


def place_car(x, y):
    display.blit(car, (x, y))


def crash():
    crashed = True
    btn_width = 120
    btn_height = 50
    play_btn_x = WINDOW_WIDTH / 4
    quit_btn_x = WINDOW_WIDTH - WINDOW_WIDTH / 4 - btn_width
    play_btn_y = quit_btn_y = WINDOW_HEIGHT / 6 * 4

    message_display('You Crashed!')
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    while crashed:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # display
        clicked = button(play_btn_x, play_btn_y, btn_width, btn_height, "Play Again!", DARK_GREEN, GREEN)
        if clicked:
            crashed = False
        clicked = button(quit_btn_x, quit_btn_y, btn_width, btn_height, "QUIT!", DARK_RED, RED)
        if clicked:
            pygame.quit()
            sys.exit()
        pygame.display.update()

        # FPS
        clock.tick(FPS)

    # start game again
    game_loop()


def message_display(msg):
    text_style = pygame.font.Font('fonts/freesansbold.ttf', 100)
    text_surf = text_style.render(msg, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    display.blit(text_surf, text_rect)
    pygame.display.update()


def button(x, y, width, height, text, normal_color, hover_color):
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


def start_menu():
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
        clicked = button(start_btn_x, start_btn_y, btn_width, btn_height, "GO!", DARK_GREEN, GREEN)
        if clicked:
            start_game = True
        clicked = button(quit_btn_x, quit_btn_y, btn_width, btn_height, "QUIT!", DARK_RED, RED)
        if clicked:
            pygame.quit()
            sys.exit()
        pygame.display.update()

        # FPS
        clock.tick(FPS)


def pause():
    paused = True
    btn_width = 100
    btn_height = 50
    pause_btn_x = WINDOW_WIDTH / 4
    quit_btn_x = WINDOW_WIDTH - WINDOW_WIDTH / 4 - btn_width
    pause_btn_y = quit_btn_y = WINDOW_HEIGHT / 6 * 4

    pygame.mixer.music.pause()
    message_display("Paused!")

    while paused:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # display
        clicked = button(pause_btn_x, pause_btn_y, btn_width, btn_height, "Continue!", DARK_GREEN, GREEN)
        if clicked:
            paused = False
        clicked = button(quit_btn_x, quit_btn_y, btn_width, btn_height, "QUIT!", DARK_RED, RED)
        if clicked:
            pygame.quit()
            sys.exit()
        pygame.display.update()

        # FPS
        clock.tick(FPS)

    pygame.mixer.music.unpause()


def game_loop():
    game_exit = False
    car_x = WINDOW_WIDTH * 0.45
    car_y = WINDOW_HEIGHT * 0.8
    car_x_change = 0
    block_x = random.randint(0, WINDOW_WIDTH)
    block_y = -WINDOW_HEIGHT
    block_speed = 7
    block_width = 100
    block_height = 100
    score = 0
    level = 1

    pygame.mixer.music.play(-1)

    while not game_exit:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_x_change = -5
                elif event.key == pygame.K_RIGHT:
                    car_x_change = 5
                elif event.key == pygame.K_p:
                    pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    car_x_change = 0

        # movement variable
        car_x += car_x_change
        block_y += utils.calculate_speed(block_speed, level)

        # movement variable handling
        # car crashes on edge
        if car_x < 0 or car_x > (WINDOW_WIDTH - car.get_rect().width):
            crash()
            game_exit = True
        # car crashes on blocks
        if car_y < block_y + block_height:
            if block_x < car_x < block_x + block_width or block_x < car_x + car.get_rect().width < block_x + block_width:
                crash()
                game_exit = True
        # block passes car, initialize block position
        if block_y > WINDOW_HEIGHT:
            block_y = -WINDOW_HEIGHT
            block_x = random.randint(0, WINDOW_WIDTH)
            score += 1
            level = utils.calculate_level(score)

        # display
        display.fill(WHITE)
        place_car(car_x, car_y)
        draw_block(block_x, block_y, block_width, block_height, BLACK)
        display_score(score)
        display_level(level)
        pygame.display.update()

        # FPS
        clock.tick(FPS)


start_menu()
game_loop()
pygame.quit()
sys.exit()
