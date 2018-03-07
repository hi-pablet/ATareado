#!/usr/bin/python

import form


class ATFrame(form.MainFrame):

    def __init__(self, parent):
        form.MainFrame.__init__(self, parent)

    def conn_button_onclick(self, event):
        self.log_text.AppendText("Connected")

    def writeToLogPannel(self, text):
        self.log_text.AppendText(text)