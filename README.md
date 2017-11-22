# Paint on Raspberry Pi
Paint application on Raspberry Pi

<img src = "00_doc\pic.jpg">

## Environment
- Raspberry Pi Zero W (may work on Pi2 and 3 as well)
- Python
	- RPi.GPIO
	- py-spidev

## What is implemented
- LCD (Ili9341 SPI) Device Driver
- Touch Panel (TSC2046 / ADS7843) Device Driver
- Main application

## How to Run this application
`> python main.py`

## Needed preparation
- enable SPI
	- edit /boot/config.txt or `sudo raspi-config`
- install RPi.GPIO (might be already installed on stretch)
- install py-spidev

```
sudo apt-get install python-rpi.gpio
git clone git://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install
```