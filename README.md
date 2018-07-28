README
================

This is the Primary Repository for the Hydro-Monitor Project
------------------------------------------------------------

Within this repository you will find:

-   A Parts List (including helpful links and providers of online services)
-   A Raspberry Pi set up guide to help assemble the sensors and activate interfaces
-   Python Code for the Raspberry Pi to capture sensor readings & images and save them to mLabs remote mongoDB repository
-   Files for pythonanywhere.com website to make charts available anywhere

Python Modules
--------------

### On the Raspberry Pi

In addition the modules we installed while assembling and testing the Raspberry Pi and sensors, there are a number of modules you will need to install to push data and images to mLabs, mongoDB.

`pip3 install pymongo`
`pip3 install gridfs`
`pip3 install picamera`

Once you have these modules installed, you will need to do a few things to get ready to send sensor data and images out to mLab.

You will need to configure the Pi to work with the camera. You can find solid and the most current directions here as the [Raspberry Pi](https://www.raspberrypi.org/documentation/configuration/camera.md) foundations website.

### mLab

You will also need to sign up for an account at mLab to push data to as it is gathered. [mLab has great support pages](https://docs.mlab.com/) to help you get set up chase down: Quick-Start Guide to mLab.

Once set up with an mLabs account you will need to collect a few bit of informations, which mLab makes immediately available to you, to access your new database remotely. You will need the following to connect with mLab using pymongo:
DATABASE NAME - you will choose this, this database will house the collection for your sensor & images HOST - it will look something like `df39249mlab.com` with two numbers and five letters
PORT - this is the port your database is assigned to access via mLab
USERNAME - this user is defined by you within your database, you can have multiples with different permission levels PASSWORD = Choose wisely

While you are signing up for your mLab account, you will want to sign up for free account at [pythonanywhere.com](https://www.pythonanywhere.com/pricing/) as well. Once you have the account set up, you might want to run through [this tutorial](http://blog.pythonanywhere.com/121/) on building a simple Flask application to get feel for working with python web framework.

On PythonAnywhere
-----------------

`pip3 install pymongo`
`pip3 install gridfs`

Setting up the Pi Code
----------------------

In the repository there are two scripts, one to take a photograph once per hour and save it to the large-file system on mongoDB and a script which takes sensor readings every fifteen minutes saving them to the database. The two could have been integrated into a single script, but I chose to keep them separate so that if there is a problem with the camera (which is FAR MORE LIKELY than sensor failures) you do not lose both systems.

Create a folder in your documents folder on the Pi. Using the commandline terminal, change directories into that folder then clone the scripts.

### Some possible safegards

#### Fault Tolerance

Both scripts are very simple,and if you are going to use this in an important setting, you might want to add some `try` and `excepts` to make it more robust in the face of fickle sensors. I prioritized the web interactivity over the fault tolerances. Once the next phase of sensors are added and working right, I will build a more global means of regulating errors.

#### Power & Reboots

To make the system robust against failures you either need to use a battery backup with your Pi or follow the directions from [this link](https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/) to automate the scripts to restart on reboot if you lose power.
