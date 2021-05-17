#!/bin/bash

sudo docker run -p 1883:1883 -p 9001:9001 -d -v /home/pi/solaranlage/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf --restart always eclipse-mosquitto:latest
