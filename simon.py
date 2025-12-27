import pygame
import random
import sys
import time

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simon Game")

FONT = pygame.font.SysFont("arial", 32)
BIG_FONT = pygame.font.SysFont("arial", 40)

# Colors
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

buttons = {
    "red": pygame.Rect(50, 150, 200, 200),
    "green": pygame.Rect(350, 150, 200, 200),
    "blue": pygame.Rect(50, 400, 200, 200),
    "yellow": pygame.Rect(350, 400, 200, 200)
}

colors = ["red", "green", "blue", "yellow"]
color_map = {
    "red": RED,
    "green": GREEN,
    "blue": BLUE,
    "yellow": YELLOW
}

sounds = {
    c: pygame.mixer.Sound(f"sounds/{c}.wav") for c in colors
}
sounds["wrong"] = pygame.mixer.Sound("sounds/wrong.wav")

game_pattern = []
user_pattern = []
level = 0
started = False
high_score = 0


def draw():
    screen.fill((1, 31, 63))
    title = BIG_FONT.render(f"Level {level}", True, WHITE)
    score = FONT.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(title, (200, 30))
    screen.blit(score, (200, 80))

    for c, rect in buttons.items():
        pygame.draw.rect(screen, color_map[c], rect)

    pygame.display.update()


def flash(color):
    pygame.draw.rect(screen, WHITE, buttons[color])
    pygame.display.update()
    sounds[color].play()
    time.sleep(0.4)
    draw()


def next_sequence():
    global level
    user_pattern.clear()
    level += 1
    choice = random.choice(colors)
    game_pattern.append(choice)

    for c in game_pattern:
        flash(c)
        time.sleep(0.2)


def check_answer(index):
    global started, level, high_score
    if user_pattern[index] != game_pattern[index]:
        sounds["wrong"].play()
        time.sleep(1)
        high_score = max(high_score, level - 1)
        reset()
        return

    if len(user_pattern) == len(game_pattern):
        time.sleep(0.5)
        next_sequence()


def reset():
    global game_pattern, user_pattern, level, started
    game_pattern.clear()
    user_pattern.clear()
    level = 0
    started = False


def get_color_clicked(pos):
    for c, rect in buttons.items():
        if rect.collidepoint(pos):
            return c
    return None


clock = pygame.time.Clock()

while True:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not started:
            started = True
            next_sequence()

        if event.type == pygame.MOUSEBUTTONDOWN and started:
            color = get_color_clicked(event.pos)
            if color:
                  pygame.draw.rect(screen, WHITE, buttons[color])
                  pygame.display.update()
                  sounds[color].play()
            time.sleep(0.2)
            draw()

            user_pattern.append(color)
            check_answer(len(user_pattern) - 1)


    clock.tick(60)
