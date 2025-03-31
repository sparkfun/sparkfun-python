# MicroPython RGB LED Blink Example

The mpy_rgb_blink demo writes to the NeoPixel LED on a MicroPython device (that has the "NEOPIXEL" pin defined). It demonstrates blinking the LED with different colors and fading the brightness of the LED higher and lower. 

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

### Blink Example
Now, let's use the `led` object.

```python
def blink_the_led(led, count=30):
    led[0] = (0, 0, 0)  # LED OFF
    led.write()

    for i in range(count):
        R = random.randint(0, 180)
        G = random.randint(0, 180)
        B = random.randint(0, 180)

        led[0] = (R, G, B)  # LED ON
        led.write()

        time.sleep_ms(BLINK_DELAY)

        led[0] = [0, 0, 0]  # off
        led.write()
        time.sleep_ms(BLINK_DELAY//2)
        print(".", end="")
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

### Fade Example

If we keep the ratio between R, G, and B the same, but raise or lower the value for all of them proportionally, we can keep the same color while changing the brightness of our LED. 

```python
def fade_in_out(led, color, fade_time=1000):
    for i in range(0, 256):
        led[0] = (int(color[0] * i / 255), int(color[1]
                  * i / 255), int(color[2] * i / 255))
        led.write()
        time.sleep_ms(fade_time // 256)

    for i in range(255, -1, -1):
        led[0] = (int(color[0] * i / 255), int(color[1]
                  * i / 255), int(color[2] * i / 255))
        led.write()
        time.sleep_ms(fade_time // 256)
```

This function takes an RGB tuple in `color` and then uses a loop to apply a multiplier to the passed in RGB values to vary their brightness.