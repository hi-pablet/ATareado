import re
import sys
from pprint import pprint

AT_CMD_ID       = 'AT'       # Check connection
ATI_CMD_ID      = 'ATI'      # Get modem Info
CPIN_CMD_ID     = 'CPIN'     # PIN needed
CSQ_CMD_ID      = 'CSQ'      # Signal Quality
CGATT_CMD_ID    = 'CGATT'    #
CIPMUX_CMD_ID   = 'CIPMUX'
CIPMODE_CMD_ID  = 'CIPMODE'
CSTT_CMD_ID     = 'CSTT'
CIICR_CMD_ID    = 'CIICR'
CIFSR_CMD_ID    = 'CIFSR'
CIPSTART_CMD_ID = 'CIPSTART'
CIPSEND_CMD_ID  = 'CIPSEND'
CIPCLOSE_CMD_ID = 'CIPCLOSE'
CIPCCFG_CMD_ID  = 'CIPCCFG'

# Command List [id, command, params tx, rx params parse, description]
# Description:
# id: AT command id
# command: command string
# params: string containing the parameters required by the command
# rx params parse string: this string will be used to parse the response using regexp
# description: description of the command
# Todo define class for this
commandsList = {AT_CMD_ID:      ['AT', '', '', 'Alive'],
                ATI_CMD_ID:     ['ATI', '', '(.*)OK', 'Device name'],
                CPIN_CMD_ID:    ['AT+CPIN', '', '\+CPIN:(.*)OK', 'Enter CPIN'],
                CSQ_CMD_ID:     ['AT+CSQ', '', '\+CSQ:(.*)OK', 'Signal Quality'],
                CGATT_CMD_ID:   ['AT+CGATT', '', '\+CGATT:(.*)OK', 'Attach GPRS Service'],
                CIPMUX_CMD_ID:  ['AT+CIPMUX', '', '\+CIPMUX(.*)OK', 'Start MultiIP Connection'],
                CIPMODE_CMD_ID: ['AT+CIPMODE', '"%val1%,%val2%,%val3%"', '', 'Select TCPIP mode'],
                CSTT_CMD_ID:    ['AT+CSTT', '"%val1%,%val2%,%val3%"', '', 'Set APN, usr, pwd'],
                CIICR_CMD_ID:   ['AT+CIICR', '', 'OK', 'Bring up GPRS'],
                CIFSR_CMD_ID:   ['AT+CIFSR', '', '(.*)OK', 'Get Local IP'],
                CIPSTART_CMD_ID:['AT+CIPSTART', '"%val1","%val2","%val3"', '', 'Start TCP/UDP conn'],  # "[TCP/UDP]", "<ip_dest>", "<port>"
                CIPSEND_CMD_ID: ['AT+CIPSEND', '', '>', 'Send data through IP'],
                CIPCLOSE_CMD_ID:['AT+CIPCLOSE', '', '', 'Close TCP/UDP connection'],
                CIPCCFG_CMD_ID: ['AT+CIPCCFG', '', '', 'Configure transparent mode']}

class ATresponse(object):

    def __init__(self,okRes = False, cmdId = '', paramsRx=[]):
        self.ok = okRes
        self.cmdId = cmdId
        self.params = paramsRx
        self.error = ''

class ATcommand(object):

    # cmdId: string with command Id
    # setMode: boolean true>set false>query
    # params: list of strings
    def __init__(self, cmdId, setMode, params):
        self.cmd = cmdId
        self.setOperation = setMode
        self.params = params
        self.sentString = ''
        try:
            self.paramString = commandsList[self.cmd][1]
            self.answer = ''
            if self.paramString != '':
                if self.paramString.find('%val1%') != -1 and 0 in params:
                    self.paramString = self.paramString.replace('%val1%', params[0])
                if self.paramString.find('%val2%') != -1 and 1 in params:
                    self.paramString = self.paramString.replace('%val2%', params[1])
                if self.paramString.find('%val3%') != -1 and 2 in params:
                    self.paramString = self.paramString.replace('%val3%', params[2])
        except:
            print "Exception creating command"

    def getString(self):
        self.sentString = commandsList[self.cmd][0]
        if self.setOperation:
            if self.paramString != '':
                self.sentString += "=" + self.paramString
        else:
            self.sentString += "?"
        self.sentString += "\r\n"
        return self.sentString

    def parseResponse(self, resStr):
        print "[%s] search %s " % (resStr, commandsList[self.cmd][2])
        res = None
        try:
            if resStr.find('ERROR') != -1:
                res = ATresponse(True, self.cmd, [resStr])
            if resStr.find('OK') != -1:
                resStr = resStr.replace(self.sentString, '')
                #Capture values?
                if commandsList[self.cmd][2] != '':
                    searchObj = re.search(commandsList[self.cmd][2], (resStr.replace('\n', '')).replace('\r', ''), re.S | re.M)
                    if searchObj:
                        pprint(searchObj.groups())
                        #print "Searched ans : ", searchObj.group(1)
                        res = ATresponse(True, self.cmd, searchObj.groups())
                else:
                    res = ATresponse(True, self.cmd, resStr)

        except Exception as e:
            print >> sys.stdout, "Exception parse response, %s" % e

        return res
