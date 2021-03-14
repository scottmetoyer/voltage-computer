import sys, pygame
from pygame.locals import *
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE

pygame.init()
size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
FRAMERATE = 30
clock = pygame.time.Clock()

black = 0, 0, 0
white = 255, 255, 255
light_color = 170, 170, 170
dark_color = 100, 100, 100

smallfont = pygame.font.SysFont('Corbel', 35)
textA = smallfont.render('A' , True , white)
textB = smallfont.render('B' , True , white)
textC = smallfont.render('C' , True , white)
textD = smallfont.render('D' , True , white)
buttonA = pygame.Rect(600, 430, 40, 40)
buttonB = pygame.Rect(650, 430, 40, 40)
buttonC = pygame.Rect(700, 430, 40, 40)
buttonD = pygame.Rect(750, 430, 40, 40)
lfoA = [100 for x in range(40)]
lfoB = [100 for x in range(40)]
lfoC = [100 for x in range(40)]
lfoD = [100 for x in range(40)]
selectedButton = buttonA
selectedLFO = lfoA

def draw_lfo():
  for index, value in enumerate(selectedLFO):
    x = index * 20
    pygame.draw.circle(screen, light_color, (x, value), 5)

def draw_buttons():
  if selectedButton == buttonA:
    pygame.draw.rect(screen, light_color, buttonA)
  else:
    pygame.draw.rect(screen, dark_color, buttonA)

  if selectedButton == buttonB:
    pygame.draw.rect(screen, light_color, buttonB)
  else:
    pygame.draw.rect(screen, dark_color, buttonB)

  if selectedButton == buttonC:
    pygame.draw.rect(screen, light_color, buttonC)
  else:
    pygame.draw.rect(screen, dark_color, buttonC)

  if selectedButton == buttonD:
    pygame.draw.rect(screen, light_color, buttonD)
  else:
    pygame.draw.rect(screen, dark_color, buttonD)

  screen.blit(textA, (612, 439))
  screen.blit(textB, (662, 439))
  screen.blit(textC, (712, 439))
  screen.blit(textD, (762, 439))

def set_button(pos):
  global selectedButton
  global selectedLFO

  if (buttonA.collidepoint(pos)):
    selectedButton = buttonA
    selectedLFO = lfoA
  elif (buttonB.collidepoint(pos)):
    selectedButton = buttonB
    selectedLFO = lfoB
  elif (buttonC.collidepoint(pos)):
    selectedButton = buttonC
    selectedLFO = lfoC
  elif (buttonD.collidepoint(pos)):
    selectedButton = buttonD
    selectedLFO = lfoD

def set_lfo_point(pos):
  global selectedLFO
  (x,y) = pos
  index = x // 20
  selectedLFO[index] = y

def touch_handler(event, touch):
  if event == TS_PRESS:
    if (touch.y > 428):
      set_button((touch.x, touch.y))
    else:
      set_lfo_point((touch.x, touch.y))
  if event == TS_RELEASE:
      print("Got release", touch)
  if event == TS_MOVE:
    if (touch.y < 428):
      set_lfo_point((touch.x, touch.y))

ts = Touchscreen()
ts.touches[0].on_press = touch_handler
ts.touches[0].on_release = touch_handler
ts.touches[0].on_move = touch_handler
ts.run()

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

  # Draw the LFO select buttons
  draw_buttons()
  draw_lfo()
  pygame.display.flip()

pygame.quit()
ts.stop()
exit()