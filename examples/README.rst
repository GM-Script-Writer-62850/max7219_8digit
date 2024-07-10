
This is a very simple clock demonstration for the MAX7219 + 8 x 7 digit board
on an PICO with micropython.

To use:

.. code:: python

   import simple_clock
   simple_clock.start()

This is script make sure the LEDs work

To use:

.. code:: python

   import led_test
   led_test.start()

This is debug script to check if the display is behaving as expected

To use:

.. code:: python

   import debug_max7219
   debug_max7219.start()
