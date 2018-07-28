Physically Setting Up the Pi
================

Base Assumptions
----------------

You will need to configure the Raspberry Pi yourself. There are many tutorials out there to help you get set up. You can find support for Raspbian this at [Raspberry Pi Organization](https://www.raspberrypi.org/downloads/raspbian/)

Devlopment Environment
----------------------

In order to work in the python environment, you need to have an IDE set up. You definitely keep your install light and work with `IDLE`. Coming from a data science domain, `IDLE` is not a comfortable workspace, so I choose instead to work in either spyder or jupyter notebooks. Because it is slimmer and more development based, when workin on a Pi I use the `Spyder` development environment and have moved exclusively to Python 3 in recent months. To create this environment you will need to open up a fresh terminal and do the following:

1.You must update prior to installing. If you work in a GUI this is done for you, but when working in the comand line it must be manually deployed. It is very common to encounter install errors when omitting this step. So, we are going to do this first.

`sudo apt-get update`

1.  Install *spyder 3* fromm the terminal as well. After issuing the following command, your Pi terminal will ask you if you wish to proceed enter `y` and `<enter>` to continue. This will take a while to install depending on your model of pi, what type of drive your raspbian OS is on and how you are connecting to the internet. Just wait to hit `y / n` and `<enter>` before walking away!

`sudo apt-get install spyder3`

Activating One-Wire Interface on Raspberry Pi for DS18B20 Sensor
----------------------------------------------------------------

![DS18B20](https://ae01.alicdn.com/kf/HTB1p19tPXXXXXXoXpXXq6xXFXXXt/Stainless-steel-package-Waterproof-DS18b20-temperature-probe-temperature-sensor-18B20.jpg_640x640.jpg)
Because the DS18B20 temperature sensor is a One-Wire device, with an assigned serial number, it is necessary to tell the Linux kernel that we are going to use this type of device communication. It is a simple task.

1.  Install `w1thermsensor` (this is a One-Wire temperature sensor module) using `sudo pip3 install w1thermsensor` Thsi should not take more than 20 or 30 seconds with a good connection.

2.  Enable the One-Wire Interface on your Raspberry Pi

<!-- -->

1.  Go to the start menu in the upper left corner of your Raspberry Pi GUI (it looks like a raspberry in a grey circle)
2.  Select `Raspberry Pi Configuration` (on the bottom row of my `preferencess`)
3.  In the grey `Raspberry Pi Configuration` window which opens click on the tab `Interfaces`
4.  Select the radio button for `Enabled` to the right of `1-Wire` optional: if you will be using a `Pi-camera`, and `SPI` or `I2C` devices in your build or intend to access the Pi via `SSH` once you have it up and running, then you should enable those features now as well!

**If you enable SSH, you should jump over to the `System` tabe and change your password, because everyone on earth know the default Pi password is `raspberry`!**
5. You will need to reboot your Rapberry Pi to use these new configuration features, and the configuration manage will ask you to do so, say yes! `y` `\<enter\>`

### Testing the DS18B20 before moving on:

*YOUR PI SHOULD BE POWERED OFF FOR THIS NEXT STEP!*

Using a a breadboard and Pi Cobbler make the following connections:

<table>
<colgroup>
<col width="26%" />
<col width="23%" />
<col width="23%" />
<col width="26%" />
</colgroup>
<thead>
<tr class="header">
<th>Sensor Connection</th>
<th>Connector</th>
<th>Pi Connection</th>
<th>Location</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>DS18B20 - red wire</td>
<td>4.7K Resistor</td>
<td>DSI18B20 Green Wire</td>
<td>On Breadboard</td>
</tr>
<tr class="even">
<td>DS18B20 - red wire</td>
<td>Red Male to Male</td>
<td>3.3 V - Pin 01</td>
<td>Cobler Pi-Breadboard</td>
</tr>
<tr class="odd">
<td>DS18B20 - green wire</td>
<td>Green Male to Male</td>
<td>GPIO 04 - Pin 07</td>
<td>Cobler Pi-Breadboard</td>
</tr>
<tr class="even">
<td>DS18B20 - black wire</td>
<td>Black Male to Male</td>
<td>Ground - Pin 09</td>
<td>Cobler Pi-Breadboard</td>
</tr>
</tbody>
</table>

*See note below*

As in the Image Here Compliments of Adafruit:

![Adafruit Wiring Diagrame](https://cdn-learn.adafruit.com/assets/assets/000/003/781/medium800/learn_raspberry_pi_breadboard-ic.png?1396801666)

*Note* This is a 26 pin version of the Pi Cobbler, if you are using a 40 pin version you may choose the same Ground or one just below the Green (yellow on this diagram) 1-Wire at `Ground - Pin 09`.

*If you are Unsure Double Check before putting power to the pins! *

You can check to see how the pins are arranged on your Pi! Open a terminal and type:

`pinout` and hit return.

You will get a printout of the system hardward as well as an ordered, labeled diagram of your Raspberry Pi's pinout!

There is NO REASON to improperly wire and damage your PI.

[ADD Screen Shot of Linux Console with Pin Identification]('none')

#### Connecting to DS19B20 From Python

Run the following script either from your terminal or spyder3.

``` python
#import needed modules
import time
from w1Thermsensor import W1ThermSense
 
#instantiate an instance of w1thermsensor to call readings
sensor = W1ThermSense() 
 
# Create a loop which reads the sensor and prints our the temperature to the console
while True:
  temp = sensor.get_temperature()
  print('%s Celcius' % temp)
  time.sleep(5)
 
```

You should see the appropriate temperature print to the terminal or your Spyder console every five seconds until you hit `Ctr+c` on the keyboard to interupt it. While it is running, use cup of warm and a cup of ice water to be sure that the sensor is noticing changes in temperature as it should.

AM2302 Setup - Humidity Sensor
------------------------------

![AM2302](https://www.digibay.in/image/cache/data/se/420-a-dht22-am2302-digital-humidity-and-temperature-sensor-600x600.jpg)

### Getting The Environment Ready

[With help from Raspberry Pi Spy](https://www.raspberrypi-spy.co.uk/2017/09/dht11-temperature-and-humidity-sensor-raspberry-pi/)

Again to make it easier, I am using python module created for us by the great folks at Adafruit. So we need to install a few things to make it happen

1.Because a lot has gone down since we installed `w1thermsensor` we will again update our linux environment.

`sudo apt-get update`

1.  This next step i only necessary if you have not previously directly intalled a module from github on this Pi, `sudo apt-get install build-essential python-dev`

2.  Directly clone the package into your Raspberry Pi from github, then change directories to the new folder location & run setup

`git clone https://github.com/adafruit/Adafruit_Python_DHT.git`

`cd Adafruit_Python_DHT`

`sudo python3 setup.py install`

#### Wiring the Raspberry Pi

<table>
<colgroup>
<col width="27%" />
<col width="21%" />
<col width="29%" />
<col width="20%" />
</colgroup>
<thead>
<tr class="header">
<th>Sensor Connection</th>
<th>Connector</th>
<th>2nd Connection</th>
<th>Location</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>AM2302 - Pin 1 3.3V Pin</td>
<td>4.7K Resistor</td>
<td>AM2302 - Pin 2 Sensor Pin</td>
<td>On Breadboard</td>
</tr>
<tr class="even">
<td>AM2302 - Pin 2 Sensor Pin</td>
<td>Orange Male to Male</td>
<td>GPIO 11 (pin23)</td>
<td>Cobler Pi-Breadboard</td>
</tr>
<tr class="odd">
<td>AM2302 - Pin 1 3.3V Pin</td>
<td>Red Male to Male</td>
<td>3.3 V Pin 17</td>
<td>Cobler Pi-Breadboard</td>
</tr>
<tr class="even">
<td>AM2302 - Pin 4 Ground</td>
<td>Black Male to Male</td>
<td>Ground - Pin 25</td>
<td>Cobler Pi-Breadboard</td>
</tr>
</tbody>
</table>

#### Testing the AM2302

``` python
#import needed modules
import Adafruit_DHT
import time
#-*- coding: utf-8 -*-
 
#instantiate an instance of AM2302
dht_sensor = Adafruit_DHT.AM2302 
#set the GPIO Pin to 11
gpio_ht = 11
# Create a loop which reads the sensor and prints our the temperature to the console
while True:
  humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, gpio_ht)
  print( 'Temperature:  {0:0.2f}\xb0 Celcius '.format(temperature))
  #print('%s, Humidity' % humidity)
  print('Humidity:  {0:0.2f} %'.format(humidity))
  time.sleep(5)
#use Control + C to break the loop
 
```

### TSL2561 - Light Sensor

![TSL2561](https://media.digikey.com/Photos/Adafruit%20Industries%20LLC/MFG_439_sml.jpg)

#### Setting up the Environment

Installing the module for python to control the TSL2561 sensor.

`sudo pip3 install tsl2561`

#### Wiring the TSL2561 to Raspbery Pi

The TSL2561 is an `I2C` sensor, which means it needs to be plugged into the `SCL`, `SDA`, 5V0 and Ground pins.

<table>
<colgroup>
<col width="27%" />
<col width="21%" />
<col width="29%" />
<col width="20%" />
</colgroup>
<thead>
<tr class="header">
<th>Sensor Connection</th>
<th>Connector</th>
<th>2nd Connection</th>
<th>Location</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>TSL2561 - Pin 1 VCC Pin</td>
<td>Red Male to Female</td>
<td>Pi pin 4 - 5 V</td>
<td>Pi Cobler - On Breadboard</td>
</tr>
<tr class="even">
<td>TSL2561 - Pin 2 Ground Pin</td>
<td>Black Male to Female</td>
<td>Pi pin 6 Ground</td>
<td>Pi Cobler - Breadboard</td>
</tr>
<tr class="odd">
<td>TSL2561 - Pin 3 SCL Pin</td>
<td>Gray Male to Female</td>
<td>GPIO 03 - (pin 5)</td>
<td>Pi Cobler - Breadboard</td>
</tr>
<tr class="even">
<td>TSL2561 - Pin 4 SDA Pin</td>
<td>Purple Male to Female</td>
<td>GPIO 02 - (pin 3)</td>
<td>Pi Cobler - Breadboard</td>
</tr>
</tbody>
</table>

#### Test Code

``` python
import time
from tsl2561 import TSL2561
tsl = TSL2561(debug=True)
while True:
  light = tsl.lux()
  print('Light:', light, 'Lux')
  time.sleep(5)
```

These are the core sensors in the base configuration of the monitor system. As I develop newer arrays, I will update both this document and the code documents.
