#!/usr/bin/python3
import sys
import base64
from PIL import Image
from CoePy.CoePyCaptchaParser import CoePyCaptchaParser as CP

if __name__ == "__main__":
    print("CoePy CPT , Captcha Parser Tester.")
    print("Copyright (C) 2018 , Antony Jr.\n")
    
    if len(sys.argv) < 3:
        print("Usage: {} [CAPCHA IMAGE] [CAPTCHA LETTER DATA DIR]")
        sys.exit(0)

    CaptchaImg = sys.argv[1]
    LetterDataDir = sys.argv[2]
    Encoded = None
    with open(CaptchaImg , 'rb') as fp:
        Encoded = base64.b64encode(fp.read())
    Parser = CP(Encoded , LetterDataDir , debug = False)
    print("Digest: " , Parser.digest())
    sys.exit(0)
