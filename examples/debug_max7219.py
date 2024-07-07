from time import sleep
from machine import Pin, SPI
import max7219

def start():
  spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
  ss = Pin(5, Pin.OUT)
  display = max7219.Display(spi, ss, intensity=0)

  while True:

    print("Turn on ALL LEDs")
    display.write_digits("8.8.8.8.8.8.8.8.")
    sleep(3)

    print('\nShow 12345678 (as string)')
    display.write_digits('12345678')
    sleep(3)
    
    print('\nReverse above (as string)')
    display.r_write_digits('12345678')
    sleep(3)

    print('\nShow 12345678 (as array)')
    display.write_digits_from_array([1,2,3,4,5,6,7,8])
    sleep(3)

    print("\nReverse above (array)")
    display.r_write_digits_from_array([1,2,3,4,5,6,7,8])
    sleep(3)

    print("\nBlank display")
    display.write_digits('        ')
    sleep(3)

    print("\nSet middle 2 digits to 1.2")
    display.write_digits_from_array([11,2],4)
    sleep(3)

    print("\nTest number too long (string)")
    display.write_digits('3.14159265359')
    sleep(3)

    print("\nReverse test number too long (string)")
    display.r_write_digits('3.14159265359')
    sleep(3)

    print("\nTest number too long (array)")
    display.write_digits_from_array([3,11,4,1,5,9,2,6,5,3,5,9])
    sleep(3)

    print("\nReverse test number too long (array)")
    display.r_write_digits_from_array([3,11,4,1,5,9,2,6,5,3,5,9])
    sleep(3)

    print("Demo setting parts of the display separately, non-destructively")
    display.write_digits('        ')# clear display
    # The second parameter is the index of the last digit on the panel we
    #   want to set, these are numbered 0-7
    #   This is most useful when you are using 1 controller for multiple panels
    #   For example temperature and humidity, and you do not want to these
    #   values independently
    print('set 1st 2 digits')
    display.write_digits(12,1)
    sleep(1)
    print('set last 2 digits')
    display.write_digits(78,7)
    sleep(1)
    display.write_digits(45,4)
    sleep(1)
    display.write_digits(3,2)
    sleep(1)
    display.write_digits(6,5)
    sleep(3)

    print('\n')

if __name__ == "__main__":
    start()
