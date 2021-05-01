#!/usr/bin/python
#-*- coding:utf-8 -*-
import paho.mqtt.client as mqtt
import spidev
import time
import math
spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode= 0b00
spi.max_speed_hz= 1000000
spi.bits_per_word= 8

deviceId = "tesdtid"
phase = "1"
topic = "shellies/shellyem3-"+deviceId+"/emeter/"+phase+"/power"

def convert_watts_to_poti(watts):
    if watts >= 245:
        # lineare funktion, weil ab 245 Watt nicht mehr parablelartig
        return linear(watts)
    elif watts < 245:
        return parabel(watts)

def linear(watts):
    floatingResult = (watts - 42.55) / 5.0545
    return math.floor(floatingResult)

def parabel(watts):
    a = -0.158
    b = 11.98
    c = (21.8 - watts)
    disc = b**2 - 4 * a * c
    x1 = (-b - math.sqrt(disc)) / (2 * a)
    x2 = (-b + math.sqrt(disc)) / (2 * a)

    if x1 <= 38:
        return math.floor(x1)
    else:
        return math.floor(x2)

def on_connect(client, userdata, flags,rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")

def on_message(client, userdata, message):
    print("received " +  message.payload)
    value = int(message.payload)
    if value <= 0:
	# wenn das haus nichts verbraucht, inverter abschalten, damit strom in die batterie geht
        converted_value = 0
    elif value > 0 and value <= 500:
        converted_value = convert_watts_to_poti(value)
    elif value > 500:
	# wenn das haus mehr als 500 verbraucht, den inverter auf maximal 500 setzen (daher die 90 -> 504W)
        converted_value = 90

    print("sending " + str(converted_value))
    spi.xfer2([int(converted_value)])


client = mqtt.Client("paho")
connected = False
while (not connected):
    try:
        client.connect("localhost", 1883, 30)
        connected = True
    except:
        print("could not establish connection, retrying in 5 seconds" )
        time.sleep(5)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever(timeout=5.0, retry_first_connection=True)
