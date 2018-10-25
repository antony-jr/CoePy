import argparse

ParserInformation = {
        'epilog' : 'Example: coepy -regno 210514665432 -dob 12-06-2001',
        'arguments' : {
            '--register-number' : {
                'short' : '-regno',
                'type' : str,
                'help' : 'Register number of the student you want to check marks.'
            },
            '--date-of-birth': {
                'short' : '-dob',
                'type' : str,
                'help' : 'Date of birth of the student you want to check marks.'
            }
        },
        'actionArguments': {
            '--assessment-mark' : {
                'short' : '-am' ,
                'help' : 'Returns the assessment mark with respect to the student.'
            },
            '--no-headless' : {
                'short' : '-nh',
                'help' : 'Disable headless mode , i.e Show the entire browser when processing.'
            },
            '--verbose' : {
                'short' : '-v',
                'help' : 'Activate Verbose mode.'
            },
            '--quick-browse' : {
                'short' : '-qb',
                'help' : 'Simply Logs you in the COE WEBSITE in a blink , substains the state in a browser!'
            }
        }
}

class CoePyArgumentParser(object):

    _mParser = None
    _mProcessed = None

    def __init__(self):
        self._mParser = argparse.ArgumentParser(epilog = ParserInformation['epilog'])
        Args = ParserInformation['arguments']
        for e in Args:
            self._mParser.add_argument(e, Args[e]['short'],type=Args[e]['type'],help=Args[e]['help'])
        ActionArgs = ParserInformation['actionArguments']
        for e in ActionArgs:
            self._mParser.add_argument(e , ActionArgs[e]['short'] , action='count' , help=ActionArgs[e]['help'])
        self._mProcessed = vars(self._mParser.parse_args())

    def printHelp(self):
        return self._mParser.print_help()

    def isEmpty(self):
        ret = True
        for e in self._mProcessed:
            if self._mProcessed[e] != None:
                ret = False
                break
        return ret

    def getValue(self , key):
        ret = None
        try:
            ret = self._mProcessed[str(key)]
        except:
            ret = None
        return ret
