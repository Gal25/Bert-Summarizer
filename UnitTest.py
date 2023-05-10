import unittest
import sys
from PyQt5.QtWidgets import QApplication
from front import OptionDialog, InputDialog, InputNum, BertApp

app = QApplication(sys.argv)

class TestApp(unittest.TestCase):
    def test_option_dialog(self):
        dialog = OptionDialog()
        dialog.option_combobox.setCurrentIndex(0)
        self.assertEqual(dialog.get_option(), 0)

        dialog.option_combobox.setCurrentIndex(1)
        self.assertEqual(dialog.get_option(), 1)

    def test_input_dialog(self):
        dialog = InputDialog()
        dialog.file_path = 'test.txt'
        self.assertEqual(dialog.file_path, 'test.txt')
        dialog.input_field.setText('Test input')
        self.assertEqual(dialog.input_field.text(), 'Test input')

    def test_input_num_dialog(self):
        dialog = InputNum('Test input', 'ratio')
        dialog.input_field.setText('5')
        self.assertEqual(dialog.get_input_text(), '5')

    def test_bert_app(self):
        app = BertApp('Test summary')
        self.assertEqual(app.result_label.text(), 'Test summary')

    def test_export_result(self):
        app = BertApp('Test summary')
        app.export_result()  # Simulate clicking the export button
        # Perform assertion to check if the result is exported successfully

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
        app = BertApp('')
        self.assertEqual(app.result_label.text(), '')

if __name__ == '__main__':
    unittest.main()