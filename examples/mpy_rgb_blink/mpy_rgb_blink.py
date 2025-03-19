
##
# @file mpy_rgb_blink.py
# @brief This MicroPython file contains functions to control the on-board RGB LED on SparkFun MicroPython
# enabled boards that have a RGB LED.
#
# @details
# This module depends on the available `neopixel` library to control the RGB LED and the on-board
# LED pin defined as "NEOPIXEL" and accessible via the machine module.
#
# @note This code is designed to work with the `neopixel` library and a compatible microcontroller, such as the
# SparkFun IoT RedBoard - ESP32, or the SparkFun IoT RedBoard - RP2350
#
# @author SparkFun Electronics
# @date March 2025
# @copyright Copyright (c) 2024-2025, SparkFun Electronics Inc.
#
# SPDX-License-Identifier: MIT
# @license MIT
#

import machine
import neopixel
import random
import time

BLINK_DELAY = 200  # delay in milliseconds
# ---------------------------------------------------------------------------------


def fade_in_out(led, color, fade_time=1000):
    """
    @brief Fade the LED in and out to a given color.

    @param led The LED object to be controlled. It is expected to be a `neopixel.NeoPixel` object.
    @param color The RGB color to fade to.
    @param fade_time The time in milliseconds for the fade effect. Default is 1000 ms.

    """

    # fade in
    for i in range(0, 256):
        led[0] = (int(color[0] * i / 255), int(color[1]
                  * i / 255), int(color[2] * i / 255))
        led.write()
        time.sleep_ms(fade_time // 256)

    # fade out
    for i in range(255, -1, -1):
        led[0] = (int(color[0] * i / 255), int(color[1]
                  * i / 255), int(color[2] * i / 255))
        led.write()
        time.sleep_ms(fade_time // 256)


def rgb_fade_example(led, count=10):
    """
    @brief Fade the LED in and out random color

    @param led The LED object to be controlled. It is expected to be a `neopixel.NeoPixel` object.
    @param count The number of times to fade the LED. Default is 1.

    """

    led[0] = (0, 0, 0)  # LED OFF
    led.write()

    for i in range(count):
        # generate random RGB values - use a lower range to avoid too bright colors
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)

        fade_in_out(led, (R, G, B))
        print(".", end="")


def blink_the_led(led, count=30):
    """
    @brief Blink the LED with random colors of count times.

    @param led The LED object to be controlled. It is expected to be a `neopixel.NeoPixel` object.
    @param count The number of times to blink the LED. Default is 1.

    """

    led[0] = (0, 0, 0)  # LED OFF
    led.write()

    for i in range(count):
        # generate random RGB values - use a lower range to avoid too bright colors
        R = random.randint(0, 180)
        G = random.randint(0, 180)
        B = random.randint(0, 180)

        led[0] = (R, G, B)  # LED ON
        led.write()

        time.sleep_ms(BLINK_DELAY)

        # restore the color
        led[0] = [0, 0, 0]  # off
        led.write()
        time.sleep_ms(BLINK_DELAY//2)
        print(".", end="")


# ---------------------------------------------------------------------------------
# rgb_blink_example

def rgb_blink_example(led, count=20):
    """
       @brief Demonstrates LED color blinking using the onboard NeoPixel.

       @details
       - Initializes the NeoPixel LED.
       - Blinks the LED through a random color sequence.

    """
    # start at LED off
    led[0] = (0, 0, 0)
    led.write()

    blink_the_led(led, count)
    print()

# ---------------------------------------------------------------------------------
# Run the example when this file is loaded


def run():

    print("-----------------------------------------------------------")
    print("Running the SparkFun RGB blink example...")
    print("-----------------------------------------------------------")
    # the the pin object for the pin defined as "NEOPIXEL"
    try:
        pin = machine.Pin("NEOPIXEL")
    except ValueError:
        print(
            "Error: The NEOPIXEL pin is not defined. Please check your board configuration.")
        exit(0)

    led = neopixel.NeoPixel(pin, 1)  # create a NeoPixel object with 1 LED
    print("Blink the LED with random colors:")
    rgb_blink_example(led)
    print("Fade in and out with random colors:")
    rgb_fade_example(led)
    print("Done!")


run()
