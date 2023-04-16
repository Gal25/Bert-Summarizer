import joblib

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QMainWindow


# model = joblib.load('finalized_model.sav')

def convert_text_to_features(text_list, max_seq_length=1024):
    """
    Convert a list of text strings to a list of feature dictionaries
    suitable for input to a BERT model.

    Args:
        text_list (list): A list of text strings to convert.
        max_seq_length (int): The maximum sequence length for the BERT model.
            Defaults to 128.

    Returns:
        list: A list of feature dictionaries, where each dictionary contains
        'input_ids', 'input_mask', and 'segment_ids' keys representing the
        tokenized input data in a format suitable for input to a BERT model.
    """

    # Load the BERT tokenizer
    # bert_module = joblib.load('finalized_model.sav')
    bert_module = hub.load("https://tfhub.dev/google/bert_uncased_L-12_H-768_A-12/2")
    vocab_file = bert_module.vocab_file.asset_path.numpy()
    do_lower_case = bert_module.do_lower_case.numpy()
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(open(vocab_file, 'rb').read())

    # Convert the input text to BERT tokens
    tokens = []
    input_masks = []
    segment_ids = []
    for text in text_list:
        tokenized_text = tokenizer.tokenize(text)
        tokenized_text = ["[CLS]"] + tokenized_text + ["[SEP]"]
        input_ids = tokenizer.convert_tokens_to_ids(tokenized_text)
        padding_length = max_seq_length - len(input_ids)
        input_ids = input_ids + [0] * padding_length
        input_mask = [1] * len(input_ids)
        segment_id = [0] * len(input_ids)

        tokens.append(input_ids)
        input_masks.append(input_mask)
        segment_ids.append(segment_id)

    # Convert the BERT tokens to feature dictionaries
    features = []
    for i in range(len(tokens)):
        feature_dict = {
            "input_ids": np.asarray(tokens[i], dtype=np.int32),
            "input_mask": np.asarray(input_masks[i], dtype=np.int32),
            "segment_ids": np.asarray(segment_ids[i], dtype=np.int32),
        }
        features.append(feature_dict)

    return features
# QWidget

class BertApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle('BERT Application')
        self.setGeometry(300, 400, 700, 400)

        self.setStyleSheet("background-color: rgb(167, 213, 250); border : 2px solid white")
        # image_path = r'C:\Users\galco\PycharmProjects\finalproject\view.jpg'
        # pixmap = QPixmap(image_path)
        # self.setPixmap(pixmap)
        # self.setFixedSize(pixmap.width(), pixmap.height())
        # label = QLabel(self)
        # pixmap = QPixmap('image.jpg')
        # label.setPixmap(pixmap)
        # label.setScaledContents(True)
        # self.setCentralWidget(label)


        # Set up the GUI elements
        self.input_field = QLineEdit()
        self.input_ratio = QLineEdit()
        self.input_sum = QLineEdit()
        self.result_label = QLabel()
        self.run_button = QPushButton('Run', self)

        # Connect the "Run" button to the run_model method
        self.run_button.clicked.connect(self.run_model)

        # Add the GUI elements to a layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel('Input Text:'))
        input_layout.addWidget(self.input_field)
        input_layout.setSizeConstraint(QHBoxLayout.SetFixedSize)


        input_numSentence = QHBoxLayout()
        input_numSentence.addWidget(QLabel('Input number of sentences:'))
        input_numSentence.addWidget(self.input_sum)

        input_ratio = QHBoxLayout()
        input_ratio.addWidget(QLabel('Input ratio:'))
        input_ratio.addWidget(self.input_ratio)


        result_layout = QHBoxLayout()
        result_layout.addWidget(QLabel('Result:'))
        result_layout.addWidget(self.result_label)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.run_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(input_numSentence)
        main_layout.addLayout(input_ratio)
        main_layout.addLayout(result_layout)
        main_layout.addLayout(button_layout)


        self.setLayout(main_layout)

    def run_model(self):

        # Get the input data from the GUI
        input_data = self.input_field.text()
        ratio = self.input_ratio.text()
        sum = self.input_sum.text()

        print("133")

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
        result = response.json()
        # result =  requests.get('http://127.0.0.1:1313')
        # Load the BERT model from the .sav file
        # model = joblib.load('finalized_model.sav')
        # Prepare the input data for the BERT model
        # input_data = [input_data]
        # ratio = [ratio]
        # sum = [sum]

        # Convert the input data into a format that can be processed by the BERT model
        # input_text = convert_text_to_features(input_data)
        # input_ratio = convert_text_to_features(ratio)
        # input_sum = convert_text_to_features(sum)

        # Pass the input data through the BERT model
        # output = model.predict(input_text)
        # result = model(input_data, sum)
        # summary = "".join(result)
        # # print(summary)

        # Display the results on the GUI
        # self.result_label.setText("test")
        summary_with_newlines = str(result).replace('. ', '.\n')

        # summary_with_newlines = "\n".join([sentence["summary_text"] for sentence in str(result)])
        self.result_label.setText(summary_with_newlines)

if __name__ == '__main__':
    # Set up the Flask server URL
    SERVER_URL = 'http://localhost:1313'

    # Set up the BERT model
    MODEL_FILE = 'finalized_model.sav'
    model = joblib.load(MODEL_FILE)

    # Set up the GUI
    app = QApplication([])
    bert_app = BertApp()
    bert_app.show()
    app.exec_()
