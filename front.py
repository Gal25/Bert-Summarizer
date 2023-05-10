import joblib
import requests
from PyQt5.QtGui import QPixmap, QPainter, QPalette
from PyQt5.QtWidgets import QApplication,QFileDialog,QComboBox, QDialog,QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QMainWindow


class OptionDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle('Choose Option')
        self.setGeometry(400, 400, 400, 400)

        self.option_combobox = QComboBox()
        self.option_combobox.addItems(['Number of Sentences', 'Ratio'])
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)

        # # Apply stylesheet to make captions bold
        # self.option_combobox.setStyleSheet("font-weight: bold;")
        self.ok_button.setStyleSheet("font-weight: bold;")


        layout = QHBoxLayout()
        layout.addWidget(QLabel('Choose an Option:', styleSheet="font-weight: bold;"))
        layout.addWidget(self.option_combobox)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        # Set background image
        self.set_background_image('img2.jpg')  # Replace with the path to your image file


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

        # Set up the GUI
        self.setWindowTitle('Select File')
        self.setGeometry(400, 400, 400, 400)

        self.input_field = QLineEdit()
        self.file_path = None

        self.file_button = QPushButton('Browse')
        self.file_button.clicked.connect(self.browse_file)
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)

        # Apply stylesheet to make captions bold
        # self.file_button.setStyleSheet("font-weight: bold;")
        # self.ok_button.setStyleSheet("font-weight: bold;")

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Select File:', styleSheet="font-weight: bold;"))
        layout.addWidget(self.file_button)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        # Set background image
        self.set_background_image('img2.jpg')  # Replace with the path to your image file

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.setStyleSheet(f"background-image: url({image_path}); background-repeat: no-repeat;")
        else:
            print(f"Failed to set background image: {image_path}")

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File', '', 'All Files (*);;Text Files (*.txt)', options=options)
        if file_path:
            self.file_path = file_path
            with open(file_path, 'r') as file:
                self.input_field.setText(file.read())

class InputNum(QDialog):
    def __init__(self, input_field_text, temp):
        super().__init__()

        # Set up the GUI
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
        self.set_background_image('img2.jpg')  # Replace with the path to your image file

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.setStyleSheet(f"background-image: url({image_path}); background-repeat: no-repeat;")
        else:
            print(f"Failed to set background image: {image_path}")

    def get_input_text(self):
        return self.input_field.text()

    def run_model(self):

        # Get the input data from the GUI
        input_data = input_field_text
        input_num = self.input_field.text()


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

        self.close()
        bert_app = BertApp(self.summary3)
        bert_app.show()

    def get_result_text(self):
        return self.summary_with_newlines

class BertApp(QWidget):
    def __init__(self, summary_with_newlines):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle('BERT Application')
        self.setGeometry(300, 400, 400, 400)

        self.result_label = QLabel()
        # self.result_label.setStyleSheet("font-weight: bold;")

        self.export_button = QPushButton('Export', styleSheet="font-weight: bold;")
        self.export_button.clicked.connect(self.export_result)

        result_layout = QHBoxLayout()
        result_layout.addWidget(QLabel('Result:', styleSheet="font-weight: bold;"))
        result_layout.addWidget(self.result_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.export_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(result_layout)
        main_layout.addLayout(button_layout)

        self.result_label.setText(summary_with_newlines)

        self.setLayout(main_layout)
        # Set background image
        self.set_background_image('pic2.jpg')  # Replace with the path to your image file

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
            with open(file_path, 'w') as file:
                file.write(self.result_label.text())
            print(f"Result exported to file: {file_path}")

if __name__ == '__main__':
    # Set up the Flask server URL
    SERVER_URL = 'http://localhost:1313'

    # Set up the BERT model
    MODEL_FILE = 'finalized_model.sav'
    model = joblib.load(MODEL_FILE)

    # Set up the GUI
    app = QApplication([])
    temp = ''
    # Usage
    dialog = InputDialog()
    if dialog.exec_() == QDialog.Accepted:
        file_path = dialog.file_path
        if file_path:
            print(f"Selected file: {file_path}")
            # print(f"File contents: {dialog.input_field.text()}")
            input_field_text = dialog.input_field.text()
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
