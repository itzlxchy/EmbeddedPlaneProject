# -----------------------------------------------------------
# ESP32 Arduino-core Makefile for WSL2
# Place this inside the firmware/ folder.
# Your main sketch file must be named firmware.ino
# -----------------------------------------------------------

PORT    = /dev/ttyUSB0       # serial port (check with: ls /dev/ttyUSB*)
FQBN    = esp32:esp32:esp32  # board

ARDUINO_CLI = $(HOME)/bin/arduino-cli

all: compile

compile:
	$(ARDUINO_CLI) compile \
		--fqbn $(FQBN) \
		--output-dir build/ \
		.

flash: compile
	$(ARDUINO_CLI) upload \
		--fqbn $(FQBN) \
		--port $(PORT) \
		--input-dir build/ \
		.

monitor:
	$(ARDUINO_CLI) monitor \
		--port $(PORT) \
		--config baudrate=115200

clean:
	rm -rf build/

usb-list:
	usbipd.exe list

usb-attach:
	usbipd.exe attach --wsl --busid $(ID)