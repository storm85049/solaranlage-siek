#!/usr/bin/python

import spidev
import time
import sys
spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode= 0b00
spi.max_speed_hz= 1000000
spi.bits_per_word= 8
print("Sending" + sys.argv[1])
spi.xfer2([int(sys.argv[1])])
spi.close()
#print spi.bits_per_word
#print spi.mode
#spi.cshigh= False
#print spi.cshigh
#frame = bytearray(b'\xA5')
#frame = [0x0D]
#try:
#    for x in reversed(range(255)):
#        print(x)
#        frame = [x]
#        resp = spi.xfer2(frame)
#        time.sleep(5)
#    spi.close()
#except KeyboardInterrupt:
#    spi.close()
