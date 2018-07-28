
# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
"""
PiDroponics
By Bethany Poulin
"""

from collections import OrderedDict
import datetime
import pytz
import time
from pymongo import MongoClient
import pymongo
import pandas as pd
from w1thermsensor import W1ThermSensor
import Adafruit_DHT
from tsl2561 import TSL2561
import os
# Pandas data frame settings
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Set up pymongo to post and pull
con = MongoClient('bb11111.mlab.com',22222)
db = con.crypto
db.authenticate('your_name', 'YourPassWord')
collection = db['sensor']



# Pandas data frame settings
pd.set_option('display.float_format', lambda x: '%.5f' % x)
os.chdir('/your/path/for/csv')

#Create a function to take sensor readings
# The sensors are instatiated in the arguments of the function, with defaults set
def read_function(tsl = TSL2561(debug=True), temp_sensor = W1ThermSensor(), dht_sense = Adafruit_DHT.AM2302, gpio_ht  = 11):
    date_time = datetime.datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M:%S")
    h2o_temp = temp_sensor.get_temperature() #DS18B20 
    humidity, temperature = Adafruit_DHT.read_retry(dht_sense, gpio_ht) #AM2302
    light = tsl.lux() #TSL2561
    
    #Because this will be saved both to mLab remotely and locally in csv file
    #It was necessary to order the dictionary to ensure each appended observation is properly ordered
    #To align with the CSV file.
    
    sensor_observation = OrderedDict([('date_time',[date_time]),('water_temp',[round(h2o_temp, 2)]), ('air_temp',[round(temperature,2)]), ('humidity',[round(humidity,2)]), ('light_level',[light])])
    return sensor_observation

# Take an endless stream of readings 
while True:

    sensor_observation = read_function() #call the above function
    
    #create a dictionary of values & make dataframe
    df = pd.DataFrame(sensor_observation)
    
    #write to CSV locally
    df.to_csv('/home/pi/Documents/hydro/hydro.csv', mode ='a', header=False, index=False) #add your path!!!
    
    #write to mongoDB on mLabs in the cloud
    collection.insert_one(sensor_observation) 

    #sleep fr 15 minutes (times 60 seconds)
    time.sleep(900) 