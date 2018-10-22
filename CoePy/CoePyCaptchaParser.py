import numpy as np
import asciiplotlib as apl
import base64
import sys
import os
from PIL import Image
from io import BytesIO
from .CoePyLogger import LogFATAL

class CoePyCaptchaParser(object):
    _mCaptchaRaw = None
    _nSWindowRow = 3
    _nEWindowRow = 13
    _nSWindowCol = 5
    _nEWindowCol = 13
    _nWindowColIncreament = 10
    _nSizeOfCaptcha = 6
    _nSingleCharacterRow = 10
    _nSingleCharacterCol = 8
    _mAvailableLettersData = dict()
    _bDebug = False 
    _bLogProgress = False

    def __init__(self , base64EncodedImage , TrainedDataDir , debug = False , logProgress = False):
        # Set Debug and Logging
        self._bDebug = debug
        self._bLogProgress = logProgress

        # Load Given Image
        try:
            im = Image.open(BytesIO(base64.b64decode(base64EncodedImage))).convert('L')
        except:
            if self._bLogProgress:
                LogFATAL("given base64 encoded image cannot be processed!")
            raise RuntimeError
        (width, height) = im.size
        greyscale_map = list(im.getdata())
        greyscale_map = np.array(greyscale_map)
        if height != 20 or width != 70:
            if self._bLogProgress:
                LogFATAL("given image does is not 70 width x 20 height image!")
            raise RuntimeError

        greyscale_map = greyscale_map.reshape((height, width))
        self._mCaptchaRaw = greyscale_map

        # Get the training data.
        contents = None
        try:
            contents = os.listdir(TrainedDataDir)
        except:
            if self._bLogProgress:
                LogFATAL("data dir given cannot be accessed!")
            raise RuntimeError

        for i in contents:
            self._mAvailableLettersData[i.replace('Letter' ,'').replace('.dat' , '')] = TrainedDataDir + "/" + i

    def __init__(self , imagePath , TrainedDataDir , debug = False , logProgress = False):
        # Set Debug and Logging 
        self._bDebug = debug
        self._bLogProgress = logProgress 

        # Load Local Image
        try:
            im = Image.open(imagePath).convert('L')
        except:
            if self._bLogProgress:
                LogFATAL("cannot retrive image file from the path '" , imagePath , "'!")
            raise RuntimeError

        (width, height) = im.size
        greyscale_map = list(im.getdata())
        greyscale_map = np.array(greyscale_map)
        if height != 20 or width != 70:
            if self._bLogProgress:
                 LogFATAL("given image does is not 70 width x 20 height image!")
            raise RuntimeError

        greyscale_map = greyscale_map.reshape((height, width))
        self._mCaptchaRaw = greyscale_map
        
        
        # Get the training data.
        contents = None
        try:
            contents = os.listdir(TrainedDataDir)
        except:
            if self._bLogProgress:
                LogFATAL("data dir given cannot be accessed!")
            raise RuntimeError
        for i in contents:
            self._mAvailableLettersData[i.replace('Letter' ,'').replace('.dat' , '')] = TrainedDataDir + "/" + i
    
    def digest(self):
        result = str()
        WhitePixels = 0
        BlackPixels = 0
        
        for r in self._mCaptchaRaw:
            for c in r:
                # From the properties , We know that the captcha 
                # is a composition of white and black pixels only.
                # (i.e) The Captcha is monochromatic in nature.
                if c == 0: # RGB = (0 , 0 , 0) , Means the Pixel is black
                    BlackPixels += 1
                    continue
                WhitePixels += 1
        PMat = self._mCaptchaRaw
        # Only invert the colour if and only if the background 
        # colour is white
        if WhitePixels > BlackPixels: # => The background is white , Which is not favourable for us.
            row = 0
            col = 0
            for r in self._mCaptchaRaw:
                for c in r:
                    if c == 0:
                        PMat[row][col] = 255
                    else:
                        PMat[row][col] = 0
                    col += 1
                col = 0
                row += 1
        
        startRow = self._nSWindowRow
        endRow = self._nEWindowRow
        startCol = self._nSWindowCol
        endCol = self._nEWindowCol
        windowIncreament = self._nWindowColIncreament
        sizeOfCaptcha = self._nSizeOfCaptcha
        singleLetterRows = self._nSingleCharacterRow
        singleLetterCols = self._nSingleCharacterCol
        
        for i in range(sizeOfCaptcha):
            l = self.__getLetter__(singleLetterRows , singleLetterCols , startRow , endRow , startCol , endCol , PMat)
            MatchData = dict()
            for letter in self._mAvailableLettersData:
                data = np.loadtxt(self._mAvailableLettersData[letter])
                MatchData[self.__getPercentageOfMatch__(l , data)] = letter
            m = list(MatchData.keys())
            m.sort()
            result += MatchData[m[len(m) - 1]]
            
            # Do Debug
            if self._bDebug:
                fig = apl.figure()
                print("Percentage of Matches for Letter {}: ".format(i+1))
                data = [
                        [["Letter" , "Percentage of Match"]],
                        []
                        ]
                for e in MatchData:
                    data[1].append([MatchData[e] , e]) 
                fig.table(data)
                fig.show()
                print("Most Appropriate Letter: '{}'.\n".format(MatchData[m[len(m)-1]]))

            startCol += windowIncreament
            endCol += windowIncreament
        return result

    def __getLetter__(self , singleLetterRows , singleLetterCols , startRow , endRow , startCol , endCol , PMat):
        LMat = np.zeros([singleLetterRows , singleLetterCols])
        row = 0
        col = 0
        for r in range(startRow , endRow):
            for c in range(startCol, endCol):
                LMat[row][col] = PMat[r][c]
                if col < 7:
                    col += 1
            col = 0
            if row < 9:
                row += 1
        return LMat

    def __getNumberOfMatchingBlackPixels__(self , AMat , LMat):
        matches = 0
        row = 0
        col = 0
        for r in LMat:
            for c in r:
                if c == 0 and c == AMat[row][col]:
                    matches += 1
                col += 1
            col = 0
            row += 1
        return matches
    
    def __getNumberOfTotalBlackPixels__(self , LMat):
        matches = 0
        for r in LMat:
            for c in r:
                if c == 0:
                    matches += 1
        return matches
    
    def __getPercentageOfMatch__(self , AMat , LMat):
        return ((self.__getNumberOfMatchingBlackPixels__(AMat , LMat) /self.__getNumberOfTotalBlackPixels__(LMat)) * 100)
