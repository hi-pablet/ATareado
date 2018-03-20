import xml.etree.ElementTree as ET
from atcmds import commandsList
from atcmds import ATcommand
import os


#class ScriptsReader(object):

#   def __init__(self):
#       self.scriptsList = []

scriptsList = {}


def loadAllScripts(path):
    filenames = []

    for file in os.listdir(path):
        if file.endswith(".xml"):
            filenames.append(file.replace('.xml',''))

    if len(filenames):
        for file in filenames:
            try:
                script = []
                tree = ET.parse(path+file+'.xml').getroot()
                for elem in tree:
                    #commandsList
                    if elem.tag == "cmd":
                        if elem.attrib['id'] in commandsList:
                            cmd = ATcommand(elem.attrib['id'],
                                            (elem.attrib['setMode'] == '1'),
                                            elem.attrib['params'].split('|'))
                            script.append(cmd)
                            #print "CMD %s, %u, %s" % (cmd.cmd, cmd.setOperation, elem.attrib['params'])
                        else:
                            print "Invalid AT command read %s" % elem.attrib['id']
                    # print "param %s = %s" % (elem.attrib['name'], elem.text)
                scriptsList[file] = script
            except ET.ParseError:
                print "Error parsing XML"

    return filenames
