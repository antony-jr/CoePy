#!/usr/bin/python3
import numpy as np
import sys
import os
from PIL import Image

class CoePyCaptchaLetterWriter(object):
    _mCaptchaLetterRaw = dict()
    _mOutputDir = "./"
    def __init__(self , output , letters = None):
        self._mOutputDir = output
        if letters is not None:
            for e in letters:
                self.stack(e)

    def stack(self , LetterImagePath):
        try:
            LetterName = os.path.basename(os.path.splitext(LetterImagePath)[0]).replace('Letter' ,'')
            self._mCaptchaLetterRaw[LetterName] = self.__image2PixelArray__(LetterImagePath)
        except:
            print("Warning: Cannot Open '{}'.".format(LetterImagePath))

    def write(self):
        try:
            item = self._mCaptchaLetterRaw.popitem()
            print("Processed Parser Letter Data({}): \n{}".format(item[0] , item[1]))
            np.savetxt(self._mOutputDir + "/Letter" + item[0] + ".dat" , item[1])
            print("Written Sucessfully!")
        except:
            print("Fatal Error: Cannot write data.")

    def writeAll(self):
        for i in range(len(self._mCaptchaLetterRaw)):
            self.write()
        return True

    def __image2PixelArray__(self , filepath):
        im = Image.open(filepath).convert('L')
        (width, height) = im.size
        greyscale_map = list(im.getdata())
        greyscale_map = np.array(greyscale_map)
        greyscale_map = greyscale_map.reshape((height, width))
        return greyscale_map


if __name__ == "__main__":
    print("CoePy CLW v1 , Captcha Letter Writer.")
    print("Copyright (C) 2018 Antony Jr.\n")
    if len(sys.argv) < 2:
        print("Usage: {} [OUTPUT DATA DIRECTORY] [CAPCHA LETTER IMAGE PATH(s)]".format(sys.argv[0]))
        sys.exit(0)
    Writer = CoePyCaptchaLetterWriter(sys.argv[1])
    for e in sys.argv:
        if e == sys.argv[0] or e == sys.argv[1]:
            continue
        Writer.stack(e)
    Writer.writeAll()
    sys.exit(0)
