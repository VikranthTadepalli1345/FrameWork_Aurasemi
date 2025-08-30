from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QCheckBox, QLabel)
from PyQt5.QtCore import Qt

class SelectTestDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Test")
        self.setFixedSize(350, 300)
        self.selected_tests = []

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Test"))

        h_layout = QHBoxLayout()

        # Left table for test names with checkboxes
        self.test_table = QTableWidget(3, 2)
        self.test_table.setHorizontalHeaderLabels(["Test", "Select"])
        self.test_table.setColumnWidth(0, 150)

        test_names = [

            "GROUP_1_OPT",
            "GROUP_2_A",
            "GROUP_3_OPT_bdfs"
        ]

        for row, name in enumerate(test_names):
            self.test_table.setItem(row, 0, QTableWidgetItem(name))
            checkbox = QCheckBox()
            self.test_table.setCellWidget(row, 1, checkbox)

        h_layout.addWidget(self.test_table)

        # Right dummy table for test settings
        # self.settings_table = QTableWidget(5, 2)
        # self.settings_table.setHorizontalHeaderLabels(["Temperatures(°C)", "Loop Count"])
        # settings = [("-25", "4"), ("25", "5"), ("40", "3"), ("60", "2"), ("90", "3")]
        # for row, (temp, loop) in enumerate(settings):
        #     self.settings_table.setItem(row, 0, QTableWidgetItem(temp))
        #     self.settings_table.setItem(row, 1, QTableWidgetItem(loop))
        #
        # h_layout.addWidget(self.settings_table)


        layout.addLayout(h_layout)

        # OK / Cancel buttons
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept_selection)
        btn_layout.addWidget(ok_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def accept_selection(self):
        self.selected_tests = []
        for row in range(self.test_table.rowCount()):
            checkbox = self.test_table.cellWidget(row, 1)
            if checkbox and checkbox.isChecked():
                item = self.test_table.item(row, 0)
                self.selected_tests.append(item.text())
        self.accept()

    def get_selected_tests(self):
        return self.selected_tests
