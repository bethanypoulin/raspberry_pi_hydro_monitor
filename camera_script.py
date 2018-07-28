#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 22:50:10 2018
picTroponics
@author: bethany poulin
"""

import time
from pymongo import MongoClient
import pymongo
import gridfs
import os
import picamera
import datetime
os.chdir('/home/pi/hydro_images')

# Set up pymongo to post and pull
con = MongoClient('bb11111.mlab.com',22222)
db = con.crypto # making connection
db.authenticate('your_name', 'YourPassWord') #checking your credentials
collection = db['sensor'] #instantiate database 


# instantiate the mongo fsGrid table
fs = gridfs.GridFS(db) #instatiate large file repository

#Define 'daylight' hours
light_on = 6 # 24-hour time when grow light comes on
light_off = 20 #24-hour time when light turns off

# an open ended loop where the images are taken every hour until the Pi is shut down
while True:
    with picamera.PiCamera() as camera: #instantiate camera
        camera.resolution = (1024, 768) #set resolution
        camera.rotation = 180 # flip image (depends on configureations of camera location)
        time.sleep(1) # warm up time for camera before taking photograph
        
        #Create a file name
        filename = 'image' + str(time.strftime("%m-%d-%Y %H:%M:%S")) + '.jpg'         
       #take current time now_hour=int(datetime.datetime.now().time().strftime('%H'))
    
        #qualify camera, only if light is on, take image
        if (now_hour > light_on & now_hour < light_off):
            test_image = camera.capture(filename)
            file = open(filename, 'rb') #save in the file above
            
            # ALthough it appears the images will all write over themselves, the won't
            #Each file saved via gridFS gets a unique _Id 
            #So that  this becomes an identifier if you shave other images to the same repository
            
            # Push the file to mongoDB 
            fs.put(file, filename='test.jpg') 
        else:
            continue
    time.sleep(3600)
