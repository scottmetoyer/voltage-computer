import sys, pygame
from pygame.locals import *
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE

pygame.init()
size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
FRAMERATE = 200
clock = pygame.time.Clock()

black = 0, 0, 0
white = 255, 255, 255
light_color = 170, 170, 170
disabled_color = 120, 120, 120
dark_color = 60, 60, 60

selected_lfo = 0

small_font = pygame.font.SysFont('Corbel', 35)

button_text = [
    small_font.render('A' , True , white),
    small_font.render('B' , True , white),
    small_font.render('C' , True , white),
    small_font.render('D' , True , white)
]

select_buttons = [
    pygame.Rect(600, 430, 40, 40),
    pygame.Rect(650, 430, 40, 40),
    pygame.Rect(700, 430, 40, 40),
    pygame.Rect(750, 430, 40, 40)
]

slider_container = pygame.Rect(100, 430, 400, 40)
cycles_per_second = [1,1,1,1]

lfos = [
    [100 for x in range(40)],
    [100 for x in range(40)],
    [100 for x in range(40)],
    [100 for x in range(40)]
]

playhead_position = 0

def draw_controls():
  pygame.draw.rect(screen, dark_color, slider_container)




pygame.mouse.set_visible(False)
running = True

while running:
  clock.tick(FRAMERATE)

  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      running = False
    elif e.type == KEYDOWN and e.key == K_ESCAPE:
      running = False

  screen.fill(black)
  draw_controls()
  pygame.display.flip()

pygame.quit()
exit()