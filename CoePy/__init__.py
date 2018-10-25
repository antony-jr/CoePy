import sys
import time
import json
from selenium.common.exceptions import WebDriverException , NoSuchWindowException
from .CoePyResourceDeployer import CoePyResourceDeployer
from .CoePyArgumentParser import CoePyArgumentParser
from .CoePyLogin import CoePyLogin
from .CoePyAssessmentMarkParser import CoePyAssessmentMarkParser
from .CoePyLogger import LogFATAL , LogINFO , LogWARNING

def PrintHead():
    print("CoePy , A Powerful CLI Tool to Retrive Information from Anna University.")
    print("Copyright (C) 2018 , Antony Jr.\n")
    return True

def ExecuteCoePy():
    PrintHead()
    ArgumentParser = CoePyArgumentParser()
    Deployer = CoePyResourceDeployer()

    if ((ArgumentParser.isEmpty() or
            ArgumentParser.getValue('register_number') is None or 
                ArgumentParser.getValue('date_of_birth') is None) and 
                    (ArgumentParser.getValue('json_info_file') is None)):
        ArgumentParser.printHelp()
        sys.exit(0)


    RegisterNumber = None
    DateOfBirth = None 
    if ArgumentParser.getValue('json_info_file') is not None:
        info = None
        try:
            with open(ArgumentParser.getValue('json_info_file') , 'r') as fp:
                info = json.load(fp)
        except:
            LogFATAL("error parsing json info file at '" , ArgumentParser.getValue('json_info_file') , "'.")
            sys.exit(-1)

        try:
            RegisterNumber = info['regno']
            DateOfBirth = info['dob']
        except:
            LogFATAL("invalid information given in json file.")
            sys.exit(-1)
    else:
        RegisterNumber = ArgumentParser.getValue('register_number')
        DateOfBirth = ArgumentParser.getValue('date_of_birth')

    NoHeadless = ArgumentParser.getValue('no_headless')
    DoVerbose = ArgumentParser.getValue('verbose')
    DoQuickBrowse = ArgumentParser.getValue('quick_browse')
    NoHeadless = DoQuickBrowse # If Quick Browse then chromium cannot be in headless mode.

    if not Deployer.deploy():
        LogFATAL("cannot deploy resources!")
        sys.exit(-1)

    LogINFO("loading login page... ")
    try:
        LoginHandle = CoePyLogin(NoHeadless)
    except (KeyboardInterrupt , TypeError, WebDriverException , NoSuchWindowException) as e:
            if type(e).__name__ == 'WebDriverException':
                LogWARNING("it seems that you closed the automatically controlled browser.")
            LogFATAL("loading failed because of " , type(e).__name__ , ".")
            sys.exit(-1)

    LoginHandle.setRegisterNumber(RegisterNumber)
    LoginHandle.setDateOfBirth(DateOfBirth)
    LoginHandle.login()
    if not LoginHandle.isLogged():
        LogFATAL("cannot login , please try again... ")
        sys.exit(-2)

    if ArgumentParser.getValue('assessment_mark'):
        LogINFO("parsing information for assessment mark... ")
        Parser = CoePyAssessmentMarkParser(LoginHandle)
    elif DoQuickBrowse:
        LogINFO("you can now start using the automated browser , Simply close the window to end the script.")
        while True:
            try:
                LoginHandle.getDriver().title
            except:
                LogINFO("browser closed , exiting... ")
                break
            time.sleep(4)
    else:
        LogFATAL("no mode is selected , atleast pass --assessment-mark option.")
        sys.exit(-3)
    LogINFO("graceful termination.")
    sys.exit(0)
