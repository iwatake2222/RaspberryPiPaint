#!/bin/env python
# coding: utf-8
import time
import spidev
import RPi.GPIO

class TpTsc2046SPI:
	def __init__(self, bus, device, pinCs, pinIrq, callback):
		# initialize spi
		self.spi = spidev.SpiDev()
		self.spi.open(0, 1)
		self.spi.mode = 0b00
		# self.spi.max_speed_hz = 125 * 1000 * 1000
		self.spi.max_speed_hz = int(125 * 1000)
		self.spi.bits_per_word = 8
		self.spi.cshigh = False
		self.spi.lsbfirst = False

		# initialize gpio
		RPi.GPIO.setmode(RPi.GPIO.BCM)
		RPi.GPIO.setup(pinCs, RPi.GPIO.OUT)
		RPi.GPIO.setup(pinIrq, RPi.GPIO.IN, RPi.GPIO.PUD_UP)
		RPi.GPIO.add_event_detect(pinIrq, RPi.GPIO.FALLING, callback = callback, bouncetime = 50) 
		self.pinCs = pinCs
		self.pinIrq = pinIrq
		self.disableCS()

	def __del__(self):
		self.spi.close()

	def enableCS(self):
		RPi.GPIO.output(self.pinCs, 0)

	def disableCS(self):
		RPi.GPIO.output(self.pinCs, 1)

	def createCmd(self, A, Mode, SER):
		return 0x80 | (A << 4) | (Mode << 3) | (SER << 2) | (0 << 0)

	def get(self):
		self.enableCS()
		# measure X
		self.spi.writebytes([self.createCmd(1, 0, 0),])
		data = self.spi.readbytes(2)
		posX = ((data[0] << 4) & 0xFF0) | ((data[1] >> 4) & 0x0F)
		posX /= 2048.0
		# print("X = %f" % (posX) )

		# measure Y
		self.spi.writebytes([self.createCmd(5, 0, 0),])
		data = self.spi.readbytes(2)
		posY = ((data[0] << 4) & 0xFF0) | ((data[1] >> 4) & 0x0F)
		posY = posY/2048.0
		# print("Y = %f" % (posY) )

		# measure pressure
		self.spi.writebytes([self.createCmd(3, 0, 0),])
		data = self.spi.readbytes(2)
		press = ((data[0] << 4) & 0xFF0) | ((data[1] >> 4) & 0x0F)
		# print("Press = %d" % (press) )

		self.disableCS()

		if press < 10:
			# released
			return [False, posX, posY]
		else:
			# pressed
			return [True, posX, posY]
