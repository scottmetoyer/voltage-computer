import sys, pygame
from pygame.locals import *

pygame.init()

FRAMERATE = 30
clock = pygame.time.Clock()
size = width, height = 800, 480

black = 0, 0, 0
white = 255, 255, 255
light_color = 170, 170, 170
dark_color = 100, 100, 100

screen = pygame.display.set_mode(size)
width = screen.get_width()
height = screen.get_height()

smallfont = pygame.font.SysFont('Corbel', 35)
textA = smallfont.render('A' , True , white)
textB = smallfont.render('B' , True , white)
textC = smallfont.render('C' , True , white)
textD = smallfont.render('D' , True , white)
buttonA = pygame.Rect(600, 430, 40, 40)
buttonB = pygame.Rect(650, 430, 40, 40)
buttonC = pygame.Rect(700, 430, 40, 40)
buttonD = pygame.Rect(750, 430, 40, 40)
selectedButton = buttonB

pygame.mouse.set_visible(False)
running = True

def drawButtons():
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

def setButton(pos):
  global selectedButton

  if (buttonA.collidepoint(pos)):
    selectedButton = buttonA
  elif (buttonB.collidepoint(pos)):
    selectedButton = buttonB
  elif (buttonC.collidepoint(pos)):
    selectedButton = buttonC
  elif (buttonD.collidepoint(pos)):
    selectedButton = buttonD

while running:
    clock.tick(FRAMERATE)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
          running = False
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
          running = False
        elif e.type == MOUSEBUTTONDOWN:
          setButton(e.pos)
        elif e.type == FINGERDOWN:
          setButton((e.x, e.y))

    screen.fill(black)

    # Draw the LFO select buttons
    drawButtons()

    pygame.display.flip()

pygame.quit()
