import os
import stat
from .CoePyCaptchaParser import CoePyCaptchaParser
from .CoeLinks import URLS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

TIME_TO_WAIT_FOR_RENDER = 10
CAPTCHA_LETTER_DATA_DIR = str(os.path.expanduser('~')) + "/.CoePy/CoePyLetterData"
CHROME_DRIVER = str(os.path.expanduser('~')) + "/.CoePy/chromedriver"

class CoePyLogin(object):
    _mDriver = None
    _mOptions = webdriver.ChromeOptions()
    def __init__(self , noheadless):
        # Just make sure that the chromedriver is executable.
        st = os.stat(CHROME_DRIVER)
        os.chmod(CHROME_DRIVER , st.st_mode | stat.S_IEXEC)

        if not noheadless:
            self._mOptions.add_argument("--headless")

        self._mDriver = webdriver.Chrome(CHROME_DRIVER , options = self._mOptions) 
        self._mDriver.get(URLS['mirror1'])

    def getDriver(self):
        return self._mDriver

    def setRegisterNumber(self , regno):
        return self.__enterValueToElement__('login_stu' , 'register_no' , regno)
    
    def setDateOfBirth(self , dob):
        return self.__enterValueToElement__('login_stu' , 'dob' , dob)

    def login(self):
        indexContent = self._mDriver.page_source
        indexContent = ((indexContent.split("login_stu"))[2]).split()
        captchaBase64Encoded = None
        for j in indexContent:
            if "base64" in j:
                captchaBase64Encoded = ((j.split("base64,"))[1]).split('"')[0]
                break
        CParser = CoePyCaptchaParser(captchaBase64Encoded , LETTER_DATA_DIR)
        self.__enterValueToElement__('login_stu' , 'security_code_student' , CParser.digest())
        if not self.__clickButton__('login_stu' , 'gos'):
            return False
        return True

    def isLogged(self):
        return False

    def __clickButton__(self , formName , elementName):
        try:
            WebDriverWait(self._mDriver, TIME_TO_WAIT_FOR_RENDER).until(EC.presence_of_element_located((By.NAME, formName)))
            el = self._mDriver.find_elements_by_name(elementName)
            el[1].click() # Note that the second button is most probabily the login button for the students.
        except TimeoutException:
            return False
        return True
        
    def __enterValueToElement__(self , formName , elementName , value):
        try:
            WebDriverWait(self._mDriver, TIME_TO_WAIT_FOR_RENDER).until(EC.presence_of_element_located((By.NAME , formName)))
            el = self._mDriver.find_element_by_name(elementName)
            el.clear()
            el.send_keys(str(value))
        except TimeoutException:
            return False
        return True


