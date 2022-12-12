#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
import Adafruit_DHT
sys.path.append('./lib_oled96')

# Bibliotheken importieren
from lib_oled96 import ssd1306
from smbus import SMBus

# Display einrichten
i2cbus = SMBus(1)            # 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1
oled = ssd1306(i2cbus)

# Ein paar Abkürzungen, um den Code zu entschlacken
draw = oled.canvas

# Display zum Start löschen
oled.cls()
oled.display()

# Formen zeichnen
draw.line((4, 2, 20, oled.height-1), fill=1)                    # diagonale Linie
draw.rectangle((22, 2, 30, oled.height-1), outline=1, fill=0)    # Rechteck
draw.rectangle((32, 2, 40, oled.height-1), outline=0, fill=1)    # Rechteck, ausgefüllt
draw.ellipse((42, 2, 60, oled.height-1), outline=1, fill=0)        # Ellipse
draw.line((76, 2, 76, 63), fill=1)                                # vertikale Linie
draw.arc((62, 2, 90, 63), -90, 90, fill=1)                        # Bogen
draw.polygon([(92, 63), (110, 63), (101, 2)], outline=1, fill=0) # Polygon (Dreieck)

# Ausgaben auf Display schreiben
oled.display()
