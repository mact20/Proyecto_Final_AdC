import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import serial

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from mpu6050 import mpu6050
from smbus2 import SMBus
from mlx90614 import MLX90614

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

mpu = mpu6050(0x68)

bus = SMBus(1)
thermometer = MLX90614(bus, address=0x5A)
humiditySensor = Adafruit_DHT.DHT11

seleccion = 3

repeatTime = 5
targetTime = time.time() + repeatTime
humidity, ambientTemp = Adafruit_DHT.read(humiditySensor,4)

while True:
    
    #Clear screen
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    #Update Accelerometer and Gyroscope
    accel_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()
    
    #Update MLX Thermometer
    objTemperature = thermometer.get_obj_temp()
    
    #Update DHT11 Humidity (every 2 seconds)
    if time.time() >= targetTime:
        print("getting temp")
        humidity, ambientTemp = Adafruit_DHT.read_retry(humiditySensor,4)
        targetTime = time.time() + repeatTime
    
    
    if seleccion == 0:
        print("Temperatura")
        draw.text((x, top),       "Temperatura",  font=font, fill=255)
        draw.text((x, top+8),     str(objTemperature) + " C",  font=font, fill=255)
        draw.text((x, top+16),    "",  font=font, fill=255)
        draw.text((x, top+25),    "",  font=font, fill=255)
        
    elif seleccion == 1:
        print("Acelerometro")
        draw.text((x, top),       "Acelerometro",  font=font, fill=255)
        draw.text((x, top+8),     "X: " + str("%.2f" % accel_data['x']),  font=font, fill=255)
        draw.text((x, top+16),    "Y: " + str("%.2f" % accel_data['y']),  font=font, fill=255)
        draw.text((x, top+25),    "Z: " + str("%.2f" % accel_data['z']),  font=font, fill=255)
        
    elif seleccion == 2:
        print("Giroscopio")
        draw.text((x, top),       "Giroscopio",  font=font, fill=255)
        draw.text((x, top+8),     "X: " + str("%.2f" % gyro_data['x']),  font=font, fill=255)
        draw.text((x, top+16),    "Y: " + str("%.2f" % gyro_data['y']),  font=font, fill=255)
        draw.text((x, top+25),    "Z: " + str("%.2f" % gyro_data['z']),  font=font, fill=255)
    
    elif seleccion == 3:
        print("Humedad")
        draw.text((x, top),       "Humedad",  font=font, fill=255)
        draw.text((x, top+8),     str(humidity),  font=font, fill=255)
        draw.text((x, top+16),    "Temperatura Ambiente",  font=font, fill=255)
        draw.text((x, top+25),    str(ambientTemp),  font=font, fill=255)
    
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
    time.sleep(0.1)

