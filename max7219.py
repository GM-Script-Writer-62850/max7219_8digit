# Licence: GPLv3
# Copyright 2017 Paul Dwerryhouse <paul@dwerryhouse.com.au>

CHAR_MAP = {
    '0': 0x7e, '1': 0x30, '2': 0x6d, '3': 0x79,
    '4': 0x33, '5': 0x5b, '6': 0x5f, '7': 0x70,
    '8': 0x7f, '9': 0x7b, 'a': 0x77, 'b': 0x1f,
    'c': 0x4e, 'd': 0x3d, 'e': 0x4f, 'f': 0x47,
    'g': 0x7b, 'h': 0x37, 'i': 0x30, 'j': 0x3c,
    'k': 0x57, 'l': 0x0e, 'm': 0x54, 'n': 0x15,
    'o': 0x1d, 'p': 0x67, 'q': 0x73, 'r': 0x05,
    's': 0x5b, 't': 0x0f, 'u': 0x1c, 'v': 0x3e,
    'w': 0x2a, 'x': 0x37, 'y': 0x3b, 'z': 0x6d,
    'A': 0x77, 'B': 0x1f, 'C': 0x4e, 'D': 0x3d,
    'E': 0x4f, 'F': 0x47, 'G': 0x7b, 'H': 0x37,
    'I': 0x30, 'J': 0x3c, 'K': 0x57, 'L': 0x0e,
    'M': 0x54, 'N': 0x15, 'O': 0x1d, 'P': 0x67,
    'Q': 0x73, 'R': 0x05, 'S': 0x5b, 'T': 0x0f,
    'U': 0x1c, 'V': 0x3e, 'W': 0x2a, 'X': 0x37,
    'Y': 0x3b, 'Z': 0x6d, ' ': 0x00, '-': 0x01,
    '\xb0': 0x63, '.': 0x80
}

INT_MAP = [
    #  0    1    2    3    4    5    6    7    8    9
    0x7e,0x30,0x6d,0x79,0x33,0x5b,0x5f,0x70,0x7f,0x7b,
]

REG_NO_OP           = 0x00
REG_DIGIT_BASE      = 0x01
REG_DECODE_MODE     = 0x09
REG_INTENSITY       = 0x0a
REG_SCAN_LIMIT      = 0x0b
REG_SHUTDOWN        = 0x0c
REG_DISPLAY_TEST    = 0x0f

class Display:

    def __init__(self, spi, cs, intensity=3, scan_limit=7):
        self.spi = spi
        self.cs = cs
        self.intensity = intensity
        self.scan_limit = scan_limit # This should be equal to 8 times the number of MAX7219 chips in use minus 1
        self.reset()

    def reset(self):
        self.set_register(REG_DECODE_MODE, 0)
        self.set_register(REG_INTENSITY, self.intensity)
        self.set_register(REG_SCAN_LIMIT, self.scan_limit)
        self.set_register(REG_DISPLAY_TEST, 0)
        self.set_register(REG_SHUTDOWN, 1)

    def set_register(self, register, value):
        self.cs.off()
        self.spi.write(bytearray([register, value]))
        self.cs.on()

    def decode_char(self, c):
        d = CHAR_MAP.get(c)
        return d if d != None else ' '

    def valid_length(self, l):
        if l is None:
            return self.scan_limit
        else:
            l=int(l)
            if 0 <= l <= self.scan_limit:
                return l
            raise Exception(f"Last digit position is out of range, must be 0 - {self.scan_limit}")

    def write_digits(self, s, l=None):
        # s is the value to show
        # l is the last digit to show, starts at 0
        buffer=[]
        s=str(s)
        i=len(s)
        l=self.valid_length(l)

        while i > 0 and l > -1:
            i -= 1
            if i > 0 and s[i] == '.':
                i -= 1
                while  i > -1 and s[i] == '.' and l > -1:
                    buffer.append([REG_DIGIT_BASE + l, 0x80])
                    l -= 1
                    i -= 1
                digit = self.decode_char(s[i]) | 0x80
            else:
                digit = self.decode_char(s[i])
            buffer.append([REG_DIGIT_BASE + l, digit])
            l -= 1
        else:
            if i > 0:
                print(s,'has',i,'digits too many to display...')
        for i in buffer:
            self.set_register(*i)

    def r_write_digits(self, value, start=0):
        # value is the data to show
        # start is the 1st digit's position

        #value=str(value)[::-1]# This is not implemented in micropython for strings
        value=''.join(reversed(value))# performance penalty
        self.write_digits(value, self.scan_limit-start)

    def write_digits_from_array(self, a, l=None):
        # a is a array of integers to show (add 10 to apply a decimal point)
        # l is the last digit to show, starts at 0
        buffer=[]
        i=len(a)
        l=self.valid_length(l)

        while i > 0 and l > -1:
            i -= 1
            if a[i] > 9:
                digit = INT_MAP[a[i]-10] | 0x80
            else:
                digit = INT_MAP[a[i]]
            buffer.append([REG_DIGIT_BASE + l, digit])
            l -= 1
        else:
            if i > 0:
                print(a,'\nhas',i,'digits too many to display...')
        for i in buffer:
            self.set_register(*i)

    def r_write_digits_from_array(self, value, start=0):
        # value is the data to show
        # start is the 1st digit's position
        self.write_digits_from_array(value[::-1], self.scan_limit-start)

    def set_intensity(self, i):
        self.intensity = i
        self.set_register(REG_INTENSITY, self.intensity)

    def set_scan_limit(self, l):
        self.scan_limit = l
        self.set_register(REG_SCAN_LIMIT, self.scan_limit)
