import traceback
import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtGui, uic
import os
import ctypes

class Settings(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi('GUI\settings.ui', self)
        self.loadSettings()
        self.TxtBaseFolder.returnPressed.connect(self.SetBF)
        self.TxtBaseFolder.setText(self.BASE_FOLDER)
        self.TxtToken.returnPressed.connect(self.SetT)
        self.TxtToken.setText(self.FILE_TOKEN)
        self.TxtFolderName.returnPressed.connect(self.SetFN)
        self.TxtFolderName.setText(self.FOLDER_NAME)
        self.setWindowIcon(QtGui.QIcon('GUI\sicon.png'))
        self.show()

    def loadSettings(self):
        with open('settings') as f:
            settings = f.read().splitlines()
            for s in settings:
                s.replace('\n', '')
                setattr(self, s.split('=')[0], s.split('=')[1])

    def SetBF(self):
        self.BASE_FOLDER = self.TxtBaseFolder.text()
        self.saveSettings()

    def SetT(self):
        self.FILE_TOKEN = self.TxtToken.text()
        self.saveSettings()

    def SetFN(self):
        self.FOLDER_NAME = self.TxtFolderName.text()
        self.saveSettings()

    def saveSettings(self):
        with open('settings', 'w') as f:
            f.writelines([
                'BASE_FOLDER=' + self.BASE_FOLDER,
                '\nFILE_TOKEN=' + self.FILE_TOKEN,
                '\nFOLDER_NAME=' + self.FOLDER_NAME
            ])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    A = Settings()
    A.setGeometry(250, 300, 500, 150)
    sys.exit(app.exec_())
