from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class CoePyAssessmentMarkParser(object):
    _mLoginHandle = None
    def __init__(self , handle):
        self._mLoginHandle = handle

    def getInfo(self):
        return {}
