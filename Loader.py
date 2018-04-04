import os
baseurl = ''
class Loader():
    LayoutFileList = []
    ErrorListDoc = []
    ErrorListFile = []
    current = -1

    def LoadFiles(self, basedir, file_token, folder_name, verbose=True):
        for i in os.listdir(basedir):
            try:
                if folder_name in os.listdir(basedir + '\\' + i):
                    found = False
                    for j in os.listdir(basedir + '\\' + i + "\\" + folder_name):
                        if j.startswith(file_token):
                            self.LayoutFileList.append(basedir + '\\' + i + "\\" + folder_name + "\\" + j)
                            found = True
                    if not found:
                        self.ErrorListFile.append(i)
                        if verbose:
                            print("MANCA FILE IN: {}".format(i))
                else:
                    self.ErrorListDoc.append(i)
                    if verbose:
                        print("MANCA CARTELLA IN: {}".format(i))
            except:
                continue
        self.current = 0
