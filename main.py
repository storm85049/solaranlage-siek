#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import json
import spidev
import time
import math

spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 0b00
spi.max_speed_hz = 1000000
spi.bits_per_word = 8

request_timeout = 1  # zeit in sekunden
request_delay = 2  # zeit in sekunden

shelly3EM = "192.168.178.49"
shelly1PM = "192.168.178.53"
shelly3EMUrl = "http://" + shelly3EM + "/status"
shelly1PMUrl = "http://" + shelly1PM + "/status"


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
    disc = b ** 2 - 4 * a * c
    x1 = (-b - math.sqrt(disc)) / (2 * a)
    x2 = (-b + math.sqrt(disc)) / (2 * a)

    if x1 <= 38:
        return math.floor(x1)
    else:
        return math.floor(x2)


def on_value_calculated(value):
    converted_value = 0
    if value <= 0:
        # wenn das haus nichts verbraucht, inverter abschalten, damit strom in die batterie geht
        converted_value = 0
    elif 0 < value <= 500:
        converted_value = convert_watts_to_poti(value)
    elif value > 500:
        # wenn das haus mehr als 500 verbraucht, den inverter auf maximal 500 setzen (daher die 90 -> 504W)
        converted_value = 90
    print("sending " + str(converted_value))
    spi.xfer2([int(converted_value)])


def executeCall():
    value_haus = 0
    value_inverter = 0
    value_not_found = False

    try:
        req_shelly = requests.get(shelly3EMUrl, timeout=request_timeout)
        if req_shelly.status_code is 200:
            res_shelly = req_shelly.json()
            for emeter in res_shelly["emeters"]:
                value_haus += emeter["power"]
    except requests.exceptions.ConnectionError as e:
        print("Es ist ein Fehler beim Verbinden mit PowerMeter aufgetreten")
        value_not_found = True

    try:
        req_inverter = requests.get(shelly1PMUrl, timeout=request_timeout)
        if req_inverter.status_code is 200:
            res_inverter = req_inverter.json()
            value_inverter = res_inverter["meters"][0]["power"]
    except requests.exceptions.ConnectionError as e:
        print("Es ist ein Fehler beim Verbinden mit SUN1000 aufgetreten")
        value_not_found = True

    print(
        "value_haus + value_inverter = " + str(value_haus) + " + " + str(value_inverter) + " = " + str(
            value_haus + value_inverter))

    final_value = 0 if value_not_found else (value_inverter + value_haus)
    on_value_calculated(final_value)
    time.sleep(request_delay)


while True:
    executeCall()
