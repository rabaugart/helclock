import time
import c3

s = c3.Spi()

while True:
    s.puttime()
    time.sleep(1.0)
