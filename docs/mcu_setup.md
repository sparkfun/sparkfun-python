# Setup and Using MicroPython

## Contents
* [Supported Platforms](#hardware)
* [Latest MicroPython Firmware Downloads](#latest-micropython-firmware-downloads)
* [Suggested Development Environments](#suggested-development-environments)
* [Drivers](#drivers)

## Supported Platforms
 [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html)

## Latest MicroPython Firmware Downloads 
Get our latest MicroPython firmware for your board from our [MicroPython release page](https://github.com/sparkfun/micropython/releases). Different platforms have different methods of flashing:


### RP2 Boards
While connected to your computer, hold the "boot" button on the RP2 board while you press and release the "reset" button to enter bootloader mode. Your board will appear as a regular drive on your computer that you can add files to. Drag and drop the correct .uf2 file from the most recent release from the link above onto your board and it will reboot, now running MicroPython. 

Connect to it with one of the [suggested development environments](#suggested-development-environments) below.  

### ESP32 Boards
Download the .zip archive for your board from the release link above and extract it. If you have not already, [download the esptool utility](https://docs.espressif.com/projects/esptool/en/latest/esp32/installation.html). Then, use ```esptool``` to flash your board using the command specified in the README.md contained in the .zip archive you downloaded for your board. Make sure you run the command from within that directory as well. For example, one ESP32 release contains a `bootloader.bin`, `partition-table.bin`, `micropython.bin`, and `README.md`. By reading the `README.md` I see that the command I must run FROM WITHIN THIS EXTRACTED DIRECTORY is:

```python -m esptool --chip esp32 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 4MB --flash_freq 40m 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 micropython.bin```

## Suggested Development Environments

### Thonny
[Thonny](https://thonny.org/) is an IDE that provides a GUI environment for MicroPython development. Connect your board with MicroPython firmware to your computer and then configure your interpreter by clicking the bottom right-hand corner of Thonny.

![thonny-boards](/docs/images/thonny-board.png "Thonny Boards")

Select the version of MicroPython that makes the most sense for your board. Not sure? Select ```MicroPython (generic)```.

This will connect to your board and show a Python REPL in the "shell" tab. To run a MicroPython program, open it from the ```MicroPython device``` tab. Then press the green arrow (Run Current Script). If you ever want to stop the running program, soft reset your board, or reconnect to your board, click the red stop sign (Stop/Restart backend).

### MicroPython remote control: mpremote
[mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) is a command line utility that provides tons of options for interfacing with a MicroPython board. A simple way to use it is to execute it standalone with no options. If you have installed mpremote you can simply execute ```mpremote``` in a command line to get direct access to the Python REPL on your board. A useful way to navigate the file system from this repl is to execute ```import os``` and then use the `os` methods. For example, ```os.listdir()``` will show everything in the current directory on your MicroPython board. ```os.getcwd()``` will print the name of the current directory and ```os.chdir('dir_name')``` will change the directory. An example of navigating around directories for a user who has installed the [mpy_tmp117_web_server](https://github.com/sparkfun/sparkfun-python/tree/main/examples/mpy_tmp117_web_server) demo from this repository can be seen below.

```
C:\Users\qwiic_guy> mpremote

Connected to MicroPython at COM14
Use Ctrl-] or Ctrl-x to exit this shell
MicroPython on SparkFun IoT RedBoard RP2350 with RP2350
Type "help()" for more information.
>>>
>>>
>>> import os
>>> os.listdir()
['lib', 'static', 'tmp117_server_ap.py']
>>> os.getcwd()
'/'
>>> os.chdir('static')
>>> os.getcwd()
'/static'
>>> os.listdir()
['index.css', 'index.html', 'logo.png']
```

Once you have navigated to the directory containing the python script that you want to run, run it with the exec command: 

```
>>> exec(open('your_script.py').read())
```

To get files from your computer onto your micropython board you can use ```mpremote cp``` or install them directly from repositories that support mip installation with ```mpremote mip install github:reponame``` for example, to install our qwiic_i2c_py driver, execute 

```
mpremote mip install github:sparkfun/qwiic_i2c_py
```

## Drivers
Check out our growing list of Python Drivers: [https://github.com/topics/sparkfun-python](https://github.com/topics/sparkfun-python)


