from pywizard.tools import formatSpecifier
from pywizard.userSettings import settings
import logging

class HexConverter(object):
    formats = {
        "arduino" : formatSpecifier("const unsigned char FILENAME[] PROGMEM = {",
                     "0x{:02X}",
                     ",",
                     "};"),
        "C"       : formatSpecifier("const unsigned char FILENAME[] = {",
                     "0x{:02X}",
                     ",",
                     "};"),
        "Ada"       : formatSpecifier("FILENAME : aliased constant LPC_Synth.LPC_Data := (",
                     "16#{:02X}#",
                     ", ",
                     ");"),
        "hex"     : formatSpecifier("",
                     "{:02x}",
                     " ",
                     ""),
        "python" : formatSpecifier("(",
                     "0x{:02X}",
                     ",",
                     ")"),
                    }

    @classmethod
    def preprocess(cls, nibbles):
        '''
        Creates nibble swapped, reversed data bytestream as hex value list.
        Used to be NibbleBitReverser, NibbleSwitcher and HexConverter
        '''
        result = []
        for u,l in zip(nibbles[0::2], nibbles[1::2]):
            if settings.nonInvertedBits:
                raw = (u+l)
            else:
                raw = (u+l)[::-1]
            result.append(int(raw, base=2))
        return result

    @classmethod
    def process(cls, nibbles):
        formatter = cls.formats[settings.outputFormat]
        logging.debug("Will format output using {} ({})".format(settings.outputFormat, formatter ))
        result=[ formatter.formatString.format(data) for data in cls.preprocess(nibbles) ]
        return formatter.header + formatter.separator.join(result) + formatter.trailer


