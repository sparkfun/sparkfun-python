##
# @file config_ap_micropython.py
# @brief This MicroPython file contains the functions to configure a supported MicroPython machine as an access point.
# 
# @details This code depends on the available MicroPython `network` library to configure an access point.
#
# @note This code is designed to work with the available MicroPython `network` library and a compatible microcontroller, such as the
# SparkFun IoT RedBoard - ESP32, or the SparkFun IoT RedBoard - RP2350
#
# @author SparkFun Electronics
# @date March 2025
# @copyright Copyright (c) 2024-2025, SparkFun Electronics Inc.
#
# SPDX-License-Identifier: MIT
# @license MIT
#

import network

# Return a string representing the ip address of the access point
kDefaultSsid = "raspberry_pi_tmp117"
kDefaultPassword = "iot_redboard_tmp117"

def config_wlan_as_ap(ssid = kDefaultSsid, password = kDefaultPassword):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)

    while ap.active() == False:
        pass

    config = ap.ifconfig()

    return str(config[0])
