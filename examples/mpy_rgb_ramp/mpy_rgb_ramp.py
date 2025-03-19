
##
# @file mpy_rgb_ramp.py
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
import time

# ---------------------------------------------------------------------------------
# Wink the LED by turning it off and


def wink_led(led):
    """
    @brief Wink the LED by turning it off and on three times.

    @param led The LED object to be controlled. It is expected to be a `neopixel.NeoPixel` object.

    @details
    - Saves the current color of the LED.
    - Turns the LED off and on three times with a delay of 100 milliseconds between each state change.
    - Restores the LED to its original color after winking.

    """

    # safe the current color
    cur_clr = led[0]

    # wink the LED ... off and on three times
    for i in range(0, 3):
        led[0] = [0, 0, 0]  # off
        led.write()

        time.sleep_ms(100)

        # restore the color
        led[0] = cur_clr
        led.write()
        time.sleep_ms(100)

# ---------------------------------------------------------------------------------
# Transition the current LED value to a given RGB value.
# This function assumes pixel color/channel values are 8 bit (0-255)
#


def led_transition(led, R, G, B):
    """
        @brief Transition the current LED value to a given RGB value.

        This function assumes pixel color/channel values are 8-bit (0-255).

        @param led The LED object to be controlled. It is expected to be a `neopixel.NeoPixel` object.
        @param R The target red color value (0-255).
        @param G The target green color value (0-255).
        @param B The target blue color value (0-255).

        @details
        - Retrieves the current color of the LED
        - transitions the current color to the provided color over a series of increments.
        - Also outputs a dot for each increment to indicate progress.

        @example
        @code
        led_transition(led, 255, 0, 0);  // Transition to red color
        @endcode
        """

    #  get current led value - which is a tuple
    #  Note - we convert to a list to support value assignment below.
    clrCurrent = list(led[0])

    # How many increments during the transition
    inc = 51  # 255/5

    # how much to change a color component value every increment
    rInc = (R - clrCurrent[0]) / inc
    gInc = (G - clrCurrent[1]) / inc
    bInc = (B - clrCurrent[2]) / inc

    # loop - adjust color during each increment.
    for i in range(0, inc):

        # add the desired increment to each color component value. Use round() to convert the float value to an integer
        clrCurrent[0] = round(clrCurrent[0] + rInc)
        clrCurrent[1] = round(clrCurrent[1] + gInc)
        clrCurrent[2] = round(clrCurrent[2] + bInc)

        # set the new LED color and write (enable) it
        led[0] = clrCurrent
        led.write()

        # indicate process ... add a small delay
        print(".", end='')
        time.sleep_ms(20)


# ---------------------------------------------------------------------------------
# rgp_ramp_example

def rgb_ramp_example():
    """
       @brief Demonstrates LED color transitions using the onboard NeoPixel.

       @details
       - Initializes the NeoPixel LED.
       - Transitions the LED through a series of colors: Blue, Red, Green, Yellow, White, and Off.
       - Winks the LED (turns it off and on three times) after each color transition.

       """

    # the the pin object for the pin defined as "NEOPIXEL"
    try:
        pin = machine.Pin("NEOPIXEL")
    except ValueError:
        print(
            "Error: The NEOPIXEL pin is not defined. Please check your board configuration.")
        return

    led = neopixel.NeoPixel(pin, 1)  # create a NeoPixel object with 1 LED

    # start at LED off
    led[0] = (0, 0, 0)
    led.write()

    print()
    print("RGB LED Color Transitions:")

    time.sleep_ms(100)

    # transition through a series of colors
    print("\t<Off>\t", end='')
    led_transition(led, 0, 0, 255)
    print(" <Blue>")
    wink_led(led)

    print("\t<Blue>\t", end='')
    led_transition(led, 255, 0, 0)
    print(" <Red>")
    wink_led(led)

    print("\t<Red>\t", end='')
    led_transition(led, 0, 255, 0)
    print(" <Green>")
    wink_led(led)

    print("\t<Green>\t", end='')
    led_transition(led, 255, 255, 0)
    print(" <Yellow>")
    wink_led(led)

    print("\t<Yellow>", end='')
    led_transition(led, 255, 255, 255)
    print(" <White>")
    wink_led(led)

    print("\t<White>\t", end='')
    led_transition(led, 0, 0, 0)
    print(" <Off>")

    # turn off the LED
    led[0] = (0, 0, 0)
    led.write()


# ---------------------------------------------------------------------------------
# Run the example when this file is loaded
print("-----------------------------------------------------------")
print("Running the SparkFun RGB ramp example...")
print("-----------------------------------------------------------")
rgb_ramp_example()
print("Done!")
