#!/bin/env python
# coding: utf-8
import time
import spidev
import RPi.GPIO

class TpTsc2046SPI:
	def __init__(self, bus, device, pinIrq, callback):
		# initialize spi
		self.spi = spidev.SpiDev()
		self.spi.open(bus, device)
		self.spi.mode = 0b00
		# self.spi.max_speed_hz = 125 * 1000 * 1000
		self.spi.max_speed_hz = int(125 * 1000)
		self.spi.bits_per_word = 8
		self.spi.cshigh = False
		self.spi.lsbfirst = False

		# initialize gpio
		RPi.GPIO.setmode(RPi.GPIO.BCM)
		RPi.GPIO.setup(pinIrq, RPi.GPIO.IN, RPi.GPIO.PUD_UP)
		RPi.GPIO.add_event_detect(pinIrq, RPi.GPIO.FALLING, callback = callback, bouncetime = 50) 
		self.pinIrq = pinIrq

	def __del__(self):
		self.spi.close()

	def createCmd(self, A, Mode, SER):
		return 0x80 | (A << 4) | (Mode << 3) | (SER << 2) | (0 << 0)

	def get(self):
		# the first sent byte is command
		# the last two byte is dummy data to read (MSB must be 0)
		# measure X
		data = self.spi.xfer([self.createCmd(1, 0, 0), 0x00, 0x00])
		posX = ((data[1] << 4) & 0xFF0) | ((data[2] >> 4) & 0x0F)
		posX /= 2048.0
		# print("X = %f" % (posX) )

		# measure Y
		data = self.spi.xfer([self.createCmd(5, 0, 0), 0x00, 0x00])
		posY = ((data[1] << 4) & 0xFF0) | ((data[2] >> 4) & 0x0F)
		posY = posY/2048.0
		# print("Y = %f" % (posY) )

		# measure pressure
		data = self.spi.xfer([self.createCmd(3, 0, 0), 0x00, 0x00])
		press = ((data[1] << 4) & 0xFF0) | ((data[2] >> 4) & 0x0F)
		# print("Press = %d" % (press) )

		if press < 10:
			# released
			return [False, posX, posY]
		else:
			# pressed
			return [True, posX, posY]
