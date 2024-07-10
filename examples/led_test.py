from time import sleep
from machine import Pin, SPI
import max7219

def start():
  spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
  ss = Pin(5, Pin.OUT)
  display = max7219.Display(spi, ss, intensity=0)
  
  digits=range(display.scan_limit+1)
  segments=['A','B','C','D','E','F','G','.']
  delay=0.5

  print("Blank display")
  display.write_all_digits('')
  sleep(delay)
  
  while True:
    for d in digits:
      print("Test Digit",d,"Start")
      for s in segments:
        print("  Test Segment",s)
        display.write_digit_segments([s],d)
        sleep(delay)
      print("Test Digit",d,"End")
      display.write_digit_segments([],d)
      sleep(delay)

    print("Test all digits")
    for s in segments:
      print("  Test Segment",s)
      for d in digits:
        display.write_digit_segments([s],d)
      sleep(delay)
      for d in digits:
        display.write_digit_segments([],d)
      sleep(delay)

    for d in digits:
      print("Test Digit",d,"Start")
      segs=[]
      for s in segments:
        print("  Add Segment",s)
        segs.append(s)
        display.write_digit_segments(segs,d)
        sleep(delay)
      print("Test Digit",d,"End")
      display.write_digit_segments([],d)
      sleep(delay)

    print("Test all digits")
    segs=[]
    for s in segments:
      print("  Add Segment",s)
      segs.append(s)
      for d in digits:
        display.write_digit_segments(segs,d)
      sleep(delay)
      for d in digits:
        display.write_digit_segments([],d)
    sleep(delay)

if __name__ == "__main__":
    start()
