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
start_time = None
# game object
car1 = None
block_list = []
score = 0
level = 1
highest_record = 0


def display_record(record):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Record: " + str(record), True, BLACK)
    display.blit(text, (WINDOW_WIDTH - 240, 0))


def display_score(score):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Score: " + str(score), True, BLACK)
    display.blit(text, (0, 0))


def display_time(time):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Time: " + str(time), True, BLACK)
    display.blit(text, (0, 0))


def display_level(level):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Level: " + str(level), True, BLACK)
    display.blit(text, (0, 30))


def display_life(life):
    font = pygame.font.Font("fonts/freesansbold.ttf", 25)
    text = font.render("Life: " + str(life), True, BLACK)
    display.blit(text, (0, 60))


def display_block(blocks):
    for b in blocks:
        display.blit(b.img, (b.x, b.y))


def display_car(car):
    display.blit(car.img, (car.x, car.y))


def display_message(msg, font_size, x_pos, y_pos):
    text_style = pygame.font.Font('fonts/freesansbold.ttf', font_size)
    text_surf = text_style.render(msg, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (x_pos, y_pos)
    display.blit(text_surf, text_rect)


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
        display_message("A Racing Car Game", 60, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
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

        display_message("Paused!", 100, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        pygame.display.update()

        # FPS
        clock.tick(FPS)

    pygame.mixer.music.unpause()


def frame_crash(current_time):
    global highest_record, start_time

    crashed = True
    btn_width = 120
    btn_height = 50
    play_btn_x = WINDOW_WIDTH / 4
    quit_btn_x = WINDOW_WIDTH - WINDOW_WIDTH / 4 - btn_width
    play_btn_y = quit_btn_y = WINDOW_HEIGHT / 6 * 4

    # stop bg music, and play crash sound
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    while crashed:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update highest record
        if current_time - start_time > highest_record:
            highest_record = current_time - start_time

        # display
        clicked = display_button(play_btn_x, play_btn_y, btn_width, btn_height, "Play Again!", DARK_GREEN, GREEN)
        if clicked:
            crashed = False
            return False
        clicked = display_button(quit_btn_x, quit_btn_y, btn_width, btn_height, "QUIT!", DARK_RED, RED)
        if clicked:
            pygame.quit()
            sys.exit()

        display_message('You Crashed!', 100, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        pygame.display.update()

        # FPS
        clock.tick(FPS)


def frame_countdown():
    global car1
    left_key_pressed = right_key_pressed = False
    start_tick = pygame.time.get_ticks()
    # this list holds display words, one word shows 1s, need '' at the beginning for second element can show for 1s
    countdown_text = ['', 'Game Start!', '1', '2', '3']
    current_display = countdown_text.pop()

    while len(countdown_text) != 0:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        # movement variable handling
        # car stops on edge
        if car1.x < 0 or car1.x > (WINDOW_WIDTH - car1.get_width()):
            car1.x_move = 0
        car1.change_x()

        # countdown ticker
        current_tick = pygame.time.get_ticks()
        if (current_tick - start_tick) / 1000 > 1:
            start_tick = current_tick
            current_display = countdown_text.pop()

        # display
        display.fill(WHITE)
        display_message(current_display, 100, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        display_car(car1)
        display_record(utils.convert_time(highest_record))
        pygame.display.update()

        # FPS
        clock.tick(FPS)

    # set global start timer
    globals()['start_time'] = pygame.time.get_ticks()


def game_init():
    globals()['car1'] = Car(pygame.image.load('img/car2.png').convert_alpha(), 0.45, 0.85, 0)
    if len(globals()['block_list']) == 0:
        globals()['block_list'].append(Block(pygame.image.load('img/brick-1.png').convert_alpha(),
                                             random.randint(0, WINDOW_WIDTH), -WINDOW_HEIGHT, 3))
        globals()['block_list'].append(Block(pygame.image.load('img/brick-1.png').convert_alpha(),
                                             random.randint(0, WINDOW_WIDTH), -WINDOW_HEIGHT, 5))
        globals()['block_list'].append(Block(pygame.image.load('img/brick-1.png').convert_alpha(),
                                             random.randint(0, WINDOW_WIDTH), -WINDOW_HEIGHT, 7))
    else:
        for b in globals()['block_list']:
            b.restore()
    globals()['score'] = 0
    globals()['level'] = 1

    frame_countdown()
    pygame.mixer.music.play(-1)


def check_crash(car, blocks):
    for b in blocks:
        if utils.crash_detection(car, b) and b.attached is None:
            b.attached = car
            return True
        elif not utils.crash_detection(car, b):
            b.attached = None
    return False


def game_loop():
    game_init()
    global score, level, car1, block_list
    # key lock
    left_key_pressed = False
    right_key_pressed = False
    game_exit = False

    while not game_exit:
        level_up = False
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
        # car stops on edge
        if car1.x < 0 or car1.x > (WINDOW_WIDTH - car1.get_width()):
            car1.x_move = 0
        # car crashes on blocks
        if check_crash(car1, block_list):
            car1.life = car1.life - 1
            if car1.life < 0 and not frame_crash(current_time):
                # frame_crash() return False, restart game
                game_init()
        # block passes car, initialize block position
        for b in block_list:
            if b.y > WINDOW_HEIGHT:
                b.y = -WINDOW_HEIGHT
                b.x = random.randint(0, WINDOW_WIDTH)
                score += 1
                level = utils.calculate_level(score)
                level_up = utils.level_up(score)
        # level up change
        if level_up:
            for b in block_list:
                b.speed = utils.calculate_speed(b.speed, level)
        # capture time
        current_time = pygame.time.get_ticks()

        # display
        display.fill(WHITE)
        display_car(car1)
        display_block(block_list)
        # display_score(score)
        display_time(utils.convert_time(current_time - start_time))
        display_level(level)
        display_life(car1.life)
        display_record(utils.convert_time(highest_record))
        pygame.display.update()

        # FPS
        clock.tick(FPS)


if __name__ == "__main__":
    frame_start_menu()
    game_loop()
    pygame.quit()
    sys.exit()
