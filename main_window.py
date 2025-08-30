from PyQt5.QtWidgets import ( QApplication, QMainWindow, QWidget, QPushButton, QLabel, QTextEdit,
QVBoxLayout, QHBoxLayout, QGroupBox, QInputDialog )
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import QDialog
from instrument_check import check_instruments
from select_test import SelectTestDialog
import sys
import os
import re
import json

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from temperature_dialog import TemperatureDialog
# from temperature_dialog_new import SelectTempDialog

from temp_file import set_selected_temperatures, get_selected_temperatures  ### give the test file name where temp variable is present as list
#from GROUP_1_OPT import temperature
class MainWindow(QMainWindow):
    # prompt_required = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.setGeometry(100, 100, 800, 550)
        self.setup_ui()
        self.setWindowTitle("SYNOPSYS GPIO")




    def setup_ui(self):
        main_layout = QVBoxLayout()

        # self.prompt_required.connect(self.show_input_prompt)
        # Header layout
        logo_and_text_layout = QVBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap("logo.png").scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignLeft)
        logo_and_text_layout.setSpacing(2)

        header_layout = QHBoxLayout()
        # header_layout.addWidget(QLabel(" TESSOLVE"), alignment=Qt.AlignLeft)
        logo_and_text_layout.addWidget(logo_label)
        header_layout.addLayout(logo_and_text_layout)

        header_label = QLabel("SYNOPSYS GPIO")
        header_label.setFont(QFont('Arial', 16, QFont.Bold))
        header_layout.addWidget(header_label, alignment=Qt.AlignCenter)

        logo_and_text_layout = QVBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap("logo2.png").scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignRight)
        logo_and_text_layout.setSpacing(2)

        logo_and_text_layout.addWidget(logo_label)
        header_layout.addLayout(logo_and_text_layout)

        # header_layout.addWidget(QLabel(" Synopsys"), alignment=Qt.AlignRight)
        main_layout.addLayout(header_layout)
        main_layout.setContentsMargins(1, 1, 1, 1)

        self.test_queue = []     # List of test scripts to run
        self.current_test_index = -1
        self.selected_test_script = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)


        # main_layout = QHBoxLayout()
        left_layout = QHBoxLayout()
        right_layout = QHBoxLayout()

        # label = QLabel("Synopsys GPIO ")
        # label.setAlignment(Qt.AlignLeft)
        # label.setFont(QFont("Arial", 10, QFont.Bold))
        # left_layout.addWidget(label)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5, 5, 5)  # smaller top margin
        left_layout.setSpacing(2)

        # left_layout.addWidget(label)
        # left_layout.addStretch()

        group_box = QGroupBox("Test Setup")
        # self.setFont(QFont("Courier", 10))
        # label.setFont(QFont("Arial", 15, QFont.Bold))
        self.setStyleSheet("background-color: light blue;")   # ( ##f5f5f5;)
        self.setStyleSheet("QGroupBox { margin: 10px; padding: 1px; }")
        box_layout = QHBoxLayout()
        left_layout.addWidget(group_box)

        btn_instr_check = QPushButton("Instrument Check")
        btn_instr_check.setStyleSheet("background-color: powder blue; font-weight: bold; font-size: 12px;")
        btn_instr_check.clicked.connect(self.run_instrument_check)
        box_layout.addWidget(btn_instr_check)

        btn_select_test = QPushButton("Select Tests")
        btn_select_test.setStyleSheet("background-color: powder blue; font-weight: bold; font-size: 12px;")
        btn_select_test.clicked.connect(self.open_test_selector)
        box_layout.addWidget(btn_select_test)

        btn_temp = QPushButton("Temperature")
        btn_temp.setStyleSheet("background-color: powder blue; font-weight: bold; font-size: 12px;")
        btn_temp.clicked.connect(self.show_temp_dialog)
        box_layout.addWidget(btn_temp)


        btn_run = QPushButton("Run")
        btn_run.setStyleSheet("background-color: powder blue; font-weight: bold; font-size: 12px;")
        btn_run.clicked.connect(self.run_test_script)
        box_layout.addWidget(btn_run)

        # box_layout.addWidget(QPushButton("Abort"))
        btn_abort = QPushButton("Abort")
        btn_abort.setStyleSheet("background-color: powder blue; font-weight: bold; font-size: 12px;")
        btn_abort.clicked.connect(self.abort_tests)
        box_layout.addWidget(btn_abort)

        datalog_button = QPushButton("Data Log")
        datalog_button.setStyleSheet("background-color: powder blue; font-weight: bold; font-size: 12px;")
        datalog_button.clicked.connect(self.open_datalog_folder)
        box_layout.addWidget(datalog_button)

        btn_exit = QPushButton("Exit")
        btn_exit.setStyleSheet("color: red;font-weight: bold; font-size: 12px;")
        btn_exit.clicked.connect(self.close)
        box_layout.addWidget(btn_exit)

        group_box.setLayout(box_layout)
        left_layout.addWidget(group_box)

        main_layout.addLayout(left_layout)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(False)
        self.output_text.append("...")
        self.output_text.setFont(QFont("Courier", 10))
        self.output_text.setStyleSheet("background-color: ##f5f5f5;")  #lightblue
        right_layout.addWidget(self.output_text)

        main_layout.addLayout(right_layout)
        central_widget.setLayout(main_layout)

        # QProcess to run script
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(lambda: self.output_text.append("\n..."))

        self.process = QProcess()
        self.setup_process_signals()


    def run_instrument_check(self):
        instruments = check_instruments()
        self.output_text.append("\n".join(instruments))

    def open_test_selector(self):
        dialog = SelectTestDialog()
        if dialog.exec_():
            self.selected_test_scripts = dialog.get_selected_tests()
            self.output_text.append(f"\nSelected Tests: {', '.join(self.selected_test_scripts)}")

    def show_temp_dialog(self):
        dialog = TemperatureDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_temps = dialog.get_selected_temperatures()
            set_selected_temperatures(selected_temps)  # From test_file.py


            with open("selected_temps.json","w") as f:
                json.dump(selected_temps,f)

            self.output_text.append("\nTemperatures selected:")
            self.output_text.append(selected_temps)
            # print(set_selected_temperatures(selected_temps))



    # def show_temp_dialog(self):
    #     dialog = SelectTempDialog()
    #     if dialog.exec_():
    #         self.selected_temps = dialog.get_selected_temps()
    #         self.output_text.append(f"Selected: {', '.join(self.get_selected_temps)}")
    #         # print("Selected temperatures:", selected_temps)
    #         # set_selected_temperatures(selected_temps)


    def run_test_script(self):
        # addition = add()
        # self.output_text.append("\n".join(addition))

        if not self.selected_test_scripts:
            # self.output_text.append("[!] No tests selected.")
            QMessageBox.warning(self, "No Test Selected", "Please select at least one test before running.")
            return

        # Start running the queue
        self.test_queue = list(self.selected_test_scripts)
        self.current_test_index = -1
        self.run_next_test()

