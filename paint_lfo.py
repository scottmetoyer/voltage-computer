import sys, pygame, math
from pygame.locals import *
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE
import board
import busio
import adafruit_mcp4728

# Initialize the MCP4728
FULL_VREF_RAW_VALUE = 4095
i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 = adafruit_mcp4728.MCP4728(i2c)
mcp4728.channel_a.vref = adafruit_mcp4728.Vref.INTERNAL
mcp4728.channel_b.vref = adafruit_mcp4728.Vref.INTERNAL
mcp4728.channel_c.vref = adafruit_mcp4728.Vref.INTERNAL
mcp4728.channel_d.vref = adafruit_mcp4728.Vref.INTERNAL
mcp4728.channel_a.gain = 2
mcp4728.channel_b.gain = 2
mcp4728.channel_c.gain = 2
mcp4728.channel_d.gain = 2
mcp4728.save_settings()

pygame.init()
size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
FRAMERATE = 200
NUMBER_OF_POINTS = 20
clock = pygame.time.Clock()

black = 0,0,0
white = 255,255,255
red = 255,0,0
light_color = 170,170,170
dark_color = 60,60,60
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
slider_handles = [
  pygame.Rect(100, 430, 400, 40),
  pygame.Rect(100, 430, 400, 40),
  pygame.Rect(100, 430, 400, 40),
  pygame.Rect(100, 430, 400, 40)
]

max_speed = 5
min_speed = .01
playhead_positions = [0,0,0,0]
cycles_per_second = [.25,.25,.25,.25]

lfos = [
    [100 for x in range(NUMBER_OF_POINTS)],
    [100 for x in range(NUMBER_OF_POINTS)],
    [100 for x in range(NUMBER_OF_POINTS)],
    [100 for x in range(NUMBER_OF_POINTS)]
]

def log_position(value, min_position, max_position, min_value, max_value):
  min_v = math.log(min_value)
  max_v = math.log(max_value)
  scale = (max_v-min_v) / (max_position-min_position)
  return (math.log(value)-min_v) / scale + min_position

def log_value(value, min_position, max_position, min_value, max_value):
  min_v = math.log(min_value)
  max_v = math.log(max_value)
  scale = (max_v-min_v) / (max_position-min_position)
  return math.exp(min_v + scale * (value-min_position))

def translate(value, fromMin, fromMax, toMin, toMax):
  fromSpan = fromMax - fromMin
  toSpan = toMax - toMin
  valueScaled = float(value - fromMin) / float(fromSpan)
  return toMin + (valueScaled * toSpan)

for index, handle in enumerate(slider_handles):
  handle.w = log_position(cycles_per_second[index], 0, 400, min_speed, max_speed)

def update_playhead():
  global playhead_positions

  # Recalculate the step sizes and update the playheads as needed
  for index, position in enumerate(playhead_positions):
    step_size = (width / FRAMERATE) * cycles_per_second[index]
    playhead_positions[index] += step_size

    if (playhead_positions[index] >= width):
      playhead_positions[index] = 0

    pygame.draw.line(screen, light_color, (playhead_positions[index], 0), (playhead_positions[index], width), 1)

  pygame.draw.line(screen, red, (playhead_positions[selected_lfo], 0), (playhead_positions[selected_lfo], width), 1)

def draw_lfo(lfo, color):
  last_point = lfo[0]

  for index, value in enumerate(lfo):
    gap = width // NUMBER_OF_POINTS
    x = index * (gap + 2)
    pygame.draw.circle(screen, color, (x + 2, value), 5)
    pygame.draw.line(screen, color, (x-gap, last_point), (x, value), 2)
    last_point = value

def draw_lfos():
  for lfo in lfos:
    draw_lfo(lfo, dark_color)

  draw_lfo(lfos[selected_lfo], light_color)

def draw_controls():
  pygame.draw.rect(screen, dark_color, slider_container)

  for index, button in enumerate(select_buttons):
    if (index == selected_lfo):
      pygame.draw.rect(screen, light_color, button)
      pygame.draw.rect(screen, light_color, slider_handles[selected_lfo])
    else:
      pygame.draw.rect(screen, dark_color, button)

    screen.blit(button_text[index], (button.x + 12, 439))

def set_button(pos):
  global selected_lfo

  for index, button in enumerate(select_buttons):
    if (button.collidepoint(pos)):
      selected_lfo = index

def set_speed_slider(pos):
  global cycles_per_second
  global slider_handles

  if (slider_container.collidepoint(pos)):
    slider_handles[selected_lfo].w = pos[0] - 100
    cycles_per_second[selected_lfo] = log_value(slider_handles[selected_lfo].w, 0, 400, min_speed, max_speed)

def set_lfo_point(pos):
  global lfos
  (x,y) = pos
  gap = width // NUMBER_OF_POINTS
  index = x // gap
  lfos[selected_lfo][index] = y

def touch_handler(event, touch):
  if event == TS_PRESS:
    if (touch.y > 428):
      set_button((touch.x, touch.y))
      set_speed_slider((touch.x, touch.y))
    else:
      set_lfo_point((touch.x, touch.y))
  if event == TS_RELEASE:
      print("Got release", touch)
  if event == TS_MOVE:
    if (touch.y < 428):
      set_lfo_point((touch.x, touch.y))
    else:
      set_speed_slider((touch.x, touch.y))

def send_dac_voltage():
  mcp4728.channel_a.raw_value = int(FULL_VREF_RAW_VALUE / 2)
  mcp4728.channel_b.raw_value = int(FULL_VREF_RAW_VALUE / 2)
  mcp4728.channel_c.raw_value = int(FULL_VREF_RAW_VALUE / 2)
  mcp4728.channel_d.raw_value = int(FULL_VREF_RAW_VALUE / 2)

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
  draw_controls()
  draw_lfos()
  update_playhead()
  send_dac_voltage()
  pygame.display.flip()

pygame.quit()
ts.stop()
exit()