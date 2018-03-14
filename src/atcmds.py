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

# Command List [id, command, params, return]
commandsList = {AT_CMD_ID:     ['AT', '', 'OK'],
                ATI_CMD_ID:    ['ATI', '', '(.*)OK'],
                CPIN_CMD_ID:   ['AT+CPIN', '', '+CPIN:(.+)OK'],
                CSQ_CMD_ID:    ['AT+CSQ', '', '+CSQ:(\d+)'],
                CGATT_CMD_ID:  ['AT+CGATT', '', '+CGATT:(\d+)OK'],
                CIPMUX_CMD_ID: ['AT+CIPMUX', '', '+CIPMUX'],
                CIPMODE_CMD_ID:['AT+CIPMODE', '"%val1%,%val2%,%val3%"', 'OK'],
                CSTT_CMD_ID:   ['AT+CSTT', '"%val1%,%val2%,%val3%"', 'OK'],
                CIICR_CMD_ID:  ['AT+CIICR', '', 'OK'],
                CIFSR_CMD_ID:  ['AT+CIFSR', '', '(.*)'],
                CIPSTART_CMD_ID: ['AT+CIPSTART', '"%val1","%val2","%val3"', 'OK'],  # "[TCP/UDP]", "<ip_dest>", "<port>"
                CIPSEND_CMD_ID:['AT+CIPSEND', '', '>'],
                CIPCLOSE_CMD_ID: ['AT+CIPCLOSE', '', 'OK'],
                CIPCCFG_CMD_ID:['AT+CIPCCFG', '', 'OK']}


class ATcommand(object):

    # cmdId: string with command Id
    # setMode: boolean true>set false>query
    # params: list of strings
    def __init__(self, cmdId, setMode, params):
        self.cmd = cmdId
        self.setOperation = setMode
        self.params = params
        try:
            self.paramString = commandsList[self.cmd][1]
            self.answer = ''
            self.respError = False
            if self.paramString.find('%val1%') != -1 and 0 in params:
                self.paramString = self.paramString.replace('%val1%', params[0])
            if self.paramString.find('%val2%') != -1 and 1 in params:
                self.paramString = self.paramString.replace('%val2%', params[1])
            if self.paramString.find('%val3%') != -1 and 2 in params:
                self.paramString = self.paramString.replace('%val3%', params[2])
        except:
            print "Exception creating command"

    def getSetString(self):
        return commandsList[self.cmd][0] + self.paramString + "\r\n"

    def getQueryString(self):
        return commandsList[self.cmd][0] + "?\r\n"

    def parseResponse(self, response):
        print "[%s] search %s " % (response, commandsList[self.cmd][2])
        res = (False, response)
        try:
            searchObj = re.search(commandsList[self.cmd][2], (response.replace('\n', '')).replace('\r', ''), re.S | re.M)
            if searchObj:
                pprint(searchObj.groups())
                #print "Searched ans : ", searchObj.group(1)
                res = (True, searchObj.groups())

        except Exception as e:
            print >> sys.stdout, "Exception parse response, %s" % e

        return res
