# Author: David Garufi, April 2020

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import spidev
from time import sleep
from lib_tft24T import TFT24T
import RPi.GPIO as GPIO

from Button import Button
from WFAdjust import WFAdjust

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Connections
MOTOR_PU = 40
MOTOR_DR = 40
MOTOR_EN = 40

# Raspberry Pi configuration.
# For LCD TFT SCREEN:
DC = 24
RST = 25
LED = 15
PEN = 26  # For PEN TOUCH

# Create TFT LCD/TOUCH object:
TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)

# Initialize display.
TFT.initLCD(DC, RST, LED)
TFT.initTOUCH(PEN)

# Get the PIL Draw object to start drawing on the display buffer.
draw = TFT.draw()

# Splash
TFT.clear()
font18 = ImageFont.truetype('FreeSans.ttf', 18)
font12 = ImageFont.truetype('FreeSans.ttf', 12)
draw.textwrapped((12, 20), "Ventilator Proof of Concept", 27, 20, font18, "#FF0000")  # a bit narrower for portrait!
draw.textwrapped((80, 40), "(c) David Garufi", 27, 20, font12, "#FF0000")  # a bit narrower for portrait!
TFT.display()
sleep(1)

# Buttons
#B1 = Button(draw, TFT, (50, 50), (10, 80), "+", "blue")
#B2 = Button(draw, TFT, (50, 50), (70, 80), "-", (0, 80, 0))

# Scenes
WFA = WFAdjust(draw, TFT)


while 1:
    # if B1.check_pos(pos) == 1:
    #     print("Button 1!")
    # if B2.check_pos(pos) == 1:
    #     print("Button 2!")

    sleep(.1)

#        All colours may be any notation (exc for clear() function):
#        (255,0,0)  =red    (R, G, B) - a tuple
#        0x0000FF   =red    BBGGRR   - note colour order
#        "#FF0000"  =red    RRGGBB   - html style
#        "red"      =red    html colour names, insensitive