# to check temp
#     def run_temp_script(self):
#         # addition = add()
#         # self.output_text.append("\n".join(addition))
#
#         if not self.selected_temp_scripts:
#             # self.output_text.append("[!] No tests selected.")
#             QMessageBox.warning(self, "No Temp Selected", "Please select at least one test before running.")
#             return
#
#         # Start running the queue
#         self.test_queue = list(self.selected_temp_scripts)
#         self.current_test_index = -1
#         self.run_next_temp()

    def run_next_test(self):
        self.current_test_index += 1
        if self.current_test_index >= len(self.test_queue):
            self.output_text.append("\nAll selected tests completed.\n")
            return

        test_name = self.test_queue[self.current_test_index]
        self.output_text.append(f"\nRunning {test_name}.py...")
        self.process.start("python", [f"{test_name}.py"])

# to check temp
#     def run_next_temp(self):
#         self.current_temp_index += 1
#         if self.current_test_index >= len(self.test_queue):
#             self.output_text.append("\nAll selected temp completed.\n")
#             return
#
#         test_name = self.test_queue[self.current_temp_index]
#         self.output_text.append(f"\nRunning {test_name}.py...")
#         self.process.start("python", [f"{test_name}.py"])

    # def handle_stdout(self):
    #     text = self.process.readAllStandardOutput().data().decode()
    #     self.output_text.append(text)
    #
    #     lines = text.strip().splitlines()
    #     if not lines:
    #         return
    #
    #     last_line = lines[-1]
    #     prompt_keywords = ["Enter", "input", "Input","offset_1","offset_2", "Device"]
    #
    #     # words = re.findall(r'\b\w+\b',last_line)
    #     # if any(word in prompt_keywords for word in words):
    #     # pattern = r'\b( '+'|'.join(re.escape(k) for k in prompt_keywords) + r')\b'
    #     # if re.search(pattern, last_line, flags = re.IGNORECASE):
    #
    #     if any(keyword in text for keyword in prompt_keywords):
    #         user_input, ok = QInputDialog.getText(self, "Input Required", last_line.strip())
    #         if ok :
    #             self.process.write((user_input + '\n').encode())      # remove user_input in previous line if needed.

    def handle_stdout(self):
        text = self.process.readAllStandardOutput().data().decode()
        self.output_text.append(text)

        lines = text.strip().splitlines()
        if not lines:
            return
        last_line = lines[-1].strip()
        prompt_keywords = {"Enter",  "offset_1", "offset_2", "Device Number"}
        words = re.findall(r'\b\w+\b',last_line)
        if any(word in prompt_keywords for word in words):
            user_input, ok = QInputDialog.getText(self, "Input Required", last_line or "Enter_input:")
            if ok:
                self.process.write((user_input + '\n').encode())

    # def handle_stdout(self):
    #     text = self.process.readAllStandardOutput().data().decode()
    #     self.output_text.append(text)
    #
    #     lines = text.strip().splitlines()
    #     if not lines:
    #         return
    #     prompt_keywords = ["Enter", "input", "Input", "offset_1", "offset_2", "Device", "Temperature", "temperature",
    #                        "temp", "Temp"]
    #
    #     pattern = r'\b( ' + '|'.join(re.escape(k) for k in prompt_keywords) + r')\b'
    #     for line in reversed(lines):
    #         if re.search(pattern, line, flags=re.IGNORECASE):
    #             if not  self.prompt_active:
    #                 self.prompt_required.emit(line.strip())
    #                 self.promt_active = True
    #             break
    #
    # def show_input_prompt(self,prompt_text):
    #     user_input, ok = QInputDialog.getText(self, "Input Required", prompt_text,flags=Qt.WindowFlags(Qt.WindowModal))
    #     self.prompt_active = False
    #     if ok:
    #         self.process.write((user_input + '\n').encode())



    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output_text.append(f"<span style='color:red;'>{data}</span>")

    def run_script_finished(self):
        self.output_text.append(f"Finished: {self.test_queue[self.current_test_index]}")
        self.run_next_test()

    def setup_process_signals(self):
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.run_script_finished)

    def abort_tests(self):
        # 1. Kill the currently running process (if any)
        if self.process.state() != QProcess.NotRunning:
            self.process.kill()
            self.process.waitForFinished()

        # 2. Clear queues and reset state
        self.test_queue.clear()
        self.current_test_index = -1
        self.output_text.append("\nTest aborted by user.")

    def open_datalog_folder(self):
        # Set your datalog folder path here
        folder_path = os.path.abspath("C:\\Users\\10633\\PycharmProjects\\GUI_Test_Development\\Results")  # Adjust path if needed
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())