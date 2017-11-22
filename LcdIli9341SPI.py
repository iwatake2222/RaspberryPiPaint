#!/bin/env python
# coding: utf-8
import time
import spidev
import RPi.GPIO

LCD_WIDTH = 320
LCD_HEIGHT = 240

class LcdIli9341SPI:
	def __init__(self, bus, device, pinCs, pinDc):
		# initialize spi
		self.spi = spidev.SpiDev()
		self.spi.open(0, 0)
		self.spi.mode = 0b00
		# self.spi.max_speed_hz = 125 * 1000 * 1000
		self.spi.max_speed_hz = int(62.5 * 1000 * 1000)
		self.spi.bits_per_word = 8
		self.spi.cshigh = False
		self.spi.lsbfirst = False

		# initialize gpio
		RPi.GPIO.setmode(RPi.GPIO.BCM)
		RPi.GPIO.setup(pinCs, RPi.GPIO.OUT)
		RPi.GPIO.setup(pinDc, RPi.GPIO.OUT)
		self.pinCs = pinCs
		self.pinDc = pinDc
		self.disableCS()

		# do not initialize here, to avoid conflict with other SPI devices
		# initialize device
		# self.initialize()

	def __del__(self):
		self.spi.close()

	def writeCmd(self, cmd):
		RPi.GPIO.output(self.pinDc, 0)
		if isinstance(cmd, list):
			self.spi.writebytes(cmd)
		else:
			self.spi.writebytes([cmd,])

	def writeData(self, data):
		RPi.GPIO.output(self.pinDc, 1)
		if isinstance(data, list):
			self.spi.writebytes(data)
		else:
			self.spi.writebytes([data,])

	def enableCS(self):
		RPi.GPIO.output(self.pinCs, 0)

	def disableCS(self):
		RPi.GPIO.output(self.pinCs, 1)

	def initialize(self):
		self.enableCS()
		self.writeCmd(0x01)
		time.sleep(0.05)
		self.writeCmd(0x11)
		time.sleep(0.05)
		self.writeCmd(0xB6)
		self.writeData([0x0A, 0xC2])
		self.writeCmd(0x36)
		self.writeData(0x68)
		self.writeCmd(0x3A)
		self.writeData(0x55)
		self.setArea(0, 0, LCD_WIDTH - 1, LCD_HEIGHT - 1)
		self.writeCmd(0x29)
		self.writeCmd(0x2C)
		self.disableCS()
		self.drawRect(0x0000)

	def setArea(self, x0, y0, x1, y1, setCs = False):
		if setCs:
			self.enableCS()
		self.writeCmd(0x2A)
		self.writeData([(x0 >> 8) & 0xFF, x0 & 0xFF, (x1 >> 8) & 0xFF, x1 & 0xFF])
		self.writeCmd(0x2B)
		self.writeData([(y0 >> 8) & 0xFF,  y0 & 0xFF, (y1 >> 8) & 0xFF, y1 & 0xFF])
		self.writeCmd(0x2C)
		if setCs:
			self.disableCS()


	def drawBuffer(self, buffer, x0 = 0, y0 = 0, x1 = LCD_WIDTH - 1, y1 = LCD_HEIGHT - 1):
		self.enableCS()
		self.setArea(x0, y0, x1, y1)
		RPi.GPIO.output(self.pinDc, 1)
		width = x1 - x0 + 1
		height = y1 - y0 + 1
		for y in range(height):
			self.spi.writebytes(buffer[ 2 * y * width : 2 * (y + 1) * width])
		self.disableCS()

	def drawRect(self, color, x0 = 0, y0 = 0, x1 = LCD_WIDTH - 1, y1 = LCD_HEIGHT - 1):
		width = x1 - x0 + 1
		height = y1 - y0 + 1
		buffer = [(color >> 8) & 0xFF, (color >> 0) & 0xFF] * width * height
		self.drawBuffer(buffer, x0, y0, x1, y1)

