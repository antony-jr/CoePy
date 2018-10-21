import sys
import time
import hashlib
import zipfile
import tempfile
import os
from .CoePyArgumentParser import CoePyArgumentParser
from .CoePyLogin import CoePyLogin
from .CoePyAssessmentMarkParser import CoePyAssessmentMarkParser

VERSION = 0.1
CAPTCHA_LETTER_DATA_MD5_SUM = "41e088efc3ec615cf1c45fe4db40f14d"
COEPY_DATA_ZIP_MD5_SUM = "5869794dc97a753c901c6793a1035d58"

def PrintHead():
    print("CoePy , A Powerful CLI Tool to Retrive Information from Anna University.")
    print("Copyright (C) 2018 , Antony Jr.\n")
    return True

def ExtractArchive(Archive , Dir):
    try:
        archive = zipfile.ZipFile(Archive , "r")
        archive.extractall(Dir)
    except:
        return False
    return True

def DeployCoePyData(BDir , SkipFile = ""):
    ARCHIVE_URL = ""
    ARCHIVE_CURRENT_DIR = os.path.abspath("CoePyData.zip")
    ARCHIVE_TEMP_DIR = os.path.abspath(tempfile.gettempdir() + "/CoePyData.zip")
    if os.path.exists(ARCHIVE_CURRENT_DIR) and SkipFile != ARCHIVE_CURRENT_DIR:
        MD5_CTX = hashlib.md5()
        with open(ARCHIVE_CURRENT_DIR , "rb") as fp:
            MD5_CTX.update(fp.read())
        if not MD5_CTX.digest().hex() == COEPY_DATA_ZIP_MD5_SUM:
            return DeployCoePyData(BDir, SkipFile = ARCHIVE_CURRENT_DIR)
        return ExtractArchive(ARCHIVE_CURRENT_DIR , BDir)
    elif os.path.exists(ARCHIVE_TEMP_DIR) and SkipFile != ARCHIVE_TEMP_DIR:
        MD5_CTX = hashlib.md5()
        with open(ARCHIVE_TEMP_DIR , "rb") as fp:
            MD5_CTX.update(fp.read())
        if not MD5_CTX.digest().hex() == COEPY_DATA_ZIP_MD5_SUM:
            return DeployCoePyData(BDir, SkipFile = ARCHIVE_TEMP_DIR) 
        return ExtractArchive(ARCHIVE_TEMP_DIR, BDir)
    # Download to temporary directory.
    return DeployCoePyData(BDir)

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
    return True

def ExecuteCoePy():
    PrintHead()
    ArgumentParser = CoePyArgumentParser()

    if (ArgumentParser.isEmpty() or
            ArgumentParser.getValue('register_number') is None or 
                ArgumentParser.getValue('date_of_birth') is None):
        ArgumentParser.printHelp()
        sys.exit(0)

    RegisterNumber = ArgumentParser.getValue('register_number')
    DateOfBirth = ArgumentParser.getValue('date_of_birth')
    NoHeadless = ArgumentParser.getValue('no_headless')
    DoVerbose = ArgumentParser.getValue('verbose')
    
    if not CheckRequiredBinaries():
        print("ERROR: cannot deploy resources.")
        sys.exit(-1)

    LoginHandle = CoePyLogin(NoHeadless)
    LoginHandle.setRegisterNumber(RegisterNumber)
    LoginHandle.setDateOfBirth(DateOfBirth)
    LoginHandle.login()

    if not LoginHandle.isLogged():
        print("ERROR: cannot login , invalid data.")
        time.sleep(10) # For Debuging purpose.
        sys.exit(-2)

    Parser = None
    if ArgumentParser.getValue('assessment_mark'):
        Parser = CoePyAssessmentMarkParser(LoginHandle)
    else:
        print("ERROR: you should select an mode , such as , --assessment-mark.")
        sys.exit(-3)

    print("INFO: " , Parser.getInfo())
