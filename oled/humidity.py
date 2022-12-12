#!/usr/bin/python

import sys
import os
import time
import Adafruit_DHT

from time import sleep
from PIL import ImageFont, ImageDraw, Image


FILE_CSV="/home/luis/robot/humidity.csv"

# how often we refresh the info in the LCD, in secs
REFRESH_DATA=60

# Temp and Humidity sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#  Font size
FONT_BODY_SIZE=18
FONT_HEADER_SIZE=10
FONT_DELIM_SIZE=18

font_header = ImageFont.truetype('lib_oled96/FreeSans.ttf', FONT_HEADER_SIZE)
font_body   = ImageFont.truetype('lib_oled96/FreeSans.ttf', FONT_BODY_SIZE)
font_delim  = ImageFont.truetype('lib_oled96/FreeSans.ttf', FONT_DELIM_SIZE)


from datetime import datetime

sys.path.append('./lib_oled96')
from lib_oled96 import ssd1306
from smbus import SMBus                  #  These are the only two variant lines !!
i2cbus = SMBus(1)                        #  1 = Raspberry Pi but NOT early REV1 board

oled = ssd1306(i2cbus)

# Ein paar Abkurzungen, um den Code zu entschlacken
draw = oled.canvas

# Display zum Start loschen
oled.cls()
#draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=20, fill=0)
draw.text((5, oled.height/2), 'Retriving data ...',body=font_header, fill=1)
oled.display()

# public file var
f = None ;

def OpenFile( file ):
  try:
      global f
      f = open( file, 'a+')
      if os.stat( file ).st_size == 0:
         f.write('Date,Time,Temperature,Humidity\r\n')
  except:
      print("Failed to open file "+file)
      os._exit(1)
  return

# print("W={0:d}, w={1:d}".format(oled.width,w))
# print("humidity="+strhumidity)
# print("temperature="+strtemperature)
# print("Screen WxH={0:d}x{1:d}, TXT WxH={2:d}x{3:d}".format(oled.width,oled.height,w,h))

OpenFile (FILE_CSV);

counter = REFRESH_DATA
while True:

    # headers: date and time
    now = datetime.now() # current date and time
    strdate=now.strftime("%m %a %Y")
    strtime=now.strftime("%H:%M:%S")

    w, h = draw.textsize(strtime,font=font_header)

    # clean the header
    draw.rectangle((0, 0, oled.width-1, h), outline=20, fill=0)
    draw.text((0, 0), strdate,body=font_header, fill=1)
    draw.text((oled.width-w, 0), strtime, font=font_header, fill=1)

    if counter == REFRESH_DATA:
       humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
       if humidity is not None and temperature is not None:

           draw.rectangle((0, h, oled.width-1, oled.height-1), outline=20, fill=0)
           # body: Humidity and Temperature
           strhumidity="{:.1f}".format(humidity)+"%"
           strtemperature="{:.1f}".format(temperature)+chr(176)+"C"
           w, h = draw.textsize(strtemperature,font=font_body)
           draw.text((0, ((oled.height/2)-(h/3))), strhumidity, font=font_body,  fill=1)

           w2, h2 = draw.textsize(strhumidity,font=font_body)
           # we draw "/" in the middle of the space available between both temperarure and humedity
           draw.text((w2+(((oled.width-w)-w2)/2), ((oled.height/2)-(h/3))), "/", font=font_delim, fill=1)
           draw.text((oled.width-w, ((oled.height/2)-(h/3))), strtemperature, font=font_body,  fill=1)

           f.write('{0},{1},{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity))
       #else:
       #    draw.text((10, 25), "Error in Sensor.", font=font_body, fill=1)
       #    print("Failed to retrieve data from humidity sensor")
       counter=0
    else:
       counter += 1
    oled.display()
