from time import sleep
from machine import Pin, SPI, RTC
import max7219

days = ['' 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def start():
  spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
  ss = Pin(5, Pin.OUT)
  display = max7219.Display(spi, ss)

  rtc = RTC()

  while True:
    (year,month,day,weekday,hour,minute,second,_) = rtc.datetime()
    date_s = "%04d %03s" % (year, days[weekday])
    date_s = "{:<8}".format(date_s)
    display.write_digits(date_s)
    sleep(3)

    (year,month,day,weekday,hour,minute,second,_) = rtc.datetime()
    date_s = "%03s %02s" % (months[month], day)
    date_s = "{:<8}".format(date_s)
    display.write_digits(date_s)
    sleep(3)

    (year,month,day,weekday,hour,minute,second,_) = rtc.datetime()
    time_s = "%02d %02d %02d" % (hour, minute, second)
    date_s = "{:<8}".format(date_s)
    display.write_digits(time_s)
    sleep(3)

if __name__ == "__main__":
    start()