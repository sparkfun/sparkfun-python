# Using Qwiic with Python on Linux

## Contents
* [Supported Platforms](#hardware)
* [Raspberry Pi Setup](#raspberry-pi-setup)
* [Jetson Orin Nano Setup](#jetson-orin-nano-setup)
* [Qwiic Shim Setup](#qwiic-shim-or-qwiic-cable-female-jumper-setup)
* [Installation](#installation)
* [Drivers](#drivers)

## Supported Platforms
[Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html) , [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html)

## Raspberry Pi Setup
Follow the [instructions here](https://www.raspberrypi.com/software/operating-systems/) to to download a Raspberry PI OS image. It is expected that most/all RaspberryPi OS versions will work with our Qwiic I2C drivers, but testing was done with Kernel v6.6, Debian GNU/Linux 12 (bookworm). Image an SD card with your favorite SD card imager, we recommend the [Raspberry Pi Imager](https://www.raspberrypi.com/software/). 

## Jetson Orin Nano Setup
Follow the [in-depth instructions here](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit#intro) to set up your Jetson Orin Nano Developer kit with a JetPack 6.2 (or higher) Linux image.

## Qwiic Shim or Qwiic Cable Female Jumper Setup
On either of the above platforms, a pysical hardware interface is required to connect the I2C pins of the board to a qwiic connector on a qwiic device. Connect a [Qwiic Shim](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) or a [Qwiic Cable Female Jumper](https://www.sparkfun.com/flexible-qwiic-cable-female-jumper-4-pin.html) to your board, making sure to connect the correct pins for PWR, GND, SDA, and SCL. See the [instructions here](https://learn.sparkfun.com/tutorials/qwiic-shim-for-raspberry-pi-hookup-guide) for more information. Then connect a qwiic cable to your SparkFun Qwiic Device. 

> [!Warning]
> IMPROPER ORIENTATION OF A QWIIC SHIM CAN SHORT POWER TO GROUND, DAMAGING YOUR BOARD!

## Installation
You can install the [qwiic_i2c_py](https://github.com/sparkfun/Qwiic_I2C_Py) package to get Qwiic I2C support for your board. Also check out our comprehensive [qwiic_py](https://github.com/sparkfun/Qwiic_Py) repository. 

The qwiic_i2c_py package is primarily installed using the `pip3` command, downloading the package from the Python Index - "PyPi". 

First, setup a virtual environment from a specific directory using venv:
```sh
python3 -m venv ~/sparkfun_venv
```
You can pass any path instead of ~/sparkfun_venv, just make sure you use the same one for all future steps. For more information on venv [click here](https://docs.python.org/3/library/venv.html).

Next, install the qwiic package with:
```sh
~/sparkfun_venv/bin/pip3 install sparkfun-qwiic-i2c
```
Now you should be able to run any example or custom python scripts that have `import qwiic_i2c` by running e.g.:
```sh
~/sparkfun_venv/bin/python3 example_script.py
```

To get started with any of the Qwiic Drivers, check out our list of Qwiic Python Driver Repos below and follow the device-specific "PyPi Installation" instructions in your device's repository.

As an alternative to pip, at you could also manually clone/download the qwiic_i2c_py repository and the repository for your desired driver and then utilize the qwiic files directly.

## Drivers
Check out our growing list of Python Drivers: [https://github.com/topics/sparkfun-python](https://github.com/topics/sparkfun-python)

