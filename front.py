import joblib

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication,QComboBox, QDialog,QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QMainWindow




# class BertApp(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         # Set up the GUI
#         self.setWindowTitle('BERT Application')
#         self.setGeometry(300, 400, 700, 400)
#
#         self.setStyleSheet("background-color: rgb(167, 213, 250); border : 2px solid white")
#         # Set up the GUI elements
#         self.input_field = QLineEdit()
#         self.input_ratio = QLineEdit()
#         self.input_sum = QLineEdit()
#         self.result_label = QLabel()
#         self.run_button = QPushButton('Run', self)
#
#         # Connect the "Run" button to the run_model method
#         self.run_button.clicked.connect(self.run_model)
#
#         # Add the GUI elements to a layout
#         input_layout = QHBoxLayout()
#         input_layout.addWidget(QLabel('Input Text:'))
#         input_layout.addWidget(self.input_field)
#         input_layout.setSizeConstraint(QHBoxLayout.SetFixedSize)
#
#
#         input_numSentence = QHBoxLayout()
#         input_numSentence.addWidget(QLabel('Input number of sentences:'))
#         input_numSentence.addWidget(self.input_sum)
#
#         input_ratio = QHBoxLayout()
#         input_ratio.addWidget(QLabel('Input ratio:'))
#         input_ratio.addWidget(self.input_ratio)
#
#
#         result_layout = QHBoxLayout()
#         result_layout.addWidget(QLabel('Result:'))
#         result_layout.addWidget(self.result_label)
#
#         button_layout = QHBoxLayout()
#         button_layout.addStretch(1)
#         button_layout.addWidget(self.run_button)
#
#         main_layout = QVBoxLayout()
#         main_layout.addLayout(input_layout)
#         main_layout.addLayout(input_numSentence)
#         main_layout.addLayout(input_ratio)
#         main_layout.addLayout(result_layout)
#         main_layout.addLayout(button_layout)
#
#
#         self.setLayout(main_layout)
class OptionDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle('Choose Option')
        self.setGeometry(400, 400, 400, 100)

        self.option_combobox = QComboBox()
        self.option_combobox.addItems(['Number of Sentences', 'Ratio'])
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Choose an Option:'))
        layout.addWidget(self.option_combobox)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_option(self):
        return self.option_combobox.currentIndex()

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle('Enter Input Text')
        self.setGeometry(400, 400, 400, 100)

        self.input_field = QLineEdit()
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Input Text:'))
        layout.addWidget(self.input_field)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_input_text(self):
        return self.input_field.text()

class InputNum(QDialog):
    def __init__(self, input_field_text):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle('Enter Input number')
        self.setGeometry(400, 400, 400, 100)

        self.input_field = QLineEdit()
        # self.ok_button = QPushButton('OK')
        # self.ok_button.clicked.connect(self.accept)
        self.run_button = QPushButton('Run', self)
        # self.input_button = QPushButton('Enter Input', self)

        # Connect the "Run" button to the run_model method
        self.run_button.clicked.connect(self.run_model)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        # button_layout.addWidget(self.input_button)
        button_layout.addWidget(self.run_button)
        layout = QHBoxLayout()
        layout.addWidget(QLabel('Input number:'))
        layout.addWidget(self.input_field)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def get_input_text(self):
        return self.input_field.text()

    def run_model(self):

        # Get the input data from the GUI
        input_data = input_field_text

        # ratio = self.input_ratio
        sum = self.input_field.text()
        ratio= ''
        print("self.input_field", sum)

        if ratio == '' or ratio is None:
            temp = sum
        else:
            temp = ratio

        # Send the input data to the Flask server
        if temp == ratio:
            data = {'text': input_data, 'ratio': ratio}
            response = requests.post(SERVER_URL+'/summarize/ratio', data=data)
        else:
            data = {'text': input_data, 'number': sum}
            response = requests.post(SERVER_URL + '/summarize/number', data=data)
        # print("response", response)

        # Process the response from the Flask server
        self.result = response.json()

        self.summary_with_newlines = str(self.result).replace('. ', '.\n')
        self.close()
        bert_app = BertApp(self.summary_with_newlines)
        bert_app.show()
        # summary_with_newlines = "\n".join([sentence["summary_text"] for sentence in str(result)])
        # self.result_label.setText(summary_with_newlines)
    def get_result_text(self):
        return self.summary_with_newlines


