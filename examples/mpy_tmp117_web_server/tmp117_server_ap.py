
##
# @file mpy_tmp117_server_ap.py
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

# -------------------- Import the necessary modules -------------------- 
from microdot import Microdot, send_file
from microdot.websocket import with_websocket
import json
import asyncio
import wlan_ap
import qwiic_tmp117

# -------------------- Constants -------------------- 
kDoAlerts = True # Set to False to disable checking alerts. This will speed up temperature reads.
kApSsid = "iot_redboard_tmp117" # This will be the SSID of the AP, the "Network Name" that you'll see when you scan for networks on your client device
kApPass = "thermo_wave2" # This will be the password for the AP, that you'll use when you connect to the network from your client device

# -------------------- Shared Variables -------------------- 
# Create instance of our TMP117 device
myTMP117 = qwiic_tmp117.QwiicTMP117()

# Use the Microdot framework to create a web server
app = Microdot()

# -------------------- Fahrenheit to Celcius -------------------- 
def f_to_c(degreesF):
    return (degreesF - 32) * 5/9

def c_to_f(degreesC):
    return (degreesC * 9/5) + 32

# --------------------  Set up the TMP117 -------------------- 
def config_TMP117(tmp117Device, doAlerts):
    """
    @brief Function to configure the TMP117 sensor

    @param tmp117Device The QwiicTMP117 object to be configured.

    @details
    - This function initializes the TMP117 sensor and sets the high and low temperature limits.
    - If doAlerts is set to True, the TMP117 will be set to alert mode.
    """
    print("Setting up TMP117")
    # Create instance of device
    tmp117Device = qwiic_tmp117.QwiicTMP117()

    # Check if it's connected
    if tmp117Device.is_connected() == False:
        print("The TMP117 device isn't connected to the system. Please check your connection")
        exit()

    print("TMP117 device connected!")
        
    # Initialize the device
    tmp117Device.begin()

    if doAlerts:
        tmp117Device.set_high_limit(25.50)
        tmp117Device.set_low_limit(25)

        # Set to kAlertMode or kThermMode
        tmp117Device.set_alert_function_mode(tmp117Device.kAlertMode)

    print("TMP117 Configured!")

# -------------------- Asynchronous Microdot Functions -------------------- 
@app.route('/')
async def index(request):
    """
    @brief Function/Route to the index.html file to serve it as the root page

    @param request The Microdot "Request" object containing details about a client HTTP request.

    @details
    - This function is asynchronous and is called when a client requests the root "/" path from our server.
    - The requested file is located in the "static" directory.
    - The requested file is sent to the client.
    """
    return send_file('static/index.html')

# Create server-side coroutine for websocket to send temperature data to the client 
async def send_temperature(tempSocket):
    """
    @brief Server-side coroutine for websocket to send temperature data to the client.

    @param tempSocket The Microdot "WebSocket" object containing details about the websocket connection.

    @details
    - This coroutine is asynchronous and is started when the client connects to the websocket.
    - It sends temperature data to the client every 0.5 seconds.
    """
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
            await tempSocket.send(data)
            await asyncio.sleep(0.5)

@app.route('/temperature')
@with_websocket
async def handle_limits(request, ws):
    """
    @brief Server-side coroutine for websocket to receive changes to the high and low temperature limits from the client
            
    Since our client code creates a websocket connection to the /temperature route, we'll define our websocket coroutine there

    @param request The Microdot "Request" object containing details about a client HTTP request.
    @param ws The Microdot "WebSocket" object containing details about the websocket connection.

    @details
    - This function is asynchronous and is called when a client requests a file from the server.
    - The requested file is located in the "static" directory.
    - The requested file is sent to the client.
    """
    print("Spawned handle_limits coroutine")
    # We won't start sending data until now, when we know the client has connected to the websocket
    # Let's start the send_temperature coroutine and pass it the websocket object
    asyncio.create_task(send_temperature(ws))
    while True:
            # Lets block here until we receive a message from the client
            data = await ws.receive()
            print("Received new limit: " + data)
            limitJson = json.loads(data)
            # Check if the client sent a new high or low limit, and update the TMP117 accordingly
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

@app.route('/static/<path:path>')
async def static(request, path):
    """
    @brief Function/Route to the static folder to serve up the HTML and CSS files

    @param request The Microdot "Request" object containing details about a client HTTP request.
    @param path The path to the requested file.

    @details
    - This function is asynchronous and is called when a client requests a file from the server.
    - The requested file is located in the "static" directory.
    - The requested file is sent to the client.
    """
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

def run():
    """
    @brief Configure the WLAN, and TMP117 and run the web server
    """
    # Set up the AP
    print("Formatting WIFI")
    accessPointIp = wlan_ap.config_wlan_as_ap(kApSsid, kApPass)
    print("WiFi Configured!")

    # Set up the TMP117
    config_TMP117(myTMP117, kDoAlerts)

    # Print the IP address of the server, port 5000 is the default port for Microdot
    print("\nNavigate to http://" + accessPointIp + ":5000/ to view the TMP117 temperature readings\n")

    # Start the web server
    app.run()

# Finally after we've defined all our functions, we'll call the run function to start the server!
run()
