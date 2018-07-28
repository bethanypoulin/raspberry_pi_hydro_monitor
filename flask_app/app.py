
import os
import bokeh
import pandas as pd
from flask import Flask
import pymongo
import gridfs
from pymongo import MongoClient
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.embed import components
from flask import  render_template
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Connecting to the data in mLabs I named my collection (like SQL table) sensor for the readings
con = MongoClient('bb11111.mlab.com',22222)
db = con.crypto
db.authenticate('your_name', 'YourPassWord')
collection = db['sensor']

#instatiating the fsGrid communications with the database to pull & reassemble image chuncks
fs = gridfs.GridFS(db)

# function to grab most recent image in mongoDB and save to images for retrival in images folder
def image_updater():
    most_recent = fs.find().sort("uploadDate", -1).limit(1)
    for grid_out in most_recent:
        data = grid_out.read()
    file_name = os.path.join('/home/yoursite/static/images' ,'most_recent_image.jpg')
    #file_name = 'most_recent_image.jpg'
    image_out = open(file_name, 'wb')
    image_out.write(data)
    image_out.close()

    # Pulling Data from mongoDB
def data_extract(mongoConn = collection):
    sensor_cursor = collection.find().limit(96).sort([("date", pymongo.ASCENDING)])
    sensor_data =  pd.DataFrame(list(sensor_cursor))
    sensor_data = sensor_data.applymap(lambda x: x[0] if isinstance(x, list) else x)
    sensor_data.drop(['_id'],axis=1, inplace=True)
    sensor_data['date_time'] = pd.to_datetime(sensor_data['date_time'], format='%Y-%m-%d %H:%M:%S')
    plot_data =sensor_data.tail(75)
    return (plot_data)

#defining a generic chart with dictionaries to pull titles, colors and labels to flesh out the charts
def chart(data_column, data_frame):
    selector={'titles':
    {'air_temp':'Twenty-Four Hour Air Temperature',
    'humidity':'Twenty-Four Hour Humidity',
    'light_level':'Twenty-Four Hour Light Level',
    'water_temp':'Twenty-Four Hour Nutrient Temperature'},
    'axis':
    {'air_temp':'Degrees Celsius',
    'humidity':'Percent Humidity',
    'light_level':'Lux',
    'water_temp':'Degrees Celsius'},
    'colors':
    {'air_temp':'green',
    'humidity':'purple',
    'light_level':'red',
    'water_temp':'blue'}}
    
    #Custom Hover Code
    hover = HoverTool(
        tooltips="""
        <div>
                <span style="font-size: 10px;">Sensor Reading:  </span> @y
        </div>
        """)

    chart = figure(x_axis_type ='datetime',title=selector['titles'][data_column], plot_width = 1050, plot_height = 450, tools =[hover])
    chart.grid.grid_line_alpha=0.3
    chart.xaxis.axis_label = 'Time'
    chart.yaxis.axis_label = selector['axis'][data_column]
    chart.line(x = pd.to_datetime(data_frame['date_time']), y = data_frame[data_column], color= selector['colors'][data_column], line_width=3)
    chart.xaxis.formatter=DatetimeTickFormatter(hours = ['%H:%M'], days=["%m-%d"])
    chart.xaxis.major_label_orientation = 45
    return(chart)

plant = 'static/images/most_recent_image.jpg'

#Home Page
@app.route('/')
def index():
    image_updater()
    plot_data = data_extract()
    script_nutrient, div_nutrient = components(chart(data_column = 'water_temp', data_frame = plot_data))
    script_air, div_air = components(chart(data_column = 'air_temp', data_frame = plot_data))
    script_humidity, div_humidity = components(chart(data_column = 'humidity', data_frame = plot_data))
    script_light, div_light = components(chart(data_column = 'light_level', data_frame = plot_data))
    return render_template('index.html',
        plant = plant,
        div_nutrient = div_nutrient,
        script_nutrient = script_nutrient,
        div_air = div_air,
        script_air = script_air,
        div_humidity = div_humidity,
        script_humidity = script_humidity,
        div_light = div_light,
        script_light = script_light)

#Chart with nutrients temperature
@app.route('/nutrient')
def nutrient():
    plot_data = data_extract()
    script_nutrient, div_nutrient = components(chart(data_column = 'water_temp', data_frame = plot_data))
    return render_template('nutrient.html',
        div_nutrient = div_nutrient,
        script_nutrient = script_nutrient)

#chart with air temperature
@app.route('/air')
def air():
    plot_data = data_extract()
    script_air, div_air = components(chart(data_column = 'air_temp', data_frame = plot_data))
    return render_template('air.html',
        div_air = div_air,
        script_air = script_air)

# Chart with humididty
@app.route('/humidity')
def humidity():
    plot_data = data_extract()
    script_humidity, div_humidity = components(chart(data_column = 'humidity', data_frame = plot_data))
    return render_template('humidity.html',
        div_humidity = div_humidity,
        script_humidity = script_humidity)

#chart with light levels
@app.route('/light')
def light():
    plot_data = data_extract()
    script_light, div_light = components(chart(data_column = 'light_level', data_frame = plot_data))
    return render_template('light.html',
        div_light = div_light,
        script_light = script_light)