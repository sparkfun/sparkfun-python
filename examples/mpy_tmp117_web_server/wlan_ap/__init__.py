
##
# @file wlan_ap/__init__.py
# @brief This Python file impoprts the correct config_wlan_as_ap function based on the platform.
# 
# @author SparkFun Electronics
# @date March 2025
# @copyright Copyright (c) 2024-2025, SparkFun Electronics Inc.
#
# SPDX-License-Identifier: MIT
# @license MIT
#

from sys import platform

if platform.startswith("linux"):
    from .config_ap_linux import config_wlan_as_ap
else:
    from .config_ap_micropython import config_wlan_as_ap