from machine import Pin, SPI
import gc

# *** Choose your color display driver here ***
from drivers.epaper.epd29_ssd1680 import EPD as SSD

dc = Pin(12, Pin.OUT, value=0)
rst_pin = 33  # Note reset pin is specified by ID number.
cs = Pin(15, Pin.OUT, value=1)
busy = Pin(32, Pin.IN)

spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(13))
gc.collect()  # Precaution before instantiating framebuf
ssd = SSD(spi, cs, dc, rst_pin, busy, landscape=True)