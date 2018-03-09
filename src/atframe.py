#!/usr/bin/python

import form


class ATFrame(form.MainFrame):

    #Define
    connectCallback = None

    def __init__(self, parent):
        form.MainFrame.__init__(self, parent)

    def conn_button_onclick(self, event):
        self.log_text.AppendText('Conn %d %s '% self.port_combo.GetValue(), self.m_comboBox2.GetValue())
        connectCallback(self.port_combo.GetValue(), self.m_comboBox2.GetValue)

    def info_button_onclick(self, event):
        self.log_text.AppendText("Connected")

    def status_button_onclick(self, event):
        pass

    def writeToLogPannel(self, text):
        self.log_text.AppendText(text)

    def setConnectionStatus(self, status):
        if status:
            self.m_staticText1.SetLabel("Connected")
        else:
            self.__mainForm.SetLabel("Disconnected")

    def setAvailablePorts(self, ports):
        self.port_combo.Clear()
        self.port_combo.AppendItems(ports)
