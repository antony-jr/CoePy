from datetime import datetime

now = datetime.now

def LogINFO(*args):
    return print("[ {} ]    INFO: ".format(now()) , "".join(args))

def LogWARNING(*args):
    return print("[ {} ] WARNING: ".format(now()) , "".join(args))

def LogFATAL(*args):
    return print("[ {} ]   FATAL: ".format(now()) , "".join(args))




