#!/bin/env python
# coding: utf-8

# enable SPI in /boot/config.txt
# git clone git://github.com/doceme/py-spidev
# cd py-spidev
# sudo python setup.py install

import time
import spidev
import RPi.GPIO
import atexit
import LcdIli9341SPI
import TpTsc2046SPI

I2C_LCD = 0
I2C_TP = 1
GPIO_PIN_LCD_DC = 26
GPIO_PIN_TP_IRQ = 19

lcd = None
tp = None

def touchCallback(pin):
	global tp
	# pressed, x, y = tp.get()
	# if pressed:
	# 	print("TP (%f, %f)" % (x, y) )

def initializeDevice():
	global lcd, tp
	lcd = LcdIli9341SPI.LcdIli9341SPI(0, I2C_LCD, GPIO_PIN_LCD_DC)
	tp = TpTsc2046SPI.TpTsc2046SPI(0, I2C_TP, GPIO_PIN_TP_IRQ, touchCallback)
	lcd.initialize()

def main():
	global lcd, tp
	initializeDevice()
	lcd.drawRect(0xFFFF)
	while True:
		pressed, x, y = tp.get()
		if pressed:
			# print("TP (%f, %f)" % (x, y) )
			x = int(x * 320)
			y = int(y * 240)
			lcd.drawRect(0xF800, x, y, x + 1, y + 1)

def atExit():
	print("atExit")
	global lcd, tp
	del lcd
	del tp
	RPi.GPIO.cleanup()

if __name__ == '__main__':
	atexit.register(atExit)
	main()
