#!/usr/bin/python3
import sys
import os
import base64
import zipfile
import tempfile
import wget
import hashlib
from PIL import Image
from CoePy.CoePyCaptchaParser import CoePyCaptchaParser as CP
from CoePy.CoePyLogger import LogINFO , LogWARNING , LogFATAL

VERSION = "0.0.1"
CAPTCHA_LETTER_DATA_MD5_SUM = "41e088efc3ec615cf1c45fe4db40f14d"
COEPY_DATA_ZIP_MD5_SUM = "5869794dc97a753c901c6793a1035d58"

def ExtractArchive(Archive , Dir):
    try:
        LogINFO("extracting resource archive... ") 
        archive = zipfile.ZipFile(Archive , "r")
        archive.extractall(Dir)
    except:
        return False
    return True

def DeployCoePyData(BDir , SkipFile = []):
    ARCHIVE_URL = "https://github.com/antony-jr/CoePy/releases/download/v"+VERSION+"/CoePyData.zip"
    ARCHIVE_CURRENT_DIR = os.path.abspath("CoePyData.zip")
    ARCHIVE_TEMP_DIR = os.path.abspath(tempfile.gettempdir() + "/CoePyData.zip")
    if os.path.exists(ARCHIVE_CURRENT_DIR) and ARCHIVE_CURRENT_DIR not in SkipFile:
        MD5_CTX = hashlib.md5()
        with open(ARCHIVE_CURRENT_DIR , "rb") as fp:
            MD5_CTX.update(fp.read())
        if not MD5_CTX.digest().hex() == COEPY_DATA_ZIP_MD5_SUM:
            LogWARNING("MD5 sum mismatch for archive found in current directory , looking for other sources.")
            SkipFile.append(ARCHIVE_CURRENT_DIR)
            return DeployCoePyData(BDir, SkipFile = SkipFile)
        return ExtractArchive(ARCHIVE_CURRENT_DIR , BDir)
    elif os.path.exists(ARCHIVE_TEMP_DIR) and ARCHIVE_TEMP_DIR not in SkipFile:
        MD5_CTX = hashlib.md5()
        with open(ARCHIVE_TEMP_DIR , "rb") as fp:
            MD5_CTX.update(fp.read())
        if not MD5_CTX.digest().hex() == COEPY_DATA_ZIP_MD5_SUM:
            LogWARNING("MD5 sum mismatch for archive found in the temporary directory , looking for other sources.")
            SkipFile.append(ARCHIVE_TEMP_DIR)
            return DeployCoePyData(BDir, SkipFile = SkipFile) 
        return ExtractArchive(ARCHIVE_TEMP_DIR, BDir)

    # Make sure not to go into infinite recursions on failure.
    if ARCHIVE_URL in SkipFile:
        return False
    
    # Download the archive to temp dir.
    LogINFO("downloading required resources from remote host... ")
    wget.download(ARCHIVE_URL , ARCHIVE_TEMP_DIR)
    print("\n" , end = '')
    try:
        SkipFile.remove(ARCHIVE_TEMP_DIR)
    except ValueError:
        pass

    SkipFile.append(ARCHIVE_URL)
    return DeployCoePyData(BDir , SkipFile = SkipFile)

def CheckRequiredBinaries():
    BINARY_DIR = str(os.path.expanduser('~')) + "/.CoePy"
    if not os.path.exists(BINARY_DIR):
        os.mkdir(BINARY_DIR)

    CAPTCHA_LETTER_DATA = BINARY_DIR + "/CaptchaLetterData"
    CHROMEDRIVER = BINARY_DIR + "/chromedriver"   
    
    if not os.path.exists(CAPTCHA_LETTER_DATA) or not os.path.exists(CHROMEDRIVER):
        return DeployCoePyData(BINARY_DIR)
    else:
        MD5_CTX = hashlib.md5()
        for i in os.listdir(CAPTCHA_LETTER_DATA):
            with open(CAPTCHA_LETTER_DATA + "/" + i , "rb") as fp:
                MD5_CTX.update(fp.read())
        if not MD5_CTX.digest().hex() == CAPTCHA_LETTER_DATA_MD5_SUM:
            return DeployCoePyData(BINARY_DIR)

    LogINFO("resource file(s) found sucessfully... ")
    return True

if __name__ == "__main__":
    print("CoePy CPT , Captcha Parser Tester.")
    print("Copyright (C) 2018 , Antony Jr.\n")
    
    if len(sys.argv) == 1:
        print("Usage: {} [CAPCHA IMAGE]")
        sys.exit(0)

    if not CheckRequiredBinaries():
        LogFATAL("unable to get resources.")
        sys.exit(-1)

    CaptchaImg = sys.argv[1]
    LetterDataDir = os.path.expanduser('~') + "/.CoePy/CaptchaLetterData"
    Encoded = None
    with open(CaptchaImg , 'rb') as fp:
        Encoded = base64.b64encode(fp.read())
    Parser = CP(Encoded , LetterDataDir , debug = False)
    LogINFO("Digest: " , Parser.digest())
    sys.exit(0)
