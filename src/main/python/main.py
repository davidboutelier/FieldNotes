from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow,QDialog,QFileDialog
from PyQt5.uic import loadUi
import datetime
import os
import pytz
import sys



class Note(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):  
        loadUi(main_ui, self)  

        self.actionNew.triggered.connect(self.make_new_note)
        self.add_entry_pushButton.clicked.connect(self.add_new_entry)

        self.actionchange_settings.triggered.connect(self.change_settings)


    def change_settings(self):
        setting_dialog = SettingsDialog()
        setting_dialog.setWindowTitle('Settings for FieldNotes')
        setting_dialog.destination_folder_edit.setText(proj_dict['home'])
        setting_dialog.exec_()

    def make_new_note(self):
        global proj_dict

        # using now() to get current time
        current_time = datetime.datetime.now()
        this_year = current_time.year
        this_month = current_time.month
        this_day = current_time.day

        index = 1
        this_note_name = str(this_day)+'-'+str(this_month)+'-'+str(this_year)+'-note-'+str(index)+'.txt'
        while os.path.exists(os.path.join(proj_dict['home'], this_note_name)) == True:
            index += 1
            this_note_name = str(this_day)+'-'+str(this_month)+'-'+str(this_year)+'-note-'+str(index)+'.txt'
        
        print('new note: '+this_note_name)
        proj_dict['this_note_name'] = os.path.join(proj_dict['home'], this_note_name) #this_note_name

        current_local_time = datetime.datetime.now()

        UTC_time = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None)

        with open(proj_dict['this_note_name'], 'w') as f:
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
        global proj_dict

        current_local_time = datetime.datetime.now()
        UTC_time = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None)

        with open(proj_dict['this_note_name'], 'a') as f:
        
            line = 'Local time: '+str(current_local_time)
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = 'User: '+self.user_comboBox.currentText()
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            line = ' '
            self.textBrowser.append("<span>"+line+"</span>")
            f.write(line+"\n")

            if self.weather_checkBox.isChecked() == True:
                weather = self.weather_comboBox.currentText()
                self.textBrowser.append("<span>Weather: "+weather+"</span>")
                f.write('Weather: '+weather+"\n")

            if self.env_checkBox.isChecked() == True:
                env = self.env_comboBox.currentText()
                self.textBrowser.append("<span>Environment: "+env+"</span>")
                f.write('Environment: '+env+"\n")

            if self.equip_checkBox.isChecked() == True:
                equip = self.equip_comboBox.currentText()
                self.textBrowser.append("<span>Equipment:"+equip+"</span>")
                f.write('Equipment: '+equip+"\n")

            if self.other_checkBox.isChecked() == True: 
                message = self.entry_plainTextEdit.toPlainText()

                self.textBrowser.append("<span>Additional observations:</span>")
                f.write("Additional observations:\n")
            
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


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        loadUi(settings_ui, self)

        self.buttonBox.accepted.connect(self.accept)
        self.select_dest_pushButton.clicked.connect(self.select_destination_folder)

    def select_destination_folder(self):
        destination_folder = QFileDialog.getExistingDirectory(self, "Select directory",proj_dict['home'])  
        self.destination_folder_edit.setText(destination_folder)

    def accept(self):
        global proj_dict 
        proj_dict['home'] = self.destination_folder_edit.text() 
        self.close()  


if __name__ == '__main__':
    app_name = 'FieldNotes'
    version = '0.1.0'

    proj_dict = {}
    proj_dict['home'] = os.path.expanduser("~") # Default home folder- 

    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    main_ui = appctxt.get_resource('note.ui')
    settings_ui = appctxt.get_resource('settings_FieldNotes.ui')
    window = Note()
    window.setWindowTitle(app_name+' '+version)
    window.setContentsMargins(11, 11, 11, 11)
    window.show()
    exit_code = appctxt.app.exec()      # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)