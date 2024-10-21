import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, \
    QHBoxLayout, QCheckBox, QTextEdit, QFormLayout, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt
import pandas as pd

class ExpertSystemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Experto - Consulta General")
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        self.layout = QVBoxLayout()

        # Styling the window
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f9;
                font-family: Arial;
            }
            QLabel {
                font-size: 24px;
                color: #333;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                color: black;
                padding: 4px;
                font-size: 18px;
            }
            QTextEdit {
                font-size: 18px;
                color: black;
            }
            QFormLayout {
                color: black;
            }
            QCheckBox {
                color: black;
            }
            QScrollArea {
                border: none;
            }
        """)

        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Label
        self.label = QLabel("Sistema Experto General")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Button to load CSV
        self.load_csv_button = QPushButton("Cargar CSV")
        self.load_csv_button.clicked.connect(self.load_csv)
        self.layout.addWidget(self.load_csv_button)

        # Horizontal layout for the button
        button_layout = QHBoxLayout()
        self.new_request_button = QPushButton("Nueva Solicitud")
        self.new_request_button.setFixedWidth(180)
        self.new_request_button.setFixedHeight(35)
        self.new_request_button.clicked.connect(self.start_new_request)
        button_layout.addStretch(1)
        button_layout.addWidget(self.new_request_button)
        button_layout.addStretch(1)
        self.layout.addLayout(button_layout)

        # Reasoning method label and combobox
        label_layout = QHBoxLayout()
        self.reasoning_method_label = QLabel("Selecciona el método de razonamiento:")
        self.reasoning_method_label.setAlignment(Qt.AlignCenter)
        label_layout.addStretch(1)
        label_layout.addWidget(self.reasoning_method_label)
        label_layout.addStretch(1)
        self.layout.addLayout(label_layout)

        combobox_layout = QHBoxLayout()
        self.reasoning_method_combo = QComboBox()
        self.reasoning_method_combo.addItems(["Forward-Chaining", "Backward-Chaining"])
        self.reasoning_method_combo.setFixedWidth(200)
        self.reasoning_method_combo.setFixedHeight(35)
        combobox_layout.addStretch(1)
        combobox_layout.addWidget(self.reasoning_method_combo)
        combobox_layout.addStretch(1)
        self.layout.addLayout(combobox_layout)

        # Scroll area for attributes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(200)  # Set a fixed height for the scroll area
        self.attributes_widget = QWidget()
        self.attributes_layout = QVBoxLayout()
        self.attributes_widget.setLayout(self.attributes_layout)
        self.scroll_area.setWidget(self.attributes_widget)
        self.layout.addWidget(self.scroll_area)
        self.scroll_area.hide()  # Initially hide the scroll area

        # Output display
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # Create a central widget to organize the layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Variables for reasoning
        self.known_facts = set()
        self.known_false = set()
        self.attribute_checkboxes = []
        self.submit_button = None
        self.rule_set = None
        self.target_column = None

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.rule_set = pd.read_csv(file_path)
                self.target_column = self.rule_set.columns[0]
                self.output_text.append(f"CSV loaded successfully: {os.path.basename(file_path)}")
                self.output_text.append(f"Target column: {self.target_column}")
            except Exception as e:
                self.output_text.append(f"Error loading CSV: {str(e)}")

    def start_new_request(self):
        if self.rule_set is None:
            self.output_text.append("Please load a CSV file first.")
            return

        selected_method = self.reasoning_method_combo.currentText()
        self.output_text.clear()
        if selected_method == "Forward-Chaining":
            self.output_text.append("Iniciando forward-chaining...")
            self.setup_forward_chaining()
        elif selected_method == "Backward-Chaining":
            self.output_text.append("Iniciando backward-chaining...")
            self.setup_backward_chaining()

    def clear_checkboxes(self):
        for checkbox in self.attribute_checkboxes:
            self.attributes_layout.removeWidget(checkbox)
            checkbox.deleteLater()
        self.attribute_checkboxes.clear()

        if self.submit_button is not None:
            self.layout.removeWidget(self.submit_button)
            self.submit_button.deleteLater()
            self.submit_button = None

    def setup_forward_chaining(self):
        self.clear_checkboxes()
        self.known_facts = set()
        self.known_false = set()

        all_attributes = set()
        for attributes in self.rule_set.iloc[:, 1:].values:
            all_attributes.update(attributes[~pd.isna(attributes)])

        for attribute in sorted(all_attributes):
            checkbox = QCheckBox(str(attribute))
            self.attribute_checkboxes.append(checkbox)
            self.attributes_layout.addWidget(checkbox)

        self.scroll_area.show()  # Show the scroll area

        if self.submit_button is None:
            self.submit_button = QPushButton("Iniciar análisis")
            self.submit_button.clicked.connect(self.run_forward_chaining)
            self.layout.addWidget(self.submit_button)

    def run_forward_chaining(self):
        self.known_facts = set(checkbox.text() for checkbox in self.attribute_checkboxes if checkbox.isChecked())
        self.output_text.append("Atributos seleccionados: " + ", ".join(self.known_facts))

        derived_conditions = set()
        for _, row in self.rule_set.iterrows():
            condition = row[self.target_column]
            attributes = set(row.dropna().values[1:])
            if attributes.issubset(self.known_facts):
                derived_conditions.add(condition)

        if derived_conditions:
            self.output_text.append(f"Condiciones {self.target_column} derivadas:")
            for condition in derived_conditions:
                self.output_text.append(f"- {condition}")
        else:
            self.output_text.append(f"No se pudo derivar ninguna condición {self.target_column} con los atributos proporcionados.")

    def setup_backward_chaining(self):
        self.clear_checkboxes()
        self.known_facts = set()
        self.known_false = set()
        self.remaining_conditions = self.rule_set[self.target_column].tolist()
        self.scroll_area.show()  # Show the scroll area for backward chaining
        self.dynamic_attribute_inquiry()

    def dynamic_attribute_inquiry(self):
        if len(self.remaining_conditions) == 0:
            self.output_text.append("No se pudieron derivar más condiciones.")
            return

        condition = self.remaining_conditions[0]
        condition_attributes = self.rule_set.loc[self.rule_set[self.target_column] == condition].dropna(axis=1).values.flatten().tolist()[1:]

        condition_attributes = [attr for attr in condition_attributes if
                                attr not in self.known_facts and attr not in self.known_false]

        if not condition_attributes:
            self.output_text.append(f"Ya se verificaron todos los atributos para {condition}.")
            self.process_next_condition()
            return

        self.clear_checkboxes()  # Clear previous checkboxes

        for attribute in condition_attributes:
            checkbox = QCheckBox(str(attribute))
            self.attribute_checkboxes.append(checkbox)
            self.attributes_layout.addWidget(checkbox)

        if self.submit_button is None:
            self.submit_button = QPushButton("Enviar selección")
            self.submit_button.clicked.connect(self.process_attributes)
            self.layout.addWidget(self.submit_button)

    def process_attributes(self):
        for checkbox in self.attribute_checkboxes:
            if checkbox.isChecked():
                self.known_facts.add(checkbox.text())
            else:
                self.known_false.add(checkbox.text())

        self.process_next_condition()

    def process_next_condition(self):
        current_condition = self.remaining_conditions[0]
        condition_attributes = self.rule_set.loc[self.rule_set[self.target_column] == current_condition].dropna(
            axis=1).values.flatten().tolist()[1:]

        if all(str(attr) in self.known_facts for attr in condition_attributes):
            self.output_text.append(f"¡Condición {self.target_column} derivada: {current_condition}!")
            self.remaining_conditions = []  # Stop when a condition is deduced
        else:
            self.output_text.append(f"No se pudo derivar la condición {self.target_column}: {current_condition}.")
            self.remaining_conditions.pop(0)

        if len(self.remaining_conditions) > 0:
            self.dynamic_attribute_inquiry()
        else:
            self.output_text.append("No se pudieron derivar más condiciones.")
            self.clear_checkboxes()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpertSystemWindow()
    window.show()
    sys.exit(app.exec_())
