from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import datetime
import os
import pytz
import time
import sys

shared_dict = {}

class Note(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):  
        loadUi(main_ui, self)  

        self.actionNew.triggered.connect(self.make_new_note)
        self.add_entry_pushButton.clicked.connect(self.add_new_entry)

    def make_new_note(self):
        global shared_dict

        # using now() to get current time
        current_time = datetime.datetime.now()
        this_year = current_time.year
        this_month = current_time.month
        this_day = current_time.day

        index = 1
        this_note_name = str(this_day)+'-'+str(this_month)+'-'+str(this_year)+'-note-'+str(index)+'.txt'
        while os.path.exists(this_note_name) == True:
            index += 1
            this_note_name = str(this_day)+'-'+str(this_month)+'-'+str(this_year)+'-note-'+str(index)+'.txt'
        
        print('new note: '+this_note_name)
        shared_dict['this_note_name'] = this_note_name

        current_local_time = datetime.datetime.now()

        UTC_time = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None)

        with open(this_note_name, 'w') as f:
            line = 'New note for '+str(this_day)+'-'+str(this_month)+'-'+str(this_year)
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = 'Note number '+str(index)
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = 'Local time: '+str(current_local_time)
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = 'UTC time: '+str(UTC_time)
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")


            line = 'User: '+self.user_comboBox.currentText()
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = ' '
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = '----------------------------------------------------------------'
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

        
    def add_new_entry(self):   
        global shared_dict

        current_local_time = datetime.datetime.now()
        UTC_time = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None)

        with open(shared_dict['this_note_name'], 'a') as f:
        
            line = 'Local time: '+str(current_local_time)
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = 'UTC time: '+str(UTC_time)
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = 'User: '+self.user_comboBox.currentText()
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = ' '
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            message = self.entry_plainTextEdit.toPlainText()
            
            for line in message.split('\n'):
                self.textBrowser.append("<span>"+line+"</span>")
                f.write(line+"\n")

            line = ' '
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = '----------------------------------------------------------------'
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            
        x = self.textBrowser.verticalScrollBar().maximum()
        self.textBrowser.verticalScrollBar().setValue(x)




if __name__ == '__main__':
    app_name = 'FieldNotes'
    version = '0.0.1'

    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    main_ui = appctxt.get_resource('note.ui')
    window = Note()
    window.setWindowTitle(app_name+' '+version)
    window.setContentsMargins(11, 11, 11, 11)
    window.show()
    exit_code = appctxt.app.exec()      # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)