import wget
import hashlib
import zipfile
import tempfile
import os
from .CoePyConstants import PATHS , CHECKSUMS , ARCHIVE_URL
from .CoePyLogger import LogINFO , LogFATAL , LogWARNING

ARCHIVE_CURRENT_DIR = os.path.abspath("CoePyData.zip")
ARCHIVE_TEMP_DIR = os.path.abspath(tempfile.gettempdir() + "/CoePyData.zip")

class CoePyResourceDeployer(object):
    _mLogProgress = None
    def __init__(self , logProgress = True):
        self._mLogProgress = logProgress

    def deploy(self):
        if not os.path.exists(PATHS['CoePy']):
            os.mkdir(PATHS['CoePy'])
        if not os.path.exists(PATHS['CaptchaLetterData']) or not os.path.exists(PATHS['ChromeDriver']):
            return self.__deployCoePyData__(PATHS['CoePy'])
        MD5_CTX = hashlib.md5()
        for i in os.listdir(PATHS['CaptchaLetterData']):
            with open(PATHS['CaptchaLetterData'] + "/" + i , "rb") as fp:
                MD5_CTX.update(fp.read())
        if not MD5_CTX.digest().hex() == CHECKSUMS['CaptchaLetterData']:
            return self.__deployCoePyData__(PATHS['CoePy'])
        if self._mLogProgress:
            LogINFO("resource file(s) found sucessfully... ")
        return True
    
    def __extractArchive__(self , Archive , Dir):
        try:
            if self._mLogProgress:
                LogINFO("extracting resource archive... ") 
            archive = zipfile.ZipFile(Archive , "r")
            archive.extractall(Dir)
        except:
            return False
        return True

    def __checkMd5Sum__(self , filepath , md5sum):
        MD5_CTX = hashlib.md5()
        with open(filepath , "rb") as fp:
            MD5_CTX.update(fp.read())
        return (MD5_CTX.digest().hex() == md5sum)
    
    def __deployCoePyData__(self , BDir , SkipFile = []):
        if os.path.exists(ARCHIVE_CURRENT_DIR) and ARCHIVE_CURRENT_DIR not in SkipFile:
            if not self.__checkMd5Sum__(ARCHIVE_CURRENT_DIR , CHECKSUMS['CoePyDataZip']):
                if self._mLogProgress:
                    LogWARNING("MD5 sum mismatch for archive found in current directory , looking for other sources.")
                SkipFile.append(ARCHIVE_CURRENT_DIR)
                return self.__deployCoePyData__(BDir, SkipFile = SkipFile)
            return self.__extractArchive__(ARCHIVE_CURRENT_DIR , BDir)
        elif os.path.exists(ARCHIVE_TEMP_DIR) and ARCHIVE_TEMP_DIR not in SkipFile:
            if not self.__checkMd5Sum__(ARCHIVE_TEMP_DIR , CHECKSUMS['CoePyDataZip']):
                if self._mLogProgress:
                    LogWARNING("MD5 sum mismatch for archive found in the temporary directory , looking for other sources.")
                SkipFile.append(ARCHIVE_TEMP_DIR)
                return self.__deployCoePyData__(BDir, SkipFile = SkipFile) 
            return self.__extractArchive__(ARCHIVE_TEMP_DIR, BDir)
        
        # Make sure not to go into infinite recursions on failure.
        if ARCHIVE_URL in SkipFile:
            return False
        
        # Download the archive to temp dir.
        if self._mLogProgress:
            LogINFO("downloading required resources from remote host... ")
        wget.download(ARCHIVE_URL , ARCHIVE_TEMP_DIR)
        print("\n" , end = '')
        try:
            SkipFile.remove(ARCHIVE_TEMP_DIR)
        except ValueError:
            pass
        SkipFile.append(ARCHIVE_URL)
        return self.__deployCoePyData__(BDir , SkipFile = SkipFile)
