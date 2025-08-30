from PyQt5.QtWidgets import (
    QDialog, QTableWidget, QTableWidgetItem, QCheckBox,
    QDialogButtonBox, QVBoxLayout, QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt

class TemperatureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Temperature")
        self.setGeometry(100, 100, 300, 250)

        self.temperatures = ["25",  "125", "-40"]

        layout = QVBoxLayout()

        # Create table widget with two columns
        self.table = QTableWidget()
        self.table.setRowCount(len(self.temperatures))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Temperature", "Select"])
        self.table.verticalHeader().setVisible(False)

        # Fill rows
        for row, temp in enumerate(self.temperatures):
            # Column 0: temperature value
            temp_item = QTableWidgetItem(temp)
            temp_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 0, temp_item)

            # Column 1: checkbox widget
            checkbox = QCheckBox()
            checkbox_widget = QWidget()
            layout_checkbox = QHBoxLayout(checkbox_widget)
            layout_checkbox.addWidget(checkbox)
            layout_checkbox.setAlignment(Qt.AlignCenter)
            layout_checkbox.setContentsMargins(0, 0, 0, 0)

            self.table.setCellWidget(row, 1, checkbox_widget)

        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        # OK / Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.on_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_selected_temperatures(self):
        selected = []
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, 1)
            checkbox = checkbox_widget.layout().itemAt(0).widget()
            if checkbox.isChecked():
                selected.append(int(self.table.item(row, 0).text()))
                self.accept()
        return str(selected)

    def on_accept(self):
        selected = self.get_selected_temperatures()
        print("Selected temperatures:", str(selected))
        self.accept()

    def get_selected_temp(self):
        return self.get_selected_temp