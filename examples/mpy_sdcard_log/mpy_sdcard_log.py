
##
# @file mpy_sdcard_log.py
# @brief This MicroPython file contains functions to manage SD card logging on SparkFun MicroPython
# enabled boards.
#
# @details
# This module provides functionality to mount an SD card, read data from sensors, and log
# the data to a file on the SD card.
#
# @note This code is designed to work with compatible microcontrollers, such as the
# SparkFun IoT RedBoard - ESP32, or the SparkFun IoT RedBoard - RP2350
#
# @author SparkFun Electronics
# @date March 2025
# @copyright Copyright (c) 2024-2025, SparkFun Electronics Inc.
#
# SPDX-License-Identifier: MIT
# @license MIT
#

# NOTE: This example requires the use of the sd card module for micro python. If not installed, the
# module is installed using the following mpremote command:
#    mpremote mip install sdcard

import os
import uos
import time
import random
import json

SDCARD_MOUNT_POINT = "/sdcard"

# global variable to track if the SD card is mounted
_mounted_sd_card = False

# Define the boards we support with this deme - This is a dictionary the key being
# the board uname.machine value, and value a tuple that contains SPI bus number and CS ping number.
SupportedBoards = {
    "SparkFun IoT RedBoard RP2350 with RP2350": (1, 9),
    "SparkFun IoT RedBoard ESP32 with ESP32": (2, 5),
    "Teensy 4.1 with MIMXRT1062DVJ6A": (-1, -1)
}

# ------------------------------------------------------------


def mount_sd_card(spi_bus, cs_pin):

    global _mounted_sd_card
    try:
        import sdcard
    except ImportError:
        print("[Error] sdcard module not found. Please install it.")
        return False

    from machine import Pin, SPI

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
        uos.mount(vfs, SDCARD_MOUNT_POINT)
    except Exception as e:
        print("[Error] Failed to mount the SD Card", e)
        return False

    _mounted_sd_card = True
    return True


def setup_sd_card():
    """
    Mounts an SD card to the filesystem.

    This function checks if the current board is supported, initializes the SPI bus and CS pin,
    creates the SD card object, and mounts the SD card to the filesystem.

    Returns:
        bool: True if the SD card was successfully mounted, False otherwise.

    """

    # is this a supported board?
    board_name = os.uname().machine
    if board_name not in SupportedBoards:
        print("This board is not supported")
        return False

    # Get the SPI bus and CS pin for this board
    spi_bus, cs_pin = SupportedBoards[board_name]

    # do we need to mount the sd card? (Teensy auto mounts)
    status = False
    if spi_bus != -1:
        status = mount_sd_card(spi_bus, cs_pin)
    else:
        status = True

    if status is True:
        print("SD Card mounted successfully")

    return status

# ------------------------------------------------------------


def read_data(observation):
    """
    Simulates the collection of data and adds values to the observation dictionary.

    This function generates simulated data for time, temperature, humidity, and pressure,
    and adds these values to the provided observation dictionary. If connecting to an actual
    sensor, you would take readings from the sensor and add them to the observation dictionary
    within this function.

    Args:
        observation (dict): A dictionary to store the simulated sensor data.

    Returns:
        bool: Always returns True to indicate successful data collection.
    """

    # Note: If connecting to a actual sensor, you would take readings from the sensor and add them to the
    # observation dictionary here.

    # Add the time
    observation["time"] = time.time()

    # Add the temperature
    observation["temperature"] = random.randrange(-340, 1000)/10

    # Add the humidity
    observation["humidity"] = random.randrange(0, 1000)/10.

    # Add the pressure
    observation["pressure"] = random.randrange(10, 1000)/10.

    # Success !
    return True

# ------------------------------------------------------------
# Setup the log file
# This function opens the log file for writing
# and returns the file object.
# If the file cannot be opened, it returns None.


def setup_log_file(filename):
    """
    Sets up a log file on the SD card with the given filename.

    This function attempts to open a file on the SD card for writing. If the file
    cannot be opened, an error message is printed and None is returned.

    Args:
        filename (str): The name of the log file to be created on the SD card.

    Returns:
        file object: A file object for the opened log file if successful, or None if an error occurred.
    """

    try:
        fs = open(SDCARD_MOUNT_POINT + os.sep + filename, "w")
    except Exception as e:
        print("[Error] Failed to open log file:", e)
        return None

    return fs

# ------------------------------------------------------------


def log_data(filename, count=30, interval=50, to_console=True):
    """
    Logs data to a specified file and optionally prints it to the console.

    Parameters:
    filename (str): The name of the file to log data to.
    count (int, optional): The number of times to log data. Default is 30.
    interval (int, optional): The interval (in milliseconds) between each log entry. Default is 50.
    to_console (bool, optional): If True, prints the data to the console. Default is True.

    Returns:
    None
    """

    # Create the observation dictionary
    observation = {}

    # Open the log file
    fs = setup_log_file(filename)
    if fs is None:
        return

    # Loop for the number of times specified
    for i in range(count):

        observation.clear()
        observation["iteration"] = i

        # Read the data
        read_data(observation)

        # Write the data to the log file
        fs.write(json.dumps(observation) + "\n")

        if to_console:
            # Print the data to the console
            print(json.dumps(observation))

        # Wait for the specified interval
        time.sleep(interval)

    # Close the log file
    fs.close()

# ------------------------------------------------------------


def sdcard_log_example(filename="mpy_sdcard_log.txt", count=20, interval=2):
    """
    Logs data to an SD card at specified intervals and prints the data to the console.

    Args:
        filename (str): The name of the file to log data to. Defaults to "mpy_sdcard_log.txt".
        count (int): The number of iterations to log data for. Defaults to 20.
        interval (int): The interval in seconds between each log entry. Defaults to 2.

    Returns:
        None
    """

    global _mounted_sd_card
    print("Logging to: {filename}, every {interval} seconds for {count} iterations.\n".format(
        filename=filename, interval=interval, count=count))
    # Mount the SD card
    if not setup_sd_card():
        print("Failed to mount SD card")
        return

    print("\nLogging Data to SD Card and Console:")

    # Log the data
    log_data(filename, count=count, interval=interval, to_console=True)

    # Unmount the SD card if we need to
    if _mounted_sd_card:
        uos.umount(SDCARD_MOUNT_POINT)
        _mounted_sd_card = False
        print("\nSD Card unmounted successfully")

# ------------------------------------------------------------
# Run method for the example


def run():
    """
    Executes the SparkFun SD card logging example.

    """
    print("-----------------------------------------------------------")
    print("Running the SparkFun sd card logging example...")
    print("-----------------------------------------------------------")

    sdcard_log_example()
    print()
    print("Done!")


# run the demo/example on load
run()
