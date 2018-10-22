import os

# COE AU Website Links
URLS = {
    'mirror1' : 'http://coe1.annauniv.edu/home/index.php',
    'mirror2' : 'http://coe2.annauniv.edu/home/index.php',
}

# MD5 Checksums for critical data.
CHECKSUMS = {
        'CaptchaLetterData' : '41e088efc3ec615cf1c45fe4db40f14d',
        'CoePyDataZip' : '5869794dc97a753c901c6793a1035d58'
}

# CoePy Data Paths.
PATHS = {
        'CoePy' : str(str(os.path.expanduser('~')) + '/.CoePy'),
        'CaptchaLetterData' : str(str(os.path.expanduser('~')) + '/.CoePy/CaptchaLetterData'),
        'ChromeDriver' : str(str(os.path.expanduser('~')) + '/.CoePy/chromedriver')
}

# Currrent ToolSet Required Global Information.
COEPY_INFO = {
        'Version' : '0.0.1'
}

# WebDriver Render Settings.
WEBDRIVER_SETTINGS = {
        'TimeToWait' : 10
}

# Remote Host where CoePy Data is kept.
ARCHIVE_URL = "https://github.com/antony-jr/CoePy/releases/download/v"+COEPY_INFO['Version']+"/CoePyData.zip"
