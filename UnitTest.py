import unittest
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QDialog
from app_frontend import OptionDialog, InputDialog, InputNum, BertApp
import os
from unittest.mock import patch

app = QApplication(sys.argv)

class TestApp(unittest.TestCase):
    def test_option_dialog(self):
        dialog = OptionDialog()
        dialog.option_combobox.setCurrentIndex(0)
        self.assertEqual(dialog.get_option(), 0)

        dialog.option_combobox.setCurrentIndex(1)
        self.assertEqual(dialog.get_option(), 1)

        dialog.option_combobox.setCurrentIndex(5) #invalid input
        self.assertEqual(dialog.get_option(), -1)

    def test_input_dialog(self):
        dialog = InputDialog()
        dialog.file_path = 'test.txt'
        self.assertEqual(dialog.file_path, 'test.txt')
        dialog.input_field.setText('Test input')
        self.assertEqual(dialog.input_field.text(), 'Test input')
        dialog.input_field.setText('Gal and Lior are the best')
        self.assertEqual(dialog.input_field.text(), 'Gal and Lior are the best')
        dialog.input_field.setText('bert summery')
        self.assertEqual(dialog.input_field.text(), 'bert summery')
        dialog.input_field.setText('welcome to our project')
        self.assertEqual(dialog.input_field.text(), 'welcome to our project')

        dialog.input_field.setText('')
        with patch.object(QMessageBox, 'exec_', return_value=QMessageBox.Ok):
            dialog.ok_button.click()
        self.assertEqual(dialog.result(), QDialog.Rejected)

        app.quit()

    def test_input_num_dialog(self):
        dialog = InputNum('Test input', 'ratio')
        dialog.input_field.setText('0.2')
        self.assertEqual(dialog.get_input_text(), '0.2')

        dialog1 = InputNum('Test input', 'num')
        dialog1.input_field.setText('7')
        self.assertEqual(dialog1.get_input_text(), '7')

        dialog2 = InputNum('Test input', 'num')
        dialog2.input_field.setText('10')
        self.assertEqual(dialog2.get_input_text(), '10')

        dialog3 = InputNum('Test input', 'ratio')
        dialog3.input_field.setText('0.6')
        self.assertEqual(dialog3.get_input_text(), '0.6')


    def test_bert_app(self):
        app = BertApp('Test summary', 'Test input text')
        self.assertEqual(app.result_label.text(), 'Test summary')

        app = BertApp('hello , this is our final project , enjoy!' , 'Test input text')
        self.assertEqual(app.result_label.text(), 'hello , this is our final project , enjoy!')

    def test_export_result(self):
        app = BertApp('Test summary' , 'Test input text')
        temp_file_path = 'test_export.txt'
        app.export_result()

        # Check if the file is created and contains the expected content
        self.assertTrue(os.path.isfile(temp_file_path))
        with open(temp_file_path, 'r') as file:
            exported_content = file.read()
        self.assertEqual(exported_content, app.result_label.text())
        # Clean up the temporary file
        os.remove(temp_file_path)

    def test_invalid_input_dialog(self):
        dialog = InputDialog()
        dialog.file_path = None
        self.assertIsNone(dialog.file_path)
        dialog.input_field.setText('')
        self.assertEqual(dialog.input_field.text(), '')

    def test_invalid_input_num_dialog(self):
        dialog = InputNum('Test input', 'ratio')
        dialog.input_field.setText('')
        self.assertEqual(dialog.get_input_text(), '')

    def test_empty_bert_app(self):
        app = BertApp('', '')
        self.assertEqual(app.result_label.text(), '')

if __name__ == '__main__':
    unittest.main()
