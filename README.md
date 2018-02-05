ST7565 LCD driver for micropython
=================================

Description
-----------
This is micropython driver for LCDs based on **ST7565** controller.
Only serial mode sopported.

Wiring example for ESP8266-based modules
----------------------------------------

|LCD | ESP8266|
|----|--------|
|A0  | GPIO 0 |
|RST | GPIO 16|
|CS  | GPIO 15|
|DATA| GPIO 13|
|CLOCK| GPIO 14|

Usage example
-------------
```python
import machine
from st7565 import ST7565

RST = Pin(16, Pin.OUT)
A0 = Pin(0, Pin.OUT)
CS = Pin(15, Pin.OUT)
spibus = SPI(1, baudrate=1000000, polarity=1, phase=1)

display = ST7565(spibus, A0, CS, RST)
display.fill(1)
display.show()
```
