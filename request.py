#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import time

delay = 1
shelly3EM = "192.168.178.49"
shelly1PM = "192.168.178.53"
shelly3EMUrl = "http://"+shelly3EM+"/status"
shelly1PMUrl = "http://"+shelly1PM+"/status"



def executeCall():
    r = requests.get(shelly3EMUrl)
    r2 = requests.get(shelly1PMUrl)
    if r2.status_code == 200:
        json2 = r2.json()
        inverterVerbrauch = json2["meters"][0]["power"]
    if r.status_code == 200:
        json = r.json()
        total = 0
        for emeter in json["emeters"]:
            total += emeter["power"]
        time.sleep(delay)
    print("total + inverter = " + str(total) + " + " + str(inverterVerbrauch) + " = " + str(total+inverterVerbrauch))
while True:
    executeCall()