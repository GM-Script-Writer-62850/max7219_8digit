
This is a micropython library for MAX7219 IC.
Note that some boards using this have the numbers wired in reverse,
this library follows the order of the pinout as defined in the datasheet
of the `MAX7219 <https://www.analog.com/media/en/technical-documentation/data-sheets/MAX7219-MAX7221.pdf>`_, 
however functions are provided to reverse the order if needed.

I have tested it with a PICO, running micropython version 1.20.0.

Requires a minimum of three spare GPIO lines to run SPI.

Manual for ``write_digits``:
  This takes 2 parameters, the 1st is the value to set and the second
  is the last digit's position you want to update, counting from 0.
  This defaults to 7, the last digit using on the pin out of the MAX7219.
  This function accepts the 1st parameter as a string or number

Manual for ``write_digits_from_list``:
  This function is exclusively for setting numbers as fast as possible.
  This takes 2 parameters, the 1st is the value to set and the second
  is the last digit you want to update, counting from 0.
  This defaults to 7, the last digit using on the pin out of the MAX7219.
  This function accepts the 1st parameter as a list.
  Using 0-9 in the array will set the digit to the number given.
  Using a 10-19 will apply a decimal point to the second digit (10='0.')

Manual for ``write_digits_reverse``:
  This takes 2 parameters, the 1st is the value to set, this
  can be a number, string, or list.
  The second is the start position (defaults to 0)
  This has a performance hit when the data type is not a list!
  See source code for more info.

Manual for ``write_all_digits``:
  This takes 2 parameters, the 1st is the value to set (number, string, or list)
  and the second is a boolean indicting if the order needs to be reversed,
  defaults to False. This will pad values to the left with 0 for a list or space
  otherwise. For example with a list of ``[13,1,4]`` would become ``[0,0,0,0,0,13,1,4]``
  and a string ``12345`` would become ``   12345``, this is decimal point safe.

In Theory using a last digit value of 15 would start at the end of the second
MAX7219 connected to the DOUT pin of the 1st MAX7219

I have not tested using daisy chained MAX7219, but I think all you will need
to do is set the scan_limit higher ``max7219.Display(spi, ss, scan_limit=15)``
or ``max7219.set_scan_limit(15)`` then it should just work... I hope...


Example of use (see `debug_max7219.py <examples/debug_max7219.py>`_ for more):

.. code:: python

   # Connections:
   # SCK (CLK) -> GP2 (4)
   # MOSI (DIN) -> GP3 (5)
   # SS (CS) -> GP5 (7)
   
   from machine import Pin, SPI
   from time import sleep
   import max7219
   
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

   # Clear the display, notice this is write_all_digits, not write_digits
   display.write_all_digits('')
   sleep(3)

   # Alter digits 2 through 6
   display.write_digits('3456',5)
   sleep(3)

   # Display Pi without using string processing
   display.write_digits_from_array([13,1,4,5,9,2,6,5])
