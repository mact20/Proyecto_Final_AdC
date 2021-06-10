import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import serial

import os
from PyQt5 import QtGui, QtCore
from proyectoFile import *

from PyQt5 import QtCore, QtGui, QtWidgets

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from mpu6050 import mpu6050
from smbus2 import SMBus
from mlx90614 import MLX90614

from datetime import datetime

import subprocess

import Adafruit_DHT

import blynklib
BLYNK_AUTH = '-csCRO5lDH1S_Kuq7Cm-njpOOrCwtU4h'
blynk = blynklib.Blynk(BLYNK_AUTH)

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

bus = SMBus(1)

#Sensors
thermometer = MLX90614(bus, address=0x5A)
humiditySensor = Adafruit_DHT.DHT11
mpu = mpu6050(0x68)

#Selected sensor
seleccion = 0

#Time values for temperature check
repeatTime = 10
targetTime = time.time()

class Ui_MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.sensorLoop()
        
        #Run the sensor loop every 250 seconds
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.sensorLoop)
        timer.start(250)
        
    def sensorLoop(self):
        #Update Accelerometer and Gyroscope
        accel_data = mpu.get_accel_data()
        gyro_data = mpu.get_gyro_data()
        
        #Update MLX Thermometer
        objTemperature = thermometer.get_obj_temp()
        
        #Update DHT11 Humidity (every 10 seconds)
        global targetTime
        global humidity
        global ambientTemp
        if time.time() >= targetTime:
            print("getting temp")
            humidity, ambientTemp = Adafruit_DHT.read_retry(humiditySensor,4)
            targetTime = time.time() + repeatTime

        
        
        #Clear screen
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        
        fechaHora = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        
        #Show data in screen and app
        if seleccion == 0:
            #print("Humedad")
            draw.text((x, top),       "Humedad",  font=font, fill=255)
            draw.text((x, top+8),     str(humidity),  font=font, fill=255)
            draw.text((x, top+16),    "Temperatura Ambiente",  font=font, fill=255)
            draw.text((x, top+25),    str(ambientTemp),  font=font, fill=255)
            self.label.setText(fechaHora + "\n"+"Humedad: " + str(humidity) + "\n" + "Temperatura Ambiente: " + str(ambientTemp))

        elif seleccion == 1:
            #print("Temperatura")
            draw.text((x, top),       "Temperatura",  font=font, fill=255)
            draw.text((x, top+8),     str(objTemperature) + " C",  font=font, fill=255)
            draw.text((x, top+16),    "",  font=font, fill=255)
            draw.text((x, top+25),    "",  font=font, fill=255)
            self.label.setText(fechaHora + "\n"+"Temperatura Objeto\n" + str(objTemperature))
            
        elif seleccion == 2:
            #print("Acelerometro")
            draw.text((x, top),       "Acelerometro",  font=font, fill=255)
            draw.text((x, top+8),     "X: " + str("%.2f" % accel_data['x']),  font=font, fill=255)
            draw.text((x, top+16),    "Y: " + str("%.2f" % accel_data['y']),  font=font, fill=255)
            draw.text((x, top+25),    "Z: " + str("%.2f" % accel_data['z']),  font=font, fill=255)
            self.label.setText(fechaHora + "\n"+"Acelerometro\nX: " + str("%.2f" % accel_data['x']) + "\n" + "Y: " + str("%.2f" % accel_data['y']) + "\nZ: " + str("%.2f" % accel_data['z']))
            
        elif seleccion == 3:
            #print("Giroscopio")
            draw.text((x, top),       "Giroscopio",  font=font, fill=255)
            draw.text((x, top+8),     "X: " + str("%.2f" % gyro_data['x']),  font=font, fill=255)
            draw.text((x, top+16),    "Y: " + str("%.2f" % gyro_data['y']),  font=font, fill=255)
            draw.text((x, top+25),    "Z: " + str("%.2f" % gyro_data['z']),  font=font, fill=255)
            self.label.setText(fechaHora + "\n"+"Giroscopio\nX: " + str("%.2f" % gyro_data['x']) + "\n" + "Y: " + str("%.2f" % gyro_data['y']) + "\nZ: " + str("%.2f" % gyro_data['z']))
        
        
        #Blynk update
        blynk.run()
        
        blynk.virtual_write(0,objTemperature)
        
        blynk.virtual_write(1,accel_data['x'])
        blynk.virtual_write(2,accel_data['y'])
        blynk.virtual_write(3,accel_data['z'])
        
        blynk.virtual_write(4,gyro_data['x'])
        blynk.virtual_write(5,gyro_data['y'])
        blynk.virtual_write(6,gyro_data['z'])
        
        blynk.virtual_write(7,humidity)
        blynk.virtual_write(8,ambientTemp)
        
        disp.image(image)
        disp.display()
        
    def press_it(self, pressed):
        global seleccion
        seleccion = pressed
        
        if pressed == 0:
            self.hum.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.temp.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.acc.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.giro.setStyleSheet("background-color: rgb(170, 170, 255);")
        elif pressed == 1:
            self.temp.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.hum.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.acc.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.giro.setStyleSheet("background-color: rgb(170, 170, 255);")
        elif pressed == 2:
            self.acc.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.temp.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.hum.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.giro.setStyleSheet("background-color: rgb(170, 170, 255);")
        elif pressed == 3:
            self.giro.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.temp.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.hum.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.acc.setStyleSheet("background-color: rgb(170, 170, 255);")
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec_()


#while True:
 #   print("loop")
    

