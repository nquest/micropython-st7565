#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from micropython import const
from time import sleep_ms, sleep_us
import framebuf

# LCD Commands definition
CMD_DISPLAY_ON = const(0xAF)
CMD_DISPLAY_OFF = const(0xAF)
CMD_SET_START_LINE = const(0x40)
CMD_SET_PAGE = const(0xB0)
CMD_COLUMN_UPPER = const(0x10)
CMD_COLUMN_LOWER = const(0x00)
CMD_SET_ADC_NORMAL = const(0xA0)
CMD_SET_ADC_REVERSE = const(0xA1)
CMD_SET_COL_NORMAL = const(0xC0)
CMD_SET_COL_REVERSE = const(0xC8)
CMD_SET_DISPLAY_NORMAL = const(0xA6)
CMD_SET_DISPLAY_REVERSE = const(0xA7)
CMD_SET_ALLPX_ON = const(0xA5)
CMD_SET_ALLPX_NORMAL = const(0xA4)
CMD_SET_BIAS_9 = const(0xA2)
CMD_SET_BIAS_7 = const(0xA3)
CMD_DISPLAY_RESET = const(0xE2)
CMD_NOP = const(0xE3)
CMD_TEST = const(0xF0)  # Exit this mode with CMD_NOP
CMD_SET_POWER = const(0x28)
CMD_SET_RESISTOR_RATIO = const(0x20)
CMD_SET_VOLUME = const(0x81)

# Display parameters
DISPLAY_W = const(128)
DISPLAY_H = const(64)
DISPLAY_CONTRAST = const(0x1B)
DISPLAY_RESISTOR_RATIO = const(5)
DISPLAY_POWER_MODE = 7


class ST7565(framebuf.FrameBuffer):
    """ST7565 Display controller driver"""
    def __init__(self, spi, a0, cs, rst):
        self.spi = spi
        self.rst = rst
        self.a0 = a0
        self.cs = cs
        self.width = DISPLAY_W
        self.height = DISPLAY_H
        self.buffer = bytearray(1024)
        super().__init__(
            self.buffer,
            self.width,
            self.height,
            framebuf.MONO_VLSB)
        self.display_init()

    def display_init(self):
        self.reset()
        sleep_ms(1)
        for cmd in (
            CMD_DISPLAY_OFF,  # Display off
            CMD_SET_BIAS_9,  # Display drive voltage 1/9 bias
            CMD_SET_ADC_REVERSE,  # Reverse SEG
            CMD_SET_COL_NORMAL,  # Commmon mode normal direction
            CMD_SET_RESISTOR_RATIO + DISPLAY_RESISTOR_RATIO,  # V5 R ratio
            CMD_SET_VOLUME,  # Contrast
            DISPLAY_CONTRAST,  # Contrast value
            CMD_SET_POWER + DISPLAY_POWER_MODE):
            self.write_cmd(cmd)
        self.show()
        self.write_cmd(CMD_DISPLAY_ON)

    def write_cmd(self, cmd):
        self.a0(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.a0(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)

    def set_contrast(self, value):
        if 0x1 <= value <= 0x3f:
            for cmd in (
                CMD_SET_VOLUME,
                value):
                    self.write_cmd(cmd)

    def reset(self):
        self.rst(0)
        sleep_us(1)
        self.rst(1)

    def show(self):
        for i in range(8):
            for cmd in (
                CMD_SET_START_LINE,
                CMD_SET_PAGE + i,
                CMD_COLUMN_UPPER,
                CMD_COLUMN_LOWER):
                self.write_cmd(cmd)
            self.write_data(self.buffer[i*128:(i+1)*128])
