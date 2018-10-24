#!/usr/bin/python3
import sys
from CoePy.CoePyConstants import PATHS as P
from CoePy.CoePyResourceDeployer import CoePyResourceDeployer as RD
from CoePy.CoePyCaptchaParser import CoePyCaptchaParser as CP
from CoePy.CoePyLogger import LogINFO as L
if __name__ == "__main__":
    print("CoePy CPT , A Powerful tool to test the Captcha parser.")
    print("Copyright (C) 2018 , Antony Jr.\n")
    if len(sys.argv) == 1:
        print("Usage: {} [CAPCHA IMAGE]".format(sys.argv[0]))
        sys.exit(0)
    elif not RD().deploy():
        sys.exit(-1)
    L("Digest: " , CP(sys.argv[1] , P["CaptchaLetterData"] , debug = False , logProgress = True , base64Encoded = False).digest())
    sys.exit(0)
