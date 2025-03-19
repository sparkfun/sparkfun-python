##
# @file config_ap_linux.py
# @brief This Python file contains the functions to configure a Raspberry Pi Linux machine as an access point.
# 
# @details This file must be run with sudo rights.
#
# @note This code was tested with a RaspberryPi 4 Model B Running Kernel v6.6, Debian GNU/Linux 12 (bookworm) 
#
# @author SparkFun Electronics
# @date March 2025
# @copyright Copyright (c) 2024-2025, SparkFun Electronics Inc.
#
# SPDX-License-Identifier: MIT
# @license MIT
#

# NOTE: 
# Import the required modules
import os
 
# # Define the default access point settings
kDefaultSsid = "raspberry_pi_tmp117"
kDefaultPassword = "I_Love_Qwiic13"
kDefaultIp = "192.168.4.1/24" # On the raspberry pi we'll configure a static ip address for the access point
kDefaultInterface = "wlan0"

def add_to_network_manager_conf():
    content = ""
    with open("/etc/NetworkManager/NetworkManager.conf", "r") as f:
        content = f.read()

    if ("[main]" in content) and ("dns=dnsmasq" not in content):
        content = content.replace("[main]", "[main]\ndns=dnsmasq")
    elif "[main]" not in content:
        content = "[main]\ndns=dnsmasq\n" + content
    else:
        return
    
    with open("/etc/NetworkManager/NetworkManager.conf", "w") as f:
        f.write(content)

# Return a string representing the url to access the content
def config_wlan_as_ap(ssid=kDefaultSsid, password=kDefaultPassword, ip=kDefaultIp, interface=kDefaultInterface):
    # Install packages that give us the necessary commands for the access point (dnsmasq)
    os.system("sudo apt update")
    os.system("sudo apt install -y dnsmasq")

    # add dnsmasq to /etc/NetworkManager/NetworkManager.conf
    add_to_network_manager_conf()

    # Disable the current instance of dnsmasq such that it doesn't conflict with the one started by network manager
    os.system("sudo systemctl disable dnsmasq")
    os.system("sudo systemctl stop dnsmasq")

    # Use network manager to create a new access point
    os.system(f"nmcli con delete myiot_ap")
    os.system(f"nmcli con add type wifi ifname {interface} mode ap con-name myiot_ap ssid {ssid} autoconnect false")
    os.system(f"nmcli con modify myiot_ap 802-11-wireless.band bg")
    os.system(f"nmcli con modify myiot_ap 802-11-wireless.channel 7")
    os.system(f"nmcli con modify myiot_ap wifi-sec.key-mgmt wpa-psk")
    os.system(f"nmcli con modify myiot_ap wifi-sec.proto rsn")
    os.system(f"nmcli con modify myiot_ap wifi-sec.group ccmp")
    os.system(f"nmcli con modify myiot_ap wifi-sec.pairwise ccmp")
    os.system(f"nmcli con modify myiot_ap wifi-sec.psk {password}")
    os.system(f"nmcli con modify myiot_ap ipv4.method shared ipv4.address {ip}")
    os.system(f"nmcli con modify myiot_ap ipv6.method disabled")
    os.system(f"nmcli con up myiot_ap")

    return ip.split("/")[0]
    
# Now serve our content to the client