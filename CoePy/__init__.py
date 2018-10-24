import sys
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

    if (ArgumentParser.isEmpty() or
            ArgumentParser.getValue('register_number') is None or 
                ArgumentParser.getValue('date_of_birth') is None):
        ArgumentParser.printHelp()
        sys.exit(0)

    RegisterNumber = ArgumentParser.getValue('register_number')
    DateOfBirth = ArgumentParser.getValue('date_of_birth')
    NoHeadless = ArgumentParser.getValue('no_headless')
    DoVerbose = ArgumentParser.getValue('verbose')
    
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
        sys.exit(-2)

    Parser = None
    if ArgumentParser.getValue('assessment_mark'):
        LogINFO("parsing information for assessment mark... ")
        Parser = CoePyAssessmentMarkParser(LoginHandle)
    else:
        LogFATAL("no mode is selected , atleast pass --assessment-mark option.")
        sys.exit(-3)
    sys.exit(0)
