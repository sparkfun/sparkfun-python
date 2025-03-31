# MicroPython RGB LED Ramp Example
The mpy_rgb_ramp demo writes to the NeoPixel LED on a MicroPython device (that has the "NEOPIXEL" pin defined). It demonstrates blinking the LED, reading the current LED RGB value, and smoothly transitioning between the current RGB value and a target RGB value. 

## Contents

* [Hardware](#hardware)
* [Installation](#installation)
* [Code Explanation](#code-explanation)

## Hardware
This example uses the built-in NeoPixel LED present on SparkFun development boards (such as the [IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html) and the [IoT RedBoard ESP32 with MicroPython](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-micropython-development-board.html)) and no additional hardware is needed!

## Installation
Check out [mcu_setup.md](https://github.com/sparkfun/sparkfun-python/blob/main/docs/mcu_setup.md) to see how to create or copy a new file to a MicroPython device. Add the `mpy_rgb_blink.py` file from this directory to your MicroPython device and run it with your [tool of choice](https://github.com/sparkfun/sparkfun-python/blob/main/docs/mcu_setup.md#suggested-development-environments).

## Code Explanation
### Setting up the NEOPIXEL

MicroPython has a built-in [`machine`](https://docs.micropython.org/en/latest/library/machine.html) module designed to enable developers to easily control hardware features. The [`machine.Pin`](https://docs.micropython.org/en/latest/library/machine.Pin.html) class is used for controlling hardware pins such as GPIOs. Usually, we pass a pin number when instantiating an instance of the `machine.Pin` class, but we can also pass a string to instantiate a named pin. Board developers can submit a "pins.csv" file to MicroPython to create a list of named pins that can be passed to `machine.Pin()` in place of a pin number. For example, if your are curious check out the [pins.csv file](https://github.com/micropython/micropython/blob/master/ports/rp2/boards/SPARKFUN_IOTREDBOARD_RP2350/pins.csv) for the IoT RedBoard RP2350. A common named pin is "NEOPIXEL" representing a NeoPixel LED (individually addressable RGB LED). Thus, our first step is to create a pin representing our LED by using this name:

```python
pin = machine.Pin("NEOPIXEL")
```

The `neopixel` module is another module included in most MicroPython versions and allows us to easily interact with these NeoPixel LEDs. Lets create a [`neopixel.NeoPixel`](https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html) object using the pin that we just created. We pass 1 to represent that we will only be interacting with a single LED.

```python
led = neopixel.NeoPixel(pin, 1) 
```

Our resulting `led` NeoPixel object allows us to write different RGB values to different LEDs. Since we only have one LED, we will only interact with `led[0]`.

### Winking the LED
Now, let's use the `led` object.

```python
def wink_led(led):
    cur_clr = led[0] # Read the current color

    # wink the LED ... off and on three times
    for i in range(0, 3):
        led[0] = [0, 0, 0]  # off
        led.write()

        time.sleep_ms(100)

        # restore the color
        led[0] = cur_clr
        led.write()
        time.sleep_ms(100)
```

Notice how every time that we want to write the LED with a new value, we assign an RGB tuple to `led[0]` and then call ```write()```. To blink the LED with random colors, we simply need to turn the LEDs off by passing a tuple with R=0, G=0, B=0:

```python
led[0] = (0, 0, 0)  # LED OFF
led.write()
```

Similarly, to assign new arbitrary led values, we can simply write them with:
```python
led[0] = (R, G, B)  # LED ON
led.write()
```

We can read this RGB tuple by inspecting `led[0]`
```python
cur_clr = led[0] # Read the current color
```

Thus by alternating between turning the LED on with its current RGB values and off with 0's, we can create a "winking" effect.

### Smoothly Transitioning the LED Color
Now, let's see how to smoothly transition between two colors. 

```python
def led_transition(led, R, G, B):
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
```

We read our current led value and convert it to a list (because you cannot have their elements directly assigned). Next we calculate the linear relationship between each of our current R, G, and B values and the target value we want them to reach. Finally, we use a loop to gradually change each RGB value.