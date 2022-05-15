import pygame
from pygame import mixer
import os
pygame.font.init()
pygame.mixer.init()#sound aspects

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

BULLET_FIRE_SOUND=mixer.Sound('laser.wav')
BULLET_HIT_SOUND=mixer.Sound('explosion.wav')
BORDER = pygame.Rect(WIDTH/2-5, 0, 10, HEIGHT)


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT= pygame.font.SysFont('comicsans',40)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
s_WIDTH, s_HEIGHT = 55, 40

y_HIT = pygame.USEREVENT + 1
r_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (s_WIDTH, s_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (s_WIDTH, s_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: "+str(red_health),1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: "+str(yellow_health),1,WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH-(red_health_text.get_width())-10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VEL > 0:  # LEFT
        yellow.x -= VEL
    # RIGHT
    if keys_pressed[pygame.K_d] and yellow.x + VEL + (yellow.width//2+20) < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y-VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT-15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x-VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + (red.width//2+20) < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y-VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT-15:
        red.y += VEL


# What this function does is move the bullets,handle the collision of the bullets,handle removing the bullets.
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(r_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(y_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)

def main():
    red = pygame.Rect(700, 300, s_WIDTH, s_HEIGHT)
    yellow = pygame.Rect(100, 300, s_WIDTH, s_HEIGHT)
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    mixer.music.load('background.wav')
    mixer.music.play(-1)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x+yellow.width, yellow.y+(yellow.height//2)-2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x+red.width, red.y+(red.height//2)-2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == r_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == y_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if red_health==0 or yellow_health==0:
            winner_text="Draw!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

main()


if __name__ == "__main__":
    main()
