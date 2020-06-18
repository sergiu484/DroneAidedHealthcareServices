import ParteaOP
import wx
import os
import wx.grid
import time
import sys
print(sys.version)


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
                                      size=(wx.DisplaySize()[0]//1.1, wx.DisplaySize()[1]//1.1))
        p = self
        p.currentDirectory = os.getcwd()
        p.SetBackgroundColour('#ADD8E6')
        self.Centre()
        p.box = wx.BoxSizer(wx.VERTICAL)
        p.image = wx.BoxSizer(wx.HORIZONTAL)
        p.jos = wx.BoxSizer(wx.VERTICAL)
        p.search = wx.BoxSizer(wx.HORIZONTAL)
        p.but = wx.BoxSizer(wx.HORIZONTAL)

        p.midP = wx.Panel(p)
        p.valori = wx.Panel(p)
        p.midP.SetBackgroundColour('#ADD8E6')
        p.valori.SetBackgroundColour('#ADD8E6')
        p.midP.box = wx.BoxSizer(wx.HORIZONTAL)
        p.valori.box = wx.BoxSizer(wx.VERTICAL)
        p.valori.centre = wx.BoxSizer(wx.HORIZONTAL)
        p.valori.droneB = wx.BoxSizer(wx.HORIZONTAL)
        p.valori.droneS = wx.BoxSizer(wx.HORIZONTAL)

        p.box.Add(p.image, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        p.image.Add(p.midP, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        p.image.Add(p.valori, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=20)

        p.box.Add(p.jos, flag=wx.ALIGN_CENTER |
                  wx.EXPAND | wx.BOTTOM, border=20)

        p.jos.Add(p.search, flag=wx.EXPAND | wx.RIGHT | wx.LEFT)
        p.jos.Add(p.but, flag=wx.ALIGN_CENTER | wx.TOP, border=20)
        p.tc = wx.TextCtrl(p)
        p.bt1 = wx.Button(p, label='Search', size=(70, 25))
        p.bt2 = wx.Button(p, label='OK', size=(70, 25))
        p.bt4 = wx.Button(p, label='Close', size=(70, 25))
        p.bt3 = wx.Button(p, label='Liniar Redundant ', size=(110, 25))
        p.bt5 = wx.Button(p, label='Liniar ', size=(70, 25))
        p.bt6 = wx.Button(p, label='Euristic', size=(70, 25))
        p.bt7 = wx.Button(p, label='Euristic redundant', size=(110, 25))
        p.search.Add(p.tc, proportion=1, flag=wx.LEFT |
                     wx.RIGHT | wx.ALIGN_CENTER, border=20)
        p.search.Add(p.bt1, flag=wx.RIGHT, border=20)

        p.but.Add(p.bt2, flag=wx.RIGHT, border=20)
        p.but.Add(p.bt5, flag=wx.RIGHT, border=20)
        p.but.Add(p.bt3, flag=wx.RIGHT, border=20)
        p.but.Add(p.bt6, flag=wx.RIGHT, border=20)
        p.but.Add(p.bt7, flag=wx.RIGHT, border=20)
        p.but.Add(p.bt4, flag=wx.RIGHT, border=20)
        p.bt1.Bind(wx.EVT_BUTTON, p.SaveFile)
        p.bt2.Bind(wx.EVT_BUTTON, self.OP)
        p.bt3.Bind(wx.EVT_BUTTON, self.DeleteRedundant)
        p.bt5.Bind(wx.EVT_BUTTON, self.CuRedundante)
        p.bt6.Bind(wx.EVT_BUTTON, self.Euristic)
        p.bt7.Bind(wx.EVT_BUTTON, self.EuristicFaraRedundante)
        p.bt4.Bind(wx.EVT_BUTTON, self.Close)
        p.SetSizer(p.box)
        p.midP.SetSizer(p.midP.box)
        p.valori.SetSizer(p.valori.box)

    def Close(self, event):
        self.Destroy()

    def Euristic(self, event):
        if 'imgd' in vars(self.midP):
            self.midP.imgd.Destroy()
            vars(self.midP).pop('imgd')

        if 'grid' in vars(self):
            self.grid.Destroy()
            vars(self).pop('grid')

        self.midP.imgd = wx.Image('./Euristic.png', wx.BITMAP_TYPE_ANY)
        self.d = self.midP.imgd.GetSize()
        self.p = self.midP.GetSize()

        if self.d[0] > self.p[0]:
            self.midP.png = self.midP.imgd.Scale(
                self.p[0] - 10 * self.p[0] // 100, self.d[1], wx.IMAGE_QUALITY_HIGH)
            self.d = self.midP.imgd.GetSize()
        if self.d[1] > self.p[1]:
            self.midP.imgd = self.midP.imgd.Scale(
                self.d[0], self.p[1], wx.IMAGE_QUALITY_HIGH)
        self.d = self.midP.imgd.GetSize()

        self.midP.imgd = wx.StaticBitmap(
            self.midP, -1, wx.BitmapFromImage(self.midP.imgd))
        self.midP.box.Add(self.midP.imgd, wx.ID_ANY,
                          wx.EXPAND | wx.ALL | wx.ALIGN_LEFT, 20)
        self.midP.Refresh()
        self.Layout()

        self.grid = wx.grid.Grid(self.midP, -1)
        ParteaOP.Tabel(self.grid, self.DateTabel2, self.PretCentru2, self.TipDroneCentru2, self.DistantaTotala2,
                       self.NrDroneMici2, self.NrDroneMari2, self.PretTotal2, self.IdPuncte2, self.nrPacienti2, self.timp2)
        self.midP.box.Add(self.grid, wx.ID_ANY, wx.ALIGN_CENTRE, 20)
        self.midP.Refresh()
        self.Layout()

    def EuristicFaraRedundante(self, event):
        if 'imgd' in vars(self.midP):
            self.midP.imgd.Destroy()
            vars(self.midP).pop('imgd')
        if 'grid' in vars(self):
            self.grid.Destroy()
            vars(self).pop('grid')

        self.midP.imgd = wx.Image('./Euristic2.png', wx.BITMAP_TYPE_ANY)
        self.d = self.midP.imgd.GetSize()
        self.p = self.midP.GetSize()

        if self.d[0] > self.p[0]:
            self.midP.png = self.midP.imgd.Scale(
                self.p[0] - 10 * self.p[0] // 100, self.d[1], wx.IMAGE_QUALITY_HIGH)
            self.d = self.midP.imgd.GetSize()
        if self.d[1] > self.p[1]:
            self.midP.imgd = self.midP.imgd.Scale(
                self.d[0], self.p[1], wx.IMAGE_QUALITY_HIGH)
        self.d = self.midP.imgd.GetSize()

        self.midP.imgd = wx.StaticBitmap(
            self.midP, -1, wx.BitmapFromImage(self.midP.imgd))
        self.midP.box.Add(self.midP.imgd, wx.ID_ANY,
                          wx.EXPAND | wx.ALL | wx.ALIGN_LEFT, 20)
        self.midP.Refresh()
        self.Layout()

        self.grid = wx.grid.Grid(self.midP, -1)
        ParteaOP.Tabel(self.grid, self.DateTabel2, self.PretCentru2, self.TipDroneCentru2, self.DistantaTotala2,
                       self.NrDroneMici2, self.NrDroneMari2, self.PretTotal2, self.IdPuncte2, self.nrPacienti2, self.timp2)
        self.midP.box.Add(self.grid, wx.ID_ANY, wx.ALIGN_CENTRE, 20)
        self.midP.Refresh()
        self.Layout()

    def CuRedundante(self, event):
        if 'imgd' in vars(self.midP):
            self.midP.imgd.Destroy()
            vars(self.midP).pop('imgd')

        if 'grid' in vars(self):
            self.grid.Destroy()
            vars(self).pop('grid')

        self.midP.imgd = wx.Image('./desen.png', wx.BITMAP_TYPE_ANY)
        self.d = self.midP.imgd.GetSize()
        self.p = self.midP.GetSize()

        if self.d[0] > self.p[0]:
            self.midP.png = self.midP.imgd.Scale(
                self.p[0] - 10 * self.p[0] // 100, self.d[1], wx.IMAGE_QUALITY_HIGH)
            self.d = self.midP.imgd.GetSize()
        if self.d[1] > self.p[1]:
            self.midP.imgd = self.midP.imgd.Scale(
                self.d[0], self.p[1], wx.IMAGE_QUALITY_HIGH)
        self.d = self.midP.imgd.GetSize()

        self.midP.imgd = wx.StaticBitmap(
            self.midP, -1, wx.BitmapFromImage(self.midP.imgd))
        self.midP.box.Add(self.midP.imgd, wx.ID_ANY,
                          wx.EXPAND | wx.ALL | wx.ALIGN_LEFT, 20)
        self.midP.Refresh()
        self.Layout()

        self.grid = wx.grid.Grid(self.midP, -1)
        ParteaOP.Tabel(self.grid, self.DateTabel, self.PretCentru, self.TipDroneCentru, self.DistantaTotala,
                       self.NrDroneMici, self.NrDroneMari, self.PretTotal, self.IdPuncte, self.nrPacienti, self.timp1)
        self.midP.box.Add(self.grid, wx.ID_ANY, wx.ALIGN_CENTRE, 20)
        self.midP.Refresh()
        self.Layout()

    def DeleteRedundant(self, event):
        if 'imgd' in vars(self.midP):
            self.midP.imgd.Destroy()
            vars(self.midP).pop('imgd')

        if 'grid' in vars(self):
            self.grid.Destroy()
            vars(self).pop('grid')

        self.midP.imgd = wx.Image('./desen2.png', wx.BITMAP_TYPE_ANY)
        self.d = self.midP.imgd.GetSize()
        self.p = self.midP.GetSize()

        if self.d[0] > self.p[0]:
            self.midP.png = self.midP.imgd.Scale(
                self.p[0] - 10 * self.p[0] // 100, self.d[1], wx.IMAGE_QUALITY_HIGH)
            self.d = self.midP.imgd.GetSize()
        if self.d[1] > self.p[1]:
            self.midP.imgd = self.midP.imgd.Scale(
                self.d[0], self.p[1], wx.IMAGE_QUALITY_HIGH)
        self.d = self.midP.imgd.GetSize()

        self.midP.imgd = wx.StaticBitmap(
            self.midP, -1, wx.BitmapFromImage(self.midP.imgd))
        self.midP.box.Add(self.midP.imgd, wx.ID_ANY,
                          wx.EXPAND | wx.ALL | wx.ALIGN_LEFT, 20)
        self.midP.Refresh()
        self.Layout()

        self.grid = wx.grid.Grid(self.midP, -1)
        ParteaOP.Tabel(self.grid, self.DateTabel, self.PretCentru, self.TipDroneCentru, self.DistantaTotala,
                       self.NrDroneMici, self.NrDroneMari, self.PretTotal, self.IdPuncte, self.nrPacienti, self.timp1)
        self.midP.box.Add(self.grid, wx.ID_ANY, wx.ALIGN_CENTRE, 20)
        self.midP.Refresh()
        self.Layout()

    def SaveFile(self, event):
        dlg = wx.FileDialog(self, message="Save file as ...",
                            defaultDir=self.currentDirectory, defaultFile="", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.tc.SetValue(path)

    def OP(self, event):
        if len(self.tc.GetValue()) == 0 or self.tc.GetValue()[-3::] != 'txt':
            wx.MessageBox("You need to select a txt file",
                          "Mesaj!", wx.OK | wx.ICON_INFORMATION)
        else:
            I, R, Raza, k, Pk, costLow, costBig = ParteaOP.citire(
                self.tc.GetValue())
            start = time.time()
            Pi, Di, self.DateTabel, self.PretCentru, self.TipDroneCentru, self.DistantaTotala, self.NrDroneMici, self.NrDroneMari, self.PretTotal, self.IdPuncte, self.nrPacienti = ParteaOP.OP(
                I, R, Raza, k, Pk, costLow, costBig)
            end = time.time()
            self.timp1 = end - start
            start = time.time()
            self.DateTabel2, self.PretCentru2, self.TipDroneCentru2, self.DistantaTotala2, self.NrDroneMici2, self.NrDroneMari2, self.PretTotal2, self.IdPuncte2, self.nrPacienti2 = ParteaOP.Euristic(
                I, R, Raza, k, Pk, costLow, costBig, Pi, Di)
            end = time.time()
            self.timp2 = end - start
            if 'imgd' in vars(self.midP):
                self.midP.imgd.Destroy()
                vars(self.midP).pop('imgd')

            self.midP.imgd = wx.Image('./Euristic.png', wx.BITMAP_TYPE_ANY)
            self.d = self.midP.imgd.GetSize()
            self.p = self.midP.GetSize()

            if self.d[0] > self.p[0]:
                self.midP.png = self.midP.imgd.Scale(
                    self.p[0] - 10*self.p[0]//100, self.d[1], wx.IMAGE_QUALITY_HIGH)
                self.d = self.midP.imgd.GetSize()
            if self.d[1] > self.p[1]:
                self.midP.imgd = self.midP.imgd.Scale(
                    self.d[0], self.p[1], wx.IMAGE_QUALITY_HIGH)
            self.d = self.midP.imgd.GetSize()

            self.midP.imgd = wx.StaticBitmap(
                self.midP, -1, wx.BitmapFromImage(self.midP.imgd))
            self.midP.box.Add(self.midP.imgd, wx.ID_ANY,
                              wx.EXPAND | wx.ALL, 20)
            self.midP.Refresh()
            self.Layout()
            if 'grid' in vars(self):
                self.grid.Destroy()
                vars(self).pop('grid')

            self.grid = wx.grid.Grid(self.midP, -1)
            ParteaOP.Tabel(self.grid, self.DateTabel2, self.PretCentru2, self.TipDroneCentru2, self.DistantaTotala2,
                           self.NrDroneMici2, self.NrDroneMari2, self.PretTotal2, self.IdPuncte2, self.nrPacienti2, self.timp2)
            self.midP.box.Add(self.grid, wx.ID_ANY, wx.ALIGN_CENTRE, 20)
            self.midP.Refresh()
            self.Layout()


def main():
    app = wx.App()
    ex = Example(None, title='Drones')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
