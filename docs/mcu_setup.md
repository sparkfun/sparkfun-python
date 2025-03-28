# Setup and Using MicroPython

## Contents
* [Supported Platforms](#hardware)
* [Latest MicroPython Firmware Downloads](#latest-micropython-firmware-downloads)
    * [RP2 Boards](#rp2-boards)
    * [ESP32 Boards](#esp32-boards)
* [Suggested Development Environments](#suggested-development-environments)
* [Drivers](#drivers)

## Supported Platforms
 [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html)

 And more to come...

## Latest MicroPython Firmware Downloads 
Get our latest MicroPython firmware for your board from our [MicroPython release page](https://github.com/sparkfun/micropython/releases). Different platforms have different methods of flashing:


### RP2 Boards
While connected to your computer, hold the "boot" button on the RP2 board while you press and release the "reset" button to enter bootloader mode. Your board will appear as a regular drive on your computer that you can add files to. Drag and drop the correct .uf2 file from the most recent release from the link above onto your board and it will reboot, now running MicroPython. 

Connect to it with one of the [suggested development environments](#suggested-development-environments) below.  

### ESP32 Boards
Download the .zip archive for your board from the release link above and extract it. If you have not already, [download the esptool utility](https://docs.espressif.com/projects/esptool/en/latest/esp32/installation.html). Then, use ```esptool``` to flash your board using the command specified in the README.md contained in the .zip archive you downloaded for your board. Make sure you run the command from within that directory as well. For example, one ESP32 release contains a `bootloader.bin`, `partition-table.bin`, `micropython.bin`, and `README.md`. By reading the `README.md` I see that the command I must run FROM WITHIN THIS EXTRACTED DIRECTORY is:

```python -m esptool --chip esp32 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 4MB --flash_freq 40m 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 micropython.bin```

Connect to it with one of the [suggested development environments](#suggested-development-environments) below.  

## Suggested Development Environments

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

Other MicroPython development environments like the IDE's below will also provide you with a REPL where you can directly execute MicroPython commands. So skills gained from navigating the REPL directly with `mpremote` will carry over into other environments.

To get files from your computer onto your micropython board you can use ```mpremote cp``` or install them directly from repositories that support mip installation with ```mpremote mip install github:reponame``` for example, to install our qwiic_i2c_py driver, execute 

```
mpremote mip install github:sparkfun/qwiic_i2c_py
```

Let's walk through a quick example where we develop a program on a local code editor and then run it on a MicroPython board.

We can either develop our files first and then manually copy them over to our board (with `mpremote cp`) each time we want to test them, or we can "mount" a directory such that files are "shared" between the local file system and the MicroPython board. 

Let's explore using [mpremote mount](https://docs.micropython.org/en/latest/reference/mpremote.html#mpremote-command-mount) to map a local directory onto our remote device. First create a new directory named `hello_world` and then open it in your code editor of choice. Now lets add our Python/MicroPython program. Add a file called `print_platform.py` to your hello_world directory. Paste the following code into the file: 

```python
import sys

print ("Hello from (Micro)Python! I am running on the following platform:", sys.platform)
```

The `sys` module exists both in Python and MicroPython so this code can run on both, and will let us know if we are successfully running it on an MCU. `sys.platform` will display your computer's OS if we interpret this program with a Python interpreter on your computer (for example on Windows it is `win32` and on linux it is `linux` or `linux2`). However, if we interpret/execute it via MicroPython on your MCU, it will be the MicroPython port representing your MCU (for example for RP2350 it is `rp2` and for ESP32 it is `esp32`).

Now, my local directory structure in my code editor looks like this:
![sublime-print-platform](/docs/images/sublime-print-platform.png "sublime-print-platfrom")

If I run `mpremote` and use `os.listdir` to list the current contents on my board, I see that it is empty:
```
C:\Users\awesome_qwiic_user> mpremote
Connected to MicroPython at COM14
Use Ctrl-] or Ctrl-x to exit this shell

>>> import os
>>> os.listdir()
[]
>>>
```

Now let's mount our directory. Issue `mpremote mount {path to your hello_world directory}`. When we issue the command and again view the contents on our board, we see that our file has appeared!

![mpremote-mount](/docs/images/mpremote-mount.png "mpremote-mount")

Notice that our file `print_platform.py` is now accessible to us from our MicroPython board and how we have automatically been moved into a directory called `/remote` on the remote device that maps to the local `hello_world` directory.

Now let's run our file using the same `exec(open('print_platform.py').read())` and see what happens. 

```
>>> exec(open('print_platform.py').read())
Hello from (Micro)Python! I am running on the following platform: rp2
```

If all went well, we'll see our hello message and the name of an MCU platform (in this case RP2 for the RP2350).

You can add any number of files in your local code-editor, and modify them as you wish and the changes will be reflected "on-the-fly" in your mpremote session. 

### Thonny
[Thonny](https://thonny.org/) is an IDE that provides a GUI environment for MicroPython development. Connect your board with MicroPython firmware to your computer and then configure your interpreter by clicking the bottom right-hand corner of Thonny.

![thonny-boards](/docs/images/thonny-board.png "Thonny Boards")

Select the version of MicroPython that makes the most sense for your board. Not sure? Select ```MicroPython (generic)```.

This will connect to your board and show a Python REPL in the "shell" tab. To run a MicroPython program, open it from the ```MicroPython device``` tab. Then press the green arrow (Run Current Script). If you ever want to stop the running program, soft reset your board, or reconnect to your board, click the red stop sign (Stop/Restart backend).

### PyCharm

[PyCharm](https://www.jetbrains.com/pycharm/) is a popular and modern Python IDE with plugin support for interfacing with MicroPython boards. PyCharm Professional is a paid version, but we suggest installing the free community version. To get started, visit the [PyCharm Downloads Page](https://www.jetbrains.com/pycharm/download/) and scroll down until you see the "PyCharm Community Addition" section and click the `Download` button. Open the setup executable that you downloaded and configure your installation. We suggest accepting the default installation folder and adding the Desktop Shortcut and Context Menu. 

![pycharm-install](/docs/images/pycharm-install.png "PyCharm Install")

Once your install is complete, open PyCharm. Skip any import settings that pop up when you open it for the first time. 

Navigate to Plugins and in the "Marketplace" tab search for "MicroPython Tools". Note: this is a third-party plugin with no explicit support or maintenance from Jetbrain or SparkFun. Older versions of PyCharm contain a JetBrains-supported plugin called simply "MicroPython" but they no longer update it and it cannot run on the latest PyCharm versions.

![micropython-tools](/docs/images/micropython-tools.png "MicroPython Tools")

After installing the plugin, restart your IDE. Then, select the gear icon and choose "Settings" then navigate to Languages & Frameworks and select `MicroPython Tools`.

![pycharm-framework](/docs/images/pycharm-framework.png "PyCharm-Framework")

Select `Enable MicroPython support` and leave the other defaults checked. SparkFun is in the process of getting stubs for SparkFun MicroPython boards added to the official repository, but in the meantime in the `stubs package` field, choose a generic MicroPython stubs package corresponding to your MCU. For an RP2350 or RP2040 board, we suggest the most recent version of `micropython-rp2-stubs_x.xx.x`. For ESP32 boards, we suggest the most recent version of `micropython-esp32-stubs_x.xx.x`. These stubs packages simply provide useful code-completion, highlighting, and warnings for MicroPython development.

![pc-mp-settings.png](/docs/images/pc-mp-settings.png "pc-mp-settings")



A good starting place for the use of this plugin is the [MicroPython Tools README](https://github.com/lukaskremla/micropython-tools-jetbrains/blob/main/README.md). Let's create our first project. Click the "+" sign or select `file > New Project...` to create a new project. Let's name our project "hello_world" and accept the default interpreter/environment:

![pycharm-new-project.png](/docs/images/pycharm-new-project.png "pycharm-new-project")

When our new project first opens up, it has our `hello_world` directory as well as several components like `.venv` and `External Libraries` that are helpful when doing regular Python Development.

![pc-start-dir.png](/docs/images/pc-start-dir.png "pc-start-dir")

But we are anything but regular. We will be using the MicroPython running on our MCU to interpret our code, not a Python interpreter installed on your computer. So you can mostly disregard these files.

Now, right click the `hello_world` directory and select `Mark Directory as > MicroPython Sources Root`. The MicroPython Tools plugin will now map this `hello_world` directory that exists on our computer to the root file system of our MicroPython board when we perform upload commands.

![pc-sources-root.png](/docs/images/pc-sources-root.png "pc-sources-root")

Now lets add our MicroPython program. Right click the `hello_world` directory and select `new > Python File` and add a file called `print_platform.py`. Paste the following code into the file: 

```python
import sys

print ("Hello from (Micro)Python! I am running on the following platform:", sys.platform)
```

This is the same code as is discussed in the [mpremote]() section. 

Now lets configure an upload command and a run command. At the top of PyCharm next to the execute and debug buttons, select `Current File > Edit Configurations` 

![edit-configurations.png](/docs/images/edit-configurations.png "edit-configurations")

In the Run/Debug Configurations window that pops up, select the "+" sign and then select `MicoPython Tools > Upload Project`. Check the boxes for `Reset on success`, `Switch to REPL tab on success`. Then, click `Apply`.

![pc-upload-project.png](/docs/images/pc-upload-project.png "pc-upload-project")

While we're at it, lets create an execute command. Again, click the "+" sign and select `MicroPython Tools > Execute`. Input the path to our print_platform.py file we have created and check the box for `Switch to REPL tab on success`. Click `Apply` and finally `OK` to save our upload  and execute commands.

![pc-execute.png](/docs/images/pc-execute.png "pc-execute")

The upload command will take the directory that is configured as `MicroPython Sources Root` (in our case the hello_world directory) and load that onto the root directory of our MicroPython connected board. The execute command will run whatever file we have selected from the local computer's file system and run it on our board (without explicitly uploading it to the device).

Now, let's connect to our device! Plug in your board that already has [MicroPython firmware installed](#latest-micropython-firmware-downloads) and then in the bottom-left of PyCharm, select the MicroPython Tools extension. Select the correct COM port for your board. And then click the plug symbol to connect. 

![pc-connect.png](/docs/images/pc-connect.png "pc-connect")

Now that we are connected, let's upload our program. Select our upload configuration from the drop-down at the top of PyCharm and then click the green `Run` arrow. 

![pc-run-upload.png](/docs/images/pc-run-upload.png "pc-run-upload")

Select the `File System` tab in the MicroPython tools extension tab and we should now see `print_platform.py` file uploaded to the device!

![pc-file-system.png](/docs/images/pc-file-system.png "pc-file-system")

Finally, let's select our execute configuration and run it as well. 

![pc-run-execute.png](/docs/images/pc-run-execute.png "pc-run-execute")

If all goes well, you should see a hello statement printed in the REPL tab of the MicroPython Tools extension. The platform printed should match the MCU of your board and not be your computer's operating system. 

![pc-run.png](/docs/images/pc-run.png "pc-run")

Some things to note:
- The execute job we configured uses the version of the file currently in our local `hello_world` directory and runs it directly without uploading it. The upload step is helpful however if we have multiple files that we want to upload at once, for example if the file we are actually running relies on other files.
- Drag and drop is supported by this extension, such that you can simply drag files from the project explorer on the left of PyCharm to the `File System` tab of the extension to copy files from your local computer to your MicroPython board. 
- Another alternative to explicitly using an upload configuration is to select a file from the PyCharm project explorer and right click it and select either `Execute file in MicroPython REPL` or `Upload file to MicroPython device`.
- Remember that you can still use the REPL directly from the `REPL` tab and execute MicroPython commands  on your board just as if you were using `mpremote`.


### Other Tools
* [VSCode with MicroPico Extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go): If you happen to be developing on a Raspberry Pi pico platform, this offers a similar experience to Thonny and PyCharm.
* [Arduino Lab For MicroPython](https://labs.arduino.cc/en/labs/micropython): Offers a simple IDE for MicroPython development with a similar look and feel to Arduino IDE.

## Drivers
Check out our growing list of Python Drivers: [https://github.com/topics/sparkfun-python](https://github.com/topics/sparkfun-python)