class BertApp(QWidget):
    def __init__(self, summary_with_newlines):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle('BERT Application')
        self.setGeometry(300, 400, 700, 400)

        self.setStyleSheet("background-color: rgb(167, 213, 250); border : 2px solid white")
        # Set up the GUI elements
        # self.input_field = QLineEdit()
        # Set up the GUI elements
        # self.input_text = input_text
        # self.num_sentences = num_sentences
        # self.ratio = ratio

        # print(num_sentences)
        # self.input_ratio = QLineEdit()
        # self.input_sum = QLineEdit()
        self.result_label = QLabel()
        # self.run_button = QPushButton('Run', self)
        # # self.input_button = QPushButton('Enter Input', self)
        #
        # # Connect the "Run" button to the run_model method
        # self.run_button.clicked.connect(self.run_model)

        # Connect the "Enter Input" button to the show_input_dialog method
        # self.input_button.clicked.connect(self.show_input_dialog)

        # Add the GUI elements to a layout
        # input_layout = QHBoxLayout()
        # # input_layout.addWidget(QLabel('Input Text:'))
        # input_layout.addWidget(self.input_field)
        # input_layout.setSizeConstraint(QHBoxLayout.SetFixedSize)

        # input_numSentence = QHBoxLayout()
        # input_numSentence.addWidget(QLabel('Input number of sentences:'))
        # input_numSentence.addWidget(self.input_sum)
        #
        # input_ratio = QHBoxLayout()
        # input_ratio.addWidget(QLabel('Input ratio:'))
        # input_ratio.addWidget(self.input_ratio)

        result_layout = QHBoxLayout()
        result_layout.addWidget(QLabel('Result:'))
        result_layout.addWidget(self.result_label)



        main_layout = QVBoxLayout()
        # main_layout.addLayout(input_layout)
        # main_layout.addLayout(input_numSentence)
        # main_layout.addLayout(input_ratio)
        main_layout.addLayout(result_layout)
        # main_layout.addLayout(button_layout)
        self.result_label.setText(summary_with_newlines)

        self.setLayout(main_layout)

    # def show_input_dialog(self):
    #     input_dialog = InputDialog(self)
    #     if input_dialog.exec_() == QDialog.Accepted:
    #         self.input_field.setText(input_dialog.input_field.text())



    # def run_model(self):
    #
    #     # Get the input data from the GUI
    #     input_data = self.input_field
    #     ratio = self.input_ratio
    #     sum = self.input_sum
    #     print(sum)
    #
    #     if ratio == '' or ratio is None:
    #         temp = sum
    #     else:
    #         temp = ratio
    #
    #     # Send the input data to the Flask server
    #     if temp == ratio:
    #         data = {'text': input_data, 'ratio': ratio}
    #         response = requests.post(SERVER_URL+'/summarize/ratio', data=data)
    #     else:
    #         data = {'text': input_data, 'number': sum}
    #         response = requests.post(SERVER_URL + '/summarize/number', data=data)
    #     # print("response", response)
    #
    #     # Process the response from the Flask server
    #     result = response.json()
    #
    #     summary_with_newlines = str(result).replace('. ', '.\n')
    #
    #     # summary_with_newlines = "\n".join([sentence["summary_text"] for sentence in str(result)])
    #     self.result_label.setText(summary_with_newlines)

if __name__ == '__main__':
    # Set up the Flask server URL
    SERVER_URL = 'http://localhost:1313'

    # Set up the BERT model
    MODEL_FILE = 'finalized_model.sav'
    model = joblib.load(MODEL_FILE)

    # Set up the GUI
    app = QApplication([])
    # Create an instance of the input dialog and get the input
    input_dialog = InputDialog()
    if input_dialog.exec_() == QDialog.Accepted:
        input_field_text = input_dialog.get_input_text()
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
        num_sentences_dialog = InputNum(input_field_text)
        if num_sentences_dialog.exec_() == QDialog.Accepted:
            num_sentences = num_sentences_dialog.get_input_text()
            result_field_text = num_sentences_dialog.get_result_text()

        else:
            # Handle the case where the user cancels the option dialog
            num_sentences = None
            ratio = None
            result_field_text = None
            option_index = -1



        # ratio_dialog = InputDialog()
        # if ratio_dialog.exec_() == QDialog.Accepted:
        #     ratio = ratio_dialog.get_input_text()
        # else:
        #     # Handle the case where the user cancels the option dialog
        #     ratio = None
        #     num_sentences =None
        #     option_index = -1
        ratio = ''

    # Create an instance of the BertApp with the input field from the input dialog



    app.exec_()
    # input_dialog = InputDialog()
    # input_field_text = input_dialog.input_field.text()
    # # print("input_field", input_field_text)
    #
    # # Create an instance of the BertApp with the input field from the input dialog
    # if input_dialog.exec_() == QDialog.Accepted:
    #     bert_app = BertApp(input_field_text)
    #     bert_app.show()
    #     app.exec_()
