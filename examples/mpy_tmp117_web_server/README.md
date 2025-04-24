
![TMP117-Web-Server](/docs/images/tmp117-web-server.png "TMP117 Web Server")

# MicroPython TMP117 Web Server Example
The mpy_tmp117_web_server demo application configures a MicroPython device or Raspberry Pi as a wireless access point that publishes TMP117 temperature data. The Microdot python web framework is used to set up a web server on your MicroPython or Python board. Static web elements are served to create a Web UI to display data and deliver commands to the device. 

While this simple demo is for the TMP117 and serves temperature data, use it as a starting point to develop your own web application for interfacing with any of our other [MicroPython supported Qwiic Devices](https://github.com/topics/sparkfun-python)!

## Contents

* [Hardware](#hardware)
* [Installation](#installation)
* [Running the Example](#running-the-example)
* [Using the Webpage](#using-the-webpage)
* [Code Explanation](#code-explanation)
* [References and More](#references-and-more)

## Hardware
In order to run this demo you will need:

* [Qwiic Cable](https://www.sparkfun.com/sparkfun-qwiic-cable-kit.html)
* [TMP117 Temperature Sensor](https://www.sparkfun.com/sparkfun-high-precision-temperature-sensor-tmp117-qwiic.html)
* A client computer, phone, tablet, etc. to view the web app.
* EITHER:
    1) MicroPython capable board with a WLAN interface and a [Qwiic Connector](https://www.sparkfun.com/qwiic) or broken-out I2C pins (we reccomend our [IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html) or [IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html)).
    
    OR

    2) A Raspberry Pi with the [Qwiic Shim](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) or a [Qwiic Cable Female Jumper](https://www.sparkfun.com/flexible-qwiic-cable-female-jumper-4-pin.html). Testing was done with a RaspberryPi 4 Model B Running Kernel v6.6, Debian GNU/Linux 12 (bookworm).

Connect the TMP117 to your board with your chosen qwiic method and you're ready to go.

## Installation

### MicroPython
If you are running the demo on a MicroPython board (and you did not purchase one of our boards with MicroPython pre-loaded on the board), first flash your board with MicroPython firmware. See the [most recent release of Sparkfun MicroPython](https://github.com/sparkfun/micropython/releases) and install the .uf2 (for RP2 boards) or .bin files (for ESP32 boards) corresponding to your board.

Next, add the demo files to your board. You can do this manually, by copying the files from this directory (and from [qwiic_i2c_py](https://github.com/sparkfun/Qwiic_I2C_Py) and [qwiic_tmp117](https://github.com/sparkfun/Qwiic_TMP117_Py)) to your board with mpremote or with Thonny or another IDE. 

In any case, after installing, the file structure on your board should look like this:
```
/
   |
   +--- lib/
   |      |--- qwiic_i2c
   |            |--- __init__.py
   |            |--- micropython_i2c.py
   |            `--- i2c_driver.py
   |      |--- microdot
   |            |--- __init__.py
   |            |--- helpers.py
   |            |--- microdot.py
   |            `--- websocket.py
   |      |--- wlan_ap
   |            |--- __init__.py
   |            |--- config_ap_micropython.py
   |            `--- config_ap_linux.py
   |      |--- qwiic_tmp117.py
   |
   +--- static/
   |      |--- index.css
   |      |--- index.html
   |      `--- logo.png
   |
   `--- tmp117_server_ap.py
```

### Raspberry Pi
On a Raspberry Pi running Linux, manually copy the files from this directory as well as those from [qwiic_i2c_py](https://github.com/sparkfun/Qwiic_I2C_Py) and [qwiic_tmp117_py](https://github.com/sparkfun/qwiic_tmp117_py) into the same directory. Alternatively, you can set up a virtual environment and install qwiic_i2c_py and qwiic_tmp117_py in the same venv path with pip3 as instructed in the READMEs for [qwiic_i2c_py](https://github.com/sparkfun/Qwiic_I2C_Py?tab=readme-ov-file#python) and [qwiic_tmp117_py](https://github.com/sparkfun/qwiic_tmp117_py/tree/master?tab=readme-ov-file#python).

If you manually copy the files, your directory structure should look like this:
```
/your-directory-name
   |
   +--- qwiic_i2c
   |        |--- __init__.py
   |        |--- micropython_i2c.py
   |        `--- i2c_driver.py
   +--- microdot
   |        |--- __init__.py
   |        |--- helpers.py
   |        |--- microdot.py
   |        `--- websocket.py
   +--- wlan_ap
   |        |--- __init__.py
   |        |--- config_ap_micropython.py
   |        `--- config_ap_linux.py
   +--- qwiic_tmp117.py
   |
   +--- static/
   |        |--- index.css
   |        |--- index.html
   |        `--- logo.png
   |
   `--- tmp117_server_ap.py
```

If you used pip3 to install qwiic_i2c and qwiic_tmp117, you won't need them in the local directory as shown above (but you will need to run from the virtual environment where you installed them).

## Running the Example

### MicroPython

#### Option 1: Thonny/Other IDE
If using Thonny, connect your board, open the ```tmp117_server_ap.py``` file, and click the green arrow button (run current script).

#### Option 2: Command Line
If using the command line:
1) Execute ```mpremote``` to connect to your board
2) From the REPL, execute the following command to run the example:
```python 
>>> exec(open("tmp117_server_ap.py").read())
```

### Raspberry Pi
Run the file with sudo privileges:
```bash
sudo python3 tmp117_server_ap.py
```

## Using the Webpage
### Connecting
When you start the application, it should print the IP address and port that you should use to connect. For example: 

```Navigate to http://192.168.4.1:5000/ to view the TMP117 temperature readings```

The application will broadcast a wireless network called ```iot_redboard_tmp117``` with the password ```thermo_wave2``` (or whatever you have set as ```kApSsid``` or ```kApPass``` in the constants at the top of the tmp117_server_ap.py file). Connect to this wireless network with the WiFi manager on your client device.

Next, copy and paste (or ctrl+click) the connection link from above into your web browser (or enter it manually in a mobile device).

### Thermometer
The Web Page should pop up and display a thermometer, some input boxes, and some indicator LEDs. The thermometer will show the temperature on a scale of 0 to 100 degrees F. Try breathing on your TMP117 to watch the temperature increase. 

### Limit LEDs and Boxes
To change one of the limit values, enter a number in the corresponding "Set Limit" box and press enter.
After changing one of the values, give several seconds for the server to receive your request,
set the limit on the device, and respond with the value read back from the device to update the "Read Limit" box.

If the temperature drops below the low limit or above the high limit, triggering an alert on the device,
the corresponding alert LED will turn red.
> [!NOTE]
> This simple version of the webserver is only designed to handle a single connection at a time and should be restarted after a client device disconnects. 

## Code Explanation

### Setting Up WLAN as an Access Point (MicroPython)
```python
def config_wlan_as_ap(ssid = kDefaultSsid, password = kDefaultPassword):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)

    while ap.active() == False:
        pass

    config = ap.ifconfig()

    return str(config[0])
```

```tmp117_server_ap.py``` uses the config_wlan_as_ap() function to configure the WLAN as an access point. Notice how simple it is to create the object using the ```network``` module. By passing ```AP_IF``` we choose to set up the WLAN interface 


See the ```wlan_ap/config_ap_linux.py``` file for the analog for Raspberry Pi. It makes use of [nmcli](https://networkmanager.dev/docs/api/latest/nmcli.html) to configure the Raspberry Pi WLAN0 as an access point. We pass our ssid and password to set up our network credentials. We return our IP so we know where to navigate to view our webpage.

### Setting Up the TMP117
First we ensure the TMP117 is properly connected by calling ```tmp117Device.is_connected()```. Then we perform initialization by calling ```tmp117Device.begin()```. Finally, we set up alerts using ```tmp117Device.set_high_limit()```, ```tmp117Device.set_low_limit()```, and ```set_alert_function_mode()```.

### The MicroDot Web Server Framework
[Microdot](https://github.com/miguelgrinberg/microdot) is a minimal Python and MicroPython web framework that allows us to quickly make web apps that can run on platforms with limited resources. It is based around the idea of "routes", such that we can call different asynchronous Python functions when we receive client http requests to different paths. See the [Microdot README](https://github.com/miguelgrinberg/microdot/blob/main/README.md) for more information. 

### Serving Static Web Elements
When a client first connects, it will be to the root path "/" of our web app. We create a route to service this path:
```python
@app.route('/')
async def index(request):
    return send_file('static/index.html')
```

Using the Microdot ```send_file()``` function, we choose display our hompage in ```index.html``` when the user first connects.

We also want to be able to serve an arbitrary number of static web elements for example, the sparkfun logo as well as some styling using css. For this, we create a route to service the "static" path:
```python
@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)
```
This creates a mapping from client requests to all ```static/``` paths and the files on our server in the "static" folder.

### Client-Server Communication with WebSocket
Microdot also allows for easy interfacing with WebSockets. In our ```index.html``` client code, we create a WebSocket at the ```'/temperature``` path. 
In our server code, we create a route for this path and specify that it will be a WebSocket using the ```@with_websocket``` decorator. 
```python
@app.route('/temperature')
@with_websocket
async def handle_limits(request, ws):
```

Now we will have access to the `ws` WebSocket access and can send and receive messages between the server and client using it's `send()` and `receive()` methods.

### Reading and Publishing Temperature
We can read from the TMP117 using the functions defined in the qwiic_tmp117_py library. Often when conveying data over a WebSocket, the JSON format is used because it keeps our messages organized, and there is library suppport for JSON in most programming langauges. So we store our data in a dictionary and use the ```json.dumps()``` and ```tempSocket.send()``` functions to write it over the WebSocket as a JSON string where it can be caught by the client. 

```python
async def send_temperature(tempSocket):
    while True:
        if myTMP117.data_ready():

            data = {"tempF": 0, "tempC": 0, "limitH": 75, "limitL": 65, "alertH": False, "alertL": False} 
            data['tempC'] = myTMP117.read_temp_c()
            data['tempF'] = myTMP117.read_temp_f()

            if kDoAlerts:
                await asyncio.sleep(1.5) 
                alertFlags = myTMP117.get_high_low_alert() 
                data['alertL'] = bool(alertFlags[myTMP117.kLowAlertIdx])
                data['alertH'] = bool(alertFlags[myTMP117.kHighAlertIdx])
                data['limitL'] = c_to_f(myTMP117.get_low_limit())
                data['limitH'] = c_to_f(myTMP117.get_high_limit())

            data = json.dumps(data)
            await tempSocket.send(data)
            await asyncio.sleep(0.5)
```

This asynchronous task is created by the handle_limits function when a client first connects and creates the websocket. 

```python
asyncio.create_task(send_temperature(ws))
```



## References and More
Special thanks to the creators of the MIT-licensed elements below:
* [Miguel Grinberg and Microdot](https://github.com/miguelgrinberg/microdot) for the Microdot Web Framework.
* [Arkellys](https://codepen.io/Arkellys/details/rgpNBK) for the Thermometer HTML/CSS element.
* [Johnny Berkmans](https://codepen.io/berkmansjohnny/details/LzXbPV) for the Indicator LED HTML/CSS elements.

Find a bug or want a feature? [Let us know here](https://github.com/sparkfun/sparkfun-python/issues). Have fun and happy hacking!
