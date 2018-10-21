import sys
import time
import wget
import hashlib
import zipfile
import tempfile
import os
from selenium.common.exceptions import WebDriverException
from .CoePyLogger import LogINFO , LogWARNING , LogFATAL
from .CoePyArgumentParser import CoePyArgumentParser
from .CoePyLogin import CoePyLogin
from .CoePyAssessmentMarkParser import CoePyAssessmentMarkParser

VERSION = "0.0.1"
CAPTCHA_LETTER_DATA_MD5_SUM = "41e088efc3ec615cf1c45fe4db40f14d"
COEPY_DATA_ZIP_MD5_SUM = "5869794dc97a753c901c6793a1035d58"

def PrintHead():
    print("CoePy , A Powerful CLI Tool to Retrive Information from Anna University.")
    print("Copyright (C) 2018 , Antony Jr.\n")
    return True

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
        LogFATAL("cannot deploy resources!")
        sys.exit(-1)

    LogINFO("loading login page... ")
    try:
        LoginHandle = CoePyLogin(NoHeadless)
    except (KeyboardInterrupt , TypeError, WebDriverException) as e:
            if type(e).__name__ == 'WebDriverException':
                LogWARNING("it seems that you closed the automatically controlled browser.")
            LogFATAL("loading failed because of " , type(e).__name__ , ".")
            sys.exit(-1)

    LogINFO("waiting to set register number... ")
    LoginHandle.setRegisterNumber(RegisterNumber)
    LogINFO("register number successfully set... ")
    LogINFO("waiting to set date of birth... ")
    LoginHandle.setDateOfBirth(DateOfBirth)
    LogINFO("date of birth sucessfully set... ")
    LogINFO("solving captcha and logging in... ")
    LoginHandle.login()

    if not LoginHandle.isLogged():
        LogFATAL("invalid login data given , giving up!")
        time.sleep(10) # For Debuging purpose.
        sys.exit(-2)

    Parser = None
    if ArgumentParser.getValue('assessment_mark'):
        LogInfo("parsing information for assessment mark... ")
        Parser = CoePyAssessmentMarkParser(LoginHandle)
    else:
        LogFATAL("no mode is selected , atleast pass --assessment-mark option.")
        sys.exit(-3)
    sys.exit(0)
