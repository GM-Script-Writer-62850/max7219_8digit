
This is a micropython library for MAX7219 IC.
Note that some boards using this have the numbers wired in reverse,
this library follows the order of the pinout as defined in the data sheet
of the [MAX7219](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX7219-MAX7221.pdf)

I have tested it with a PICO, running micropython version 1.20.0.

Requires a minimum of three spare GPIO lines to run SPI.

Manual for `write_digits`:
  This takes 2 parameters, the 1st is the value to set and the second
  is the last digit's position you want to update, counting from 0.
  This defaults to 7, the last digit using on the pin out of the MAX7219.
  This function accepts the 1st parameter as a string or number

Manual for `r_write_digits`:
  This has a performance hit! See source code for more info
  `write_digits` but in reverse order
  This takes 2 parameters, the 1st is the value to set
  The second is the start position (defaults to 0)


Manual for `write_digits_from_array`:
  This takes 3 parameters, the 1st is the value to set and the second
  is the last digit you want to update, counting from 0.
  This defaults to 7, the last digit using on the pin out of the MAX7219.
  This function accepts the 1st parameter as an array.
  This function is exclusively for setting numbers as fast as possible.
  Using 0-9 in the array will set the digit to the number given.
  Using a 10-19 will apply a decimal point to the second digit (10='0.')

Manual for `r_write_digits_from_array`:
  `write_digits_from_array` but in reverse order
  This takes 2 parameters, the 1st is the value to set
  The second is the start position (defaults to 0)

In Theory using a last digit value of 15 would start at the end of the second
MAX7219 connected to the DOUT pin of the 1st MAX7219

I have not test using daisy chained MAX7219, but I think all you will need to do is set the scan_limit higher `max7219.Display(spi, ss, scan_limit=15)` or `max7219.set_scan_limit(15)` then it should just work... i hope


Example of use:

.. code:: python

   # Connections:
   # SCK (CLK) -> GP2 (4)
   # MOSI (DIN) -> GP3 (5)
   # SS (CS) -> GP5 (7)
   
   from machine import Pin, SPI
   from time import sleep
   import max7219_8digit
   
   spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
   ss = Pin(5, Pin.OUT)
   
   # Configure display
   # Brightness of display are 0 - 15, default is 3
   # 0 is dim and 15 is bright
   display = max7219.Display(spi, ss)
   #display = max7219.Display(spi, ss, intensity=0)

   # Change brightness
   #display.set_intensity(2)

   # Display 12345678
   display.write_digits(12345678)
   sleep(3)

   # Display 12.3456.78
   display.write_digits('12.3456.78')
   sleep(3)

   # Alter first 4 digits, digits 0 - 3
   display.write_digits(3.141,3)
   sleep(3)

   # Alter last 4 digits, digits 4 - 7
   display.write_digits(5926,7)
   sleep(3)

   # Clear the display
   display.write_digits('        ')
   sleep(3)

   # Alter digits 2 through 6
   display.write_digits('3456',5)
   sleep(3)

   # Display Pi without using string processing
   display.write_digits_from_array([13,1,4,5,9,2,6,5])
