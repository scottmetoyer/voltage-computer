import sys, pygame
from pygame.locals import *

pygame.init()

FRAMERATE = 30
clock = pygame.time.Clock()
size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

running = True

while running:
    clock.tick(FRAMERATE)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            running = False

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()

pygame.quit()
