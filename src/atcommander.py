#!/usr/bin/python

import wx
import atframe


if __name__ == "__main__":
    app = wx.App(False)

    frame = atframe.ATFrame(None)
    frame.Show()

    app.MainLoop()