import sys,subprocess,os,os.path,datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from HEXAgui import Ui_MainWindow,Ui_aboutgui
from HEXAtesting import ToolTesting

cwd=os.getcwd()

class checkCasesThread(QtCore.QThread):
    signalUpdate = QtCore.pyqtSignal(int,str)
    signalFinish = QtCore.pyqtSignal()
    def __init__(self, test_Input, test_Answer):
        QtCore.QThread.__init__(self)
        self.test_Input=test_Input
        self.test_Answer=test_Answer
    def __del__(self):
        self.wait()
    def concat(self, inlist):
        outstring = ""
        for i in inlist:
            outstring = outstring + " " + i
        return outstring
    def check_case(self, case_Index, test_Input, test_Answer):
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            test_Out = subprocess.run(test_Input, timeout=3, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         startupinfo=si)
            if test_Out.stderr.decode("utf-8")=="":
                test_Output = test_Out.stdout.decode("utf-8")
            else:
                test_Output = "Dump Stack Error"
        except subprocess.TimeoutExpired:
            test_Output = "Timeout Expired"
        except:
            test_Output = "Unexpected Error!"
        test_Input = self.concat(test_Input[1:])
        if (test_Output == test_Answer) or (test_Output == (test_Answer + " ")):
            return [1,("""Case {}: Passed\nInput: {}\nExpected Output:  {}\nGenerated Output: {}""".format(case_Index + 1, test_Input, test_Answer, test_Output))]
        elif ((test_Output == (test_Answer + " \n")) or (test_Output == (test_Answer + "\n"))):
            return [2,("""Case {}: Warning\nInput: {}\nExpected Output:  {}\nGenerated Output: {}""".format(case_Index + 1, test_Input, test_Answer, test_Output))]
        else:
            return [3,("""Case {}: Failed\nInput: {}\nExpected Output:  {}\nGenerated Output: {}""".format(case_Index + 1, test_Input, test_Answer, test_Output))]
    def run(self):
        for l in range(len(self.test_Input)):
            res = self.check_case(l, self.test_Input[l], self.test_Answer[l])
            self.signalUpdate.emit(res[0],res[1])
            self.sleep(0.1)
        self.signalFinish.emit()

class MyFirstGuiProgram(Ui_MainWindow):
    def __init__(self, dialog):
        super(MyFirstGuiProgram, self).__init__()
        self.setupUi(dialog)
        self.toolobject=ToolTesting()
        self.fileButton.clicked.connect(self.showDialog)
        self.updateButton.clicked.connect(self.updateCases)
        self.startButton.clicked.connect(self.startCheck)
        self.pushButton.clicked.connect(self.startCheck)
        self.actionClear_Result.triggered.connect(self.clearResult)
        self.actionSave_Result.triggered.connect(self.saveResult)
        self.actionQuit.triggered.connect(self.closeApplication)
        self.actionDelete_Cases.triggered.connect(self.deleteFiles)
        self.actionAbout.triggered.connect(self.aboutShow)
        self.updateCombo(self.searchOffline())
        self.get_thread = None

    def startCheck(self):
        currentfile=self.fileEdit.text()
        currentcase=self.casesBox.currentText()
        if currentcase=="Select Test Case:":
            self.statusBar.showMessage("Please Select Test Case First!", 3000)
        elif (not currentfile.endswith(".exe")) or (not os.path.isfile(currentfile)):
            self.statusBar.showMessage("Please Select Correct EXE File First!", 3000)
        elif currentcase!="Select Test Case:" and currentfile.endswith(".exe"):
            self.statusBar.showMessage("Start Testing...", 2000)
            self.clearResult()
            self.tabWidget.setCurrentIndex(1)
            self.begin_Test(currentcase+".hexa", currentfile)
        else:
            self.statusBar.showMessage("Unexpected Error!", 2000)

    def showDialog(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Select File', cwd,"Executable File (*.exe)")
        if fname[0]:
            self.fileEdit.setText(fname[0])

    def updateCases(self):
        self.statusBar.showMessage("Downloading Online Files...", 5000)
        downloadstatus=self.toolobject.download_Other_Files()
        self.statusBar.clearMessage()
        self.statusBar.showMessage(downloadstatus, 3000)
        self.updateCombo(self.searchOffline())

    def updateCombo(self, inputData=[]):
        self.casesBox.clear()
        comboData=['Select Test Case:']
        for i in inputData:
            comboData.append(i[:i.rfind('.hexa')])
        self.casesBox.addItems(comboData)

    def searchOffline(self):
        path = cwd
        text_files = [f for f in os.listdir(path) if f.endswith('.hexa')]
        return text_files

    def begin_Test(self, CaseFile, FilePath):
        test_Cases = self.toolobject.open_Offline_Cases(CaseFile)
        # Get Input and Modle Answers
        test_Input, test_Answer = self.toolobject.split_Data(FilePath, test_Cases)
        self.casesnumber=len(test_Input)
        self.currentcasesnumber=0
        self.get_thread = checkCasesThread(test_Input, test_Answer)
        self.get_thread.signalUpdate.connect(self.add_result)
        self.get_thread.signalFinish.connect(self.done)
        self.get_thread.start()
        self.startButton.setEnabled(False)
        self.pushButton.setEnabled(False)

    #Result Add
    def add_result(self, status,post_text):
        self.currentcasesnumber += 1
        self.progressBar.setValue((self.currentcasesnumber/self.casesnumber)*100)
        if status==1:
            self.lcdNumber.display(self.lcdNumber.value()+1)
            self.resultEdit.setTextColor(QtGui.QColor(54, 209, 0))
        elif status==2:
            self.lcdNumber_2.display(self.lcdNumber_2.value() + 1)
            self.resultEdit.setTextColor(QtGui.QColor(242, 185, 6))
            post_text=post_text.rstrip('\n')+"+newline"
        elif status==3:
            self.lcdNumber_3.display(self.lcdNumber_3.value() + 1)
            self.resultEdit.setTextColor(QtGui.QColor(220, 0, 0))
            post_text = post_text.rstrip('\n')
        self.resultEdit.append(post_text)
        self.resultEdit.setTextColor(QtGui.QColor("black"))
        self.resultEdit.append("===========================================")

    def done(self):
        self.progressBar.setValue(100)
        self.statusBar.clearMessage()
        self.statusBar.showMessage("Test Finished", 2000)
        self.startButton.setEnabled(True)
        self.pushButton.setEnabled(True)

    def saveResult(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(None, 'Select File', cwd, "Text File (*.txt)")
        if fname[0]:
            Filetosave=fname[0]
            current_contents=self.resultEdit.toPlainText()
            File_to_Save = open(Filetosave, 'w+')
            File_to_Save.write("Generated by:\nHEXA-A Test Tool\n"+str(datetime.datetime.now()).split('.')[0]+"\n"+"===========================================\n")
            File_to_Save.write(current_contents)
            File_to_Save.close()
            self.statusBar.showMessage("Logfile Saved Successfully", 2000)

    def clearResult(self):
        if self.get_thread and self.get_thread.isRunning():
            self.get_thread.terminate()
            self.statusBar.showMessage("Test Terminated", 2000)
            self.startButton.setEnabled(True)
            self.pushButton.setEnabled(True)
        else:
            self.progressBar.setValue(0)
            self.lcdNumber.display(0)
            self.lcdNumber_2.display(0)
            self.lcdNumber_3.display(0)
            self.resultEdit.clear()
            self.statusBar.clearMessage()

    def deleteFiles(self):
        result = QtWidgets.QMessageBox.warning(None, 'Warning!', "All offline files will be deleted!", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            hexafiles = self.searchOffline()
            for i in hexafiles:
                os.remove(cwd +'/'+ i)
            self.updateCombo(self.searchOffline())
        else:
            pass

    def aboutShow(self):
        self.aboutgui = QtWidgets.QDialog()
        self.about=Ui_aboutgui()
        self.about.setupUi(self.aboutgui)
        self.aboutgui.show()

    def closeApplication(self):
        sys.exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    prog = MyFirstGuiProgram(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
