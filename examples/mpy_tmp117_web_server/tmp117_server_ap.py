
##
# @file mpy_rgb_ramp.py
# @brief This MicroPython file contains a full implementation of a web server that reads 
# temperature data from a TMP117 sensor and sends it to a client via a websocket.
# The complementary client code that is served can be found in the static directory.
# 
# @details
# This module depends on the qwicc_tmp117 library to control the TMP117 sensor.
#
# @note This code is designed to work with the qwiic_tmp117 library and a compatible microcontroller, such as the
# SparkFun IoT RedBoard - ESP32, or the SparkFun IoT RedBoard - RP2350
#
# @author SparkFun Electronics
# @date March 2025
# @copyright Copyright (c) 2024-2025, SparkFun Electronics Inc.
#
# SPDX-License-Identifier: MIT
# @license MIT
#

from microdot import Microdot, send_file
from microdot.websocket import with_websocket
import json
import asyncio
import wlan_ap
import qwiic_tmp117

# defines
kDoAlerts = True # Set to False to disable checking alerts. This will speed up temperature reads.
kApSsid = "iot_redboard_tmp117"
kApPass = "thermo_wave2"

# fahrenheit to celcius
def f_to_c(degreesF):
    return (degreesF - 32) * 5/9

def c_to_f(degreesC):
    return (degreesC * 9/5) + 32

# Set up the AP
print("Formatting WIFI")
accessPointIp = wlan_ap.config_wlan_as_ap(kApSsid, kApPass)
print("WiFi Configured!")
# print("Active config: ", config)

# Set up the TMP117
print("Setting up TMP117")
# Create instance of device
myTMP117 = qwiic_tmp117.QwiicTMP117()

# Check if it's connected
if myTMP117.is_connected() == False:
    print("The TMP117 device isn't connected to the system. Please check your connection")
    exit()

print("TMP117 device connected!")
    
# Initialize the device
myTMP117.begin()

if kDoAlerts:
    myTMP117.set_high_limit(25.50)
    myTMP117.set_low_limit(25)

    # Set to kAlertMode or kThermMode
    myTMP117.set_alert_function_mode(myTMP117.kAlertMode)

print("TMP117 Configured!")

print("\nNavigate to http://" + accessPointIp + ":5000/ to view the TMP117 temperature readings\n")

# Use the Microdot framework to create a web server
app = Microdot()

# Route our root page to the index.html file
@app.route('/')
async def index(request):
    return send_file('static/index.html')
 
gTempSocket = None

# Create server-side coroutine for websocket to send temperature data to the client 
async def send_temperature():
    print("Spawned send_temperature coroutine")
    while True:
        if myTMP117.data_ready():
            # We'll store all our results in a dictionary so it's easy to dump to JSON
            data = {"tempF": 0, "tempC": 0, "limitH": 75, "limitL": 65, "alertH": False, "alertL": False} 
            data['tempC'] = myTMP117.read_temp_c()
            data['tempF'] = myTMP117.read_temp_f()

            if kDoAlerts:
                await asyncio.sleep(1.5) # This delay between reads to the config register is necessary. see qwiic_tmp117_ex2
                alertFlags = myTMP117.get_high_low_alert() # Returned value is a list containing the two flags
                data['alertL'] = bool(alertFlags[myTMP117.kLowAlertIdx])
                data['alertH'] = bool(alertFlags[myTMP117.kHighAlertIdx])
                data['limitL'] = c_to_f(myTMP117.get_low_limit())
                data['limitH'] = c_to_f(myTMP117.get_high_limit())

            data = json.dumps(data) # Convert to a json string to be parsed by client
            await gTempSocket.send(data)
            await asyncio.sleep(0.5)

# Create server-side coroutine for websocket to receive changes to the high and low temperature limits from the client
# Since our client code creates a websocket connection to the /temperature route, we'll define our websocket coroutine there
@app.route('/temperature')
@with_websocket
async def handle_limits(request, ws):
    print("Spawned handle_limits coroutine")
    global gTempSocket
    gTempSocket = ws # Let's save the websocket object so we can send data to it from our send_temperature coroutine
    # We won't start sending data until now, when we know the client has connected to the websocket
    asyncio.create_task(send_temperature())
    while True:
            data = await ws.receive()
            print("Received new limit: " + data)
            limitJson = json.loads(data)
            if 'low_input' in limitJson:
                toSet = f_to_c(limitJson['low_input'])
                print("setting low limit to: " + str(toSet))
                myTMP117.set_low_limit(toSet)
                print("New low limit: " + str(myTMP117.get_low_limit()))
            if 'high_input' in limitJson:
                toSet = f_to_c(limitJson['high_input'])
                print("setting high limit to: " + str(toSet))
                myTMP117.set_high_limit(toSet)
                print("New high limit: " + str(myTMP117.get_high_limit()))

# Route to the static folder to serve up the HTML and CSS files
@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

def run():
    """
    @brief Run the web server
    """   
    app.run()

run()
