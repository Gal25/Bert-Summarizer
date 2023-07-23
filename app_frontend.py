import sys

import joblib
import requests
from PyQt5.QtGui import QPixmap, QPainter, QPalette
from PyQt5.QtWidgets import QApplication, QFileDialog, QComboBox, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QPushButton, QMainWindow, QMessageBox, QTextEdit
import re
from PyQt5.QtGui import QIcon
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import traceback

data = ''
try:
    class OptionDialog(QDialog):
        def __init__(self):
            super().__init__()

            self.setWindowTitle('Choose Option')
            self.setGeometry(400, 400, 400, 400)
            icon = QIcon(r'C:\Users\galco\PycharmProjects\finalproject\image\BERT.png')
            self.setWindowIcon(icon)
            self.option_combobox = QComboBox()
            self.option_combobox.addItems(['Number of Sentences', 'Ratio'])
            self.ok_button = QPushButton('OK')
            self.ok_button.clicked.connect(self.accept)

            # # Apply stylesheet to make captions bold
            self.ok_button.setStyleSheet("font-weight: bold;")

            layout = QHBoxLayout()
            layout.addWidget(QLabel('Choose an Option:', styleSheet="font-weight: bold;"))
            layout.addWidget(self.option_combobox)
            layout.addWidget(self.ok_button)

            self.setLayout(layout)

            # Set background image
            self.set_background_image('image/view.jpg')  # Replace with the path to your image file


        def set_background_image(self, image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.setStyleSheet(f"background-image: url({image_path}); background-repeat: no-repeat;")
            else:
                print(f"Failed to set background image: {image_path}")

        def get_option(self):
            return self.option_combobox.currentIndex()

    class InputDialog(QDialog):
        def __init__(self):
            super().__init__()
            global data
            self.setWindowTitle('Select File')
            self.setGeometry(400, 400, 400, 400)

            self.input_field = QLineEdit()
            self.text_line = QLineEdit()
            self.url_line = QLineEdit()

            self.text_line.setFixedHeight(self.text_line.sizeHint().height())  # Adjust the initial height
            self.file_path = None

            self.file_button = QPushButton('Browse')
            self.file_button.clicked.connect(self.browse_file)
            self.ok_button = QPushButton('OK')
            self.ok_button.clicked.connect(self.on_ok_clicked)
            self.get_text_button = QPushButton('Get Text')
            self.get_text_button.clicked.connect(self.get_text_from_url)

            layout = QHBoxLayout()
            layout.addWidget(QLabel('Select File:', styleSheet="font-weight: bold;"))
            layout.addWidget(self.file_button)
            # layout.addWidget(self.ok_button)

            layout2 = QHBoxLayout()
            layout2.addWidget(QLabel('Insert Text:', styleSheet="font-weight: bold;"))
            layout2.addWidget(self.text_line)

            layout3 = QHBoxLayout()
            layout3.addWidget(QLabel('Insert URL:', styleSheet="font-weight: bold;"))
            layout3.addWidget(self.url_line)
            layout3.addWidget(self.get_text_button)


            main_layout = QVBoxLayout()
            main_layout.addLayout(layout)
            main_layout.addLayout(layout2)
            main_layout.addLayout(layout3)
            main_layout.addWidget(self.ok_button)
            self.setLayout(main_layout)
            icon = QIcon(r'C:\Users\galco\PycharmProjects\finalproject\image\BERT.png')
            self.setWindowIcon(icon)
            # Set background image
            self.set_background_image('image/view.jpg')  # Replace with the path to your image file

        def remove_hyperlinks(self,text):
            # Define regular expression pattern to match hyperlinks
            pattern = re.compile(r'<a href=.*?>(.*?)</a>')

            # Remove hyperlinks from text
            text = re.sub(pattern, r'\1', text)

            return text


        def get_text_from_url(self):
            url = self.url_line.text()
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Remove script and style tags
            for script in soup(["script", "style"]):
                script.extract()

            for title in soup.find_all('title'):
                title.decompose()

            text = soup.get_text()
            # Remove extra white space
            text = " ".join(text.split())

            text = self.remove_hyperlinks(text)
            self.text_line.setText(text)

        def set_background_image(self, image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.setStyleSheet(f"background-image: url({image_path}); background-repeat: no-repeat;")
            else:
                print(f"Failed to set background image: {image_path}")

        def on_ok_clicked(self):
            # Check if the input field is empty
            if not self.input_field.text() and not self.text_line.text():
                # Display an error message to the user
                error_box = QMessageBox()
                error_box.setWindowTitle('Error')
                error_box.setText('Input text can not be empty')
                error_box.setIcon(QMessageBox.Warning)
                error_box.exec_()
                return

            # If the input field is not empty, accept the dialog
            data = self.input_field.text()
            self.accept()

        def browse_file(self):
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, 'Select File', '', 'All Files (*);;Text Files (*.txt)', options=options)
            if file_path:
                self.file_path = file_path
                with open(file_path, mode='r', encoding='utf-8') as file:
                    self.input_field.setText(file.read())

        def get_text(self):
            return self.input_field.text()

    class InputNum(QDialog):
        def __init__(self, input_field_text, temp):
            super().__init__()

            self.setWindowTitle('Enter Input number')
            self.setGeometry(400, 400, 400, 400)
            self.temp = temp
            self.input_field = QLineEdit()

            self.run_button = QPushButton('Run', self)

            # Connect the "Run" button to the run_model method
            self.run_button.clicked.connect(self.run_model)
            self.run_button.setStyleSheet("font-weight: bold;")

            button_layout = QHBoxLayout()
            button_layout.addStretch(1)
            button_layout.addWidget(self.run_button)
            layout = QHBoxLayout()
            layout.addWidget(QLabel('Input number:', styleSheet="font-weight: bold;"))
            layout.addWidget(self.input_field)
            layout.addWidget(self.run_button)

            self.setLayout(layout)

            # Set background image
            self.set_background_image('image/view.jpg')  # Replace with the path to your image file
            icon = QIcon(r'C:\Users\galco\PycharmProjects\finalproject\image\BERT.png')
            self.setWindowIcon(icon)
        def set_background_image(self, image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.setStyleSheet(f"background-image: url({image_path}); background-repeat: no-repeat;")
            else:
                print(f"Failed to set background image: {image_path}")

        def get_input_text(self):

            return self.input_field.text()

        def run_model(self):


            input_data = input_field_text
            input_num = self.input_field.text()

            if not self.input_field.text() :
                # Display an error message to the user
                error_box = QMessageBox()
                error_box.setWindowTitle('Error')
                error_box.setText('Input number can not be empty')
                error_box.setIcon(QMessageBox.Warning)
                error_box.exec_()
                return

            # Send the input data to the Flask server
            if self.temp == "ratio":
                data = {'text': input_data, 'ratio': input_num}
                response = requests.post(SERVER_URL+'/summarize/ratio', data=data)
            else:
                data = {'text': input_data, 'number': input_num}
                response = requests.post(SERVER_URL + '/summarize/number', data=data)

            # Process the response from the Flask server
            self.result = response.json()
            self.summary_with_newlines = str(self.result).replace('. ', '.\n')
            self.summary_with_newlines2 = str(self.summary_with_newlines).replace('result:', '')
            self.summary1 = str(self.summary_with_newlines2).replace('}', '')
            self.summary2 = str(self.summary1).replace('{', '')
            self.summary3 = str(self.summary2).replace(':', '')
            self.summary4 = str(self.summary3).replace("'", '')

            # lines = self.summary3.splitlines()
            # new_text = '\n'.join(lines[1:])

            try:
                self.close()
                self.bert_app = BertApp(self.summary4, input_data)

                self.bert_app.show()
            except Exception as e:

                traceback.print_exc()


        def get_result_text(self):
            return self.summary_with_newlines

    class BertApp(QWidget):
        def __init__(self, summary_with_newlines,  input_data):
            super().__init__()
            self.setWindowTitle('BERT Application')
            self.setGeometry(300, 400, 400, 400)
            self.result_label = QLabel()

            self.data = input_data
            self.summary = summary_with_newlines
            # self.result_label.setStyleSheet("font-weight: bold;")

            icon = QIcon(r'C:\Users\galco\PycharmProjects\finalproject\image\BERT.png')
            self.setWindowIcon(icon)

            self.export_button = QPushButton('Export', styleSheet="font-weight: bold;")
            self.export_button.clicked.connect(self.export_result)
            self.extract_button = QPushButton('Extract Main Subject', styleSheet="font-weight: bold;")
            self.extract_button.clicked.connect(self.extract_keywords)
            self.send_email_button = QPushButton('Send Email', styleSheet="font-weight: bold;")
            self.send_email_button.clicked.connect(self.send_email)

            result_layout = QHBoxLayout()
            result_layout.addWidget(QLabel('Result:', styleSheet="font-weight: bold;"))
            result_layout.addWidget(self.result_label)

            button_layout = QHBoxLayout()
            button_layout.addWidget(self.export_button)

            button_layout2 = QHBoxLayout()
            button_layout2.addWidget(self.extract_button)

            button_layout3 = QHBoxLayout()
            button_layout3.addWidget(self.send_email_button)

            main_layout = QVBoxLayout()
            main_layout.addLayout(result_layout)
            main_layout.addLayout(button_layout)
            main_layout.addLayout(button_layout2)
            main_layout.addLayout(button_layout3)



            self.result_label.setText(summary_with_newlines)
            self.setLayout(main_layout)
            # Set background image
            self.set_background_image('image/blue.jpg')

        def set_background_image(self, image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.setStyleSheet(f"background-image: url({image_path}); background-repeat: no-repeat;")
            else:
                print(f"Failed to set background image: {image_path}")

        def export_result(self):
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, 'Export Result', '', 'Text Files (*.txt)', options=options)
            if file_path:
                with open(file_path, 'w', encoding='gbk') as file:
                    file.write(self.result_label.text())
                print(f"Result exported to file: {file_path}")

        def extract_keywords(self):
            input_data = self.data
            encoded_data = input_data.encode('utf-8')
            data = {'text': encoded_data}
            response = requests.post(SERVER_URL + '/keybert/', data=data)

            # Process the response from the Flask server
            self.result = response.json()
            self.result2 = str(self.result).replace('result:', '')
            self.result3 = str(self.result2).replace('}', '')
            self.result4 = str(self.result3).replace('{', '')
            self.result5 = str(self.result4).replace(':', '')
            self.result6 = str(self.result5).replace("'", '')

            # Display the main subject
            QMessageBox.information(self, "Main Subject", f"Main Subject: {self.result6}")


        def send_email(self):
            # Get user input for email details
            dialog = EmailDialog()
            if dialog.exec_() == QDialog.Accepted:
                recipient_email = dialog.recipient_email_text.text()
                subject = dialog.subject_text.text()
                newline = "\n"
                mes = self.summary + newline
                message = mes + dialog.message_text.toPlainText()
                data = {'subject': subject, 'message': message, 'recipient_email': recipient_email}
                response = requests.post(SERVER_URL + '/sendemail', data=data)
                self.result = response.json()
                QMessageBox.information(self, "send email", f"{self.result}")


    class EmailDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Email Details')

            self.recipient_email_label = QLabel('Recipient Email:')
            self.recipient_email_text = QLineEdit()

            self.subject_label = QLabel('Subject:')
            self.subject_text = QLineEdit()

            self.message_label = QLabel('Message:')
            self.message_text = QTextEdit()

            self.send_button = QPushButton('Send')
            self.send_button.clicked.connect(self.accept)

            layout = QVBoxLayout()
            layout.addWidget(self.recipient_email_label)
            layout.addWidget(self.recipient_email_text)
            layout.addWidget(self.subject_label)
            layout.addWidget(self.subject_text)
            layout.addWidget(self.message_label)
            layout.addWidget(self.message_text)

            button_layout = QHBoxLayout()
            button_layout.addWidget(self.send_button)

            layout.addLayout(button_layout)
            self.setLayout(layout)

            # Set background image
            self.set_background_image('image/view.jpg')

        def set_background_image(self, image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.setStyleSheet(f"background-image: url({image_path}); background-repeat: no-repeat;")
            else:
                print(f"Failed to set background image: {image_path}")

    if __name__ == '__main__':
        # Set up the Flask server URL
        SERVER_URL = 'http://localhost:1313'

        # # Set up the BERT model
        # MODEL_FILE = 'finalized_model.sav'
        # model = joblib.load(MODEL_FILE)

        # Set up the GUI
        app = QApplication([])
        temp = ''

        dialog = InputDialog()
        if dialog.exec_() == QDialog.Accepted:
            # print(f"File contents: {dialog.input_field.text()}")
            if not dialog.text_line.text() :
                print(2)
                file_path = dialog.file_path
                if file_path:
                    print(f"Selected file: {file_path}")
                    # input_field_text = dialog.input_field.text()
                    input_field_text = dialog.get_text()


            if not dialog.input_field.text():
                input_field_text = dialog.text_line.text()
            # if not dialog.input_field.text() and not dialog.text_line:
            #     input_field_text = dialog.text_line.text()
        else:
            # Handle the case where the user cancels the input dialog
            input_field_text = ''

        # Show the OptionDialog and get the chosen option
        option_dialog = OptionDialog()
        if option_dialog.exec_() == QDialog.Accepted:
            option_index = option_dialog.get_option()
        else:
            # Handle the case where the user cancels the option dialog
            option_index = -1
            num_sentences = None
            ratio= None

        # Depending on the chosen option, show the appropriate input dialog and get the input
        if option_index == 0:
            temp = "num"
            num_sentences_dialog = InputNum(input_field_text, temp)
            if num_sentences_dialog.exec_() == QDialog.Accepted:
                num_sentences = num_sentences_dialog.get_input_text()
                result_field_text = num_sentences_dialog.get_result_text()

            else:
                # Handle the case where the user cancels the option dialog
                num_sentences = None
                ratio = None
                result_field_text = None
                option_index = -1

        if option_index == 1:
            temp = "ratio"
            ratio_dialog = InputNum(input_field_text, temp)
            if ratio_dialog.exec_() == QDialog.Accepted:
                ratio = ratio_dialog.get_input_text()
            else:
                # Handle the case where the user cancels the option dialog
                ratio = None
                num_sentences =None
                option_index = -1
                result_field_text = None

        app.exec_()


except Exception as e:
    traceback.print_exc()
