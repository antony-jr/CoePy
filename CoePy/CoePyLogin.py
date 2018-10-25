import os
import stat
import asciiplotlib as apl
from .CoePyCaptchaParser import CoePyCaptchaParser
from .CoePyLogger import LogINFO
from .CoePyConstants import URLS , PATHS , WEBDRIVER_SETTINGS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class CoePyLogin(object):
    _mDriver = None
    _mOptions = webdriver.ChromeOptions()
    def __init__(self , noheadless):
        # Just make sure that the chromedriver is executable.
        st = os.stat(PATHS['ChromeDriver'])
        os.chmod(PATHS['ChromeDriver'] , st.st_mode | stat.S_IEXEC)

        if not noheadless:
            self._mOptions.add_argument("--headless")

        self._mDriver = webdriver.Chrome(PATHS['ChromeDriver'], options = self._mOptions) 
        self._mDriver.get(URLS['mirror1'])

    def getDriver(self):
        return self._mDriver

    def reset(self):
        self._mDriver.get(URLS['mirror1'])
        return True

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
        CParser = CoePyCaptchaParser(captchaBase64Encoded , PATHS['CaptchaLetterData'])
        self.__enterValueToElement__('login_stu' , 'security_code_student' , CParser.digest())
        if not self.__clickButton__('login_stu' , 'gos'):
            return False
        return True

    def isLogged(self):
        # TODO: Check for something else , This is just for the 
        # time beign.
        try:
            WebDriverWait(self._mDriver, WEBDRIVER_SETTINGS['TimeToWait']).until(EC.presence_of_element_located((By.ID, "page")))
            el = self._mDriver.find_element_by_id("page")
        except:
            return False

        try:
            soup = BeautifulSoup(self._mDriver.find_element_by_id("resulttable").get_attribute("outerHTML") , 'html.parser')
            data = [
                    [
                        [td.string.strip() for td in tr.find_all('td') if td.string]
                        for tr in table.find_all('tr')[1:]
                    ]
                    for table in soup.find_all('table')
            ]
            
            LogINFO("showing student information... ")
            fig = apl.figure()
            fig.table(data)
            fig.show()
        except:
            return False

        return True

    def __clickButton__(self , formName , elementName):
        try:
            WebDriverWait(self._mDriver, WEBDRIVER_SETTINGS['TimeToWait']).until(EC.presence_of_element_located((By.NAME, formName)))
            el = self._mDriver.find_elements_by_name(elementName)
            el[1].click() # Note that the second button is most probabily the login button for the students.
        except TimeoutException:
            return False
        return True
        
    def __enterValueToElement__(self , formName , elementName , value):
        try:
            WebDriverWait(self._mDriver,WEBDRIVER_SETTINGS['TimeToWait']).until(EC.presence_of_element_located((By.NAME , formName)))
            el = self._mDriver.find_element_by_name(elementName)
            el.clear()
            el.send_keys(str(value))
        except TimeoutException:
            return False
        return True


