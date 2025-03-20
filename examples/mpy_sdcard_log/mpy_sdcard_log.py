

import machine
from machine import Pin, SPI
import sdcard


import os
import uos
import time

# Define the boards we support with this deme - This is a dictionary the key being
# the board uname.machine value, and value a tuple that contains SPI bus number and CS ping number.
SupportedBoards = {
    "SparkFun IoT RedBoard RP2350 with RP2350": (1, 9),
    "SparkFun IoT RedBoard ESP32 with ESP32": (2, 5)
}


def mount_sd_card():

    # is this a supported board?
    board_name = os.uname().machine
    if board_name not in SupportedBoards:
        print("This board is not supported")
        return False

    # Get the SPI bus and CS pin for this board
    spi_bus, cs_pin = SupportedBoards[board_name]

    # Create the SPI object
    spi = SPI(spi_bus, baudrate=1000000, polarity=0, phase=0)
    # Create the CS pin object
    cs = Pin(cs_pin, Pin.OUT)

    # Create the SD card object
    try:
        sd = sdcard.SDCard(spi, cs)
    except Exception as e:
        print("[Error] ", e)
        return False

    # Mount the SD card
    try:
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd")
    except Exception as e:
        print("[Error] Failed to mount the SD Card", e)
        return False

    print("SD Card mounted successfully")

    return True
