import traceback
import sys
from Loader import Loader
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtGui, uic
from shutil import copy
import os
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
PDFJS = 'file:///pdfjs-1.9.426-dist/web/viewer.html'
PDF = 'file:///Benvenuto.pdf'


class SearchDialog(QtWidgets.QDialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = uic.loadUi('GUI\SearchDialog.ui', self)

class ErrorDialog(QtWidgets.QDialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = uic.loadUi('GUI\ErrorListDialog.ui', self)

class Appli(QtWidgets.QMainWindow):
    pdfViewer1 = None
    pdfViewer2 = None
    ControlPanel = None
    completerList = []
    FIRST = True

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi('GUI\mainwindow.ui', self)
        self.loadSettings()
        self.pdfViewer1 = Window()
        self.pdfViewer2 = Window()
        self.Web1.addWidget(self.pdfViewer1)
        self.Web2.addWidget(self.pdfViewer2)
        self.BaseFolder.setText(self.BASE_FOLDER)
        self.BaseFolder.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BtnLoad.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BtnNext.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BtnPrevious.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BtnLoad.clicked.connect(self.openFileNameDialog)
        self.BtnNext.clicked.connect(self.NextPDF)
        self.BtnPrevious.clicked.connect(self.PrevPDF)
        self.setWindowIcon(QtGui.QIcon('GUI\icon.jpg'))
        self.show()
        self.setFocus()
        self.CmbList.currentIndexChanged.connect(self.Update)
        self.automa = False
        self.TxtSearch.returnPressed.connect(self.SearchFun)
        self.BtnErrorList.clicked.connect(self.showError)

    def showError(self):
        dialog = ErrorDialog()
        dialog.LstDoc.addItems(Loader.ErrorListDoc)
        dialog.LstLayout.addItems(Loader.ErrorListFile)
        r = dialog.exec_()

    def setSearchList(self):
        self.SearchList = [x.split('\\')[-1].split('.')[0].replace(self.FILE_TOKEN + " ", "") for x in Loader.LayoutFileList]
        self.completer = QtWidgets.QCompleter(self.SearchList)
        self.TxtSearch.setCompleter(self.completer)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

    def Update(self):
        if not self.automa:
            Loader.current = self.CmbList.currentIndex()
            copy(Loader.LayoutFileList[Loader.current], 'Temp/List.pdf')
            self.pdfViewer2.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, 'file:///Temp/List.pdf')))
            self.setFocus()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Left or e.key() == QtCore.Qt.Key_Down:
            self.PrevPDF()
        if e.key() == QtCore.Qt.Key_Right or e.key() == QtCore.Qt.Key_Up:
            self.NextPDF()
        if e.text() == 'l':
            self.openFileNameDialog()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.PrevPDF()
        else:
            self.NextPDF()
            self.NextPDF()

    def mouseReleaseEvent(self, QMouseEvent):
        self.setFocus()

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                            self.BASE_FOLDER,
                                                            "All Files (*);;PDF Files (*.pdf)", options=options)
        if fileName:
            try:
                a = fileName.split('/')[-1].split('.')[0]
                self.LblMain.setText(a)
                copy(fileName, 'Temp/Main.pdf')
                self.pdfViewer1.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, 'file:///Temp/Main.pdf')))
            except Exception as e:
                print(str(e))
        self.setFocus()

    def NextPDF(self):
        Loader.current = Loader.current + 1
        if Loader.current >= len(Loader.LayoutFileList):
            Loader.current = 0
        copy(Loader.LayoutFileList[Loader.current], 'Temp/List.pdf')
        self.pdfViewer2.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, 'file:///Temp/List.pdf')))
        self.setFocus()
        self.automa = True
        self.CmbList.setCurrentIndex(Loader.current)
        self.automa = False

    def PrevPDF(self):
        Loader.current = Loader.current - 1
        if Loader.current < 0:
            Loader.current = len(Loader.LayoutFileList) - 1
        copy(Loader.LayoutFileList[Loader.current], 'Temp/List.pdf')
        self.pdfViewer2.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, 'file:///Temp/List.pdf')))
        self.setFocus()
        self.automa = True
        self.CmbList.setCurrentIndex(Loader.current)
        self.automa = False

    def ModifyBase(self):
        options = QtWidgets.QFileDialog.Options()
        try:
            fileName, _ = QtWidgets.QFileDialog.getExistingDirectory(self, "QFileDialog.getOpenFileName()",
                                                                     self.BASE_FOLDER,
                                                                     " ", options=options)
            if fileName:
                Loader.LoadFiles(fileName)
        except Exception as e:
            print(e.with_traceback())
        self.setFocus()

    def loadSettings(self):
        with open('settings') as f:
            settings = f.read().splitlines()
            for s in settings:
                s.replace('\n', '')
                setattr(self, s.split('=')[0], s.split('=')[1])

    def setComboBox(self):
        self.automa = True
        for a in Loader.LayoutFileList:
            self.CmbList.addItem(a.split('\\')[-1].split('.')[0])
        self.automa = False

    def showdialog(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Error Loading File List")
        msg.setInformativeText("Please check settings file")
        msg.setWindowTitle("Critical Error")
        msg.setDetailedText(self.BASE_FOLDER + ' leads to an empty file list, please insert a correct base folder')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        self.close()

    def SearchFun(self):
        while True:
            dialog = SearchDialog()
            l = [x for x in self.SearchList if self.TxtSearch.text().upper() in x.upper()]
            dialog.LstResult.addItems(l)
            print(len(l))
            if len(l) == 0:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("No layout Found")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
                return
            elif len(l) == 1:
                try:
                    dialog.LstResult.setCurrentRow(0)
                    r = 1
                except Exception as e:
                    r = 0
                    print(str(e))
            else:
                r = dialog.exec_()
            if dialog.LstResult.selectedItems() or r != 1:
                break
        if r == 1:
            try:
                ind = self.SearchList.index(dialog.LstResult.currentItem().text())
                if self.FIRST:
                    self.FIRST = False
                    self.automa = True
                    self.CmbList.setCurrentIndex(ind+1)
                    self.automa = False
                self.CmbList.setCurrentIndex(ind)
                self.TxtSearch.setText("")
            except Exception as e:
                print(str(e))

class Window(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super(Window, self).__init__()
        self.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (PDFJS, PDF)))


if __name__ == '__main__':
    pdfH = screensize[1] - 100
    pdfW = screensize[0] - 10
    app = QtWidgets.QApplication(sys.argv)
    A = Appli()
    if Loader.current == -1:
        try:
            os.remove('Temp/Main.pdf')
            os.remove('Temp/List.pdf')
        except:
            pass
        Loader.LoadFiles(Loader, basedir=A.BASE_FOLDER, file_token=A.FILE_TOKEN, folder_name=A.FOLDER_NAME, verbose= False)
        if len(Loader.LayoutFileList) < 1:
            A.showdialog()
        A.setComboBox()
        A.setSearchList()
    A.setGeometry(1, 30, pdfW, pdfH)
    sys.exit(app.exec_())