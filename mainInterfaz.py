import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QHBoxLayout, QCheckBox, QTextEdit, QFormLayout, QScrollArea
from PyQt5.QtCore import Qt
import pandas as pd

filepath = '/Users/jovany/PycharmProjects/Expert-System-Implementation-with-Pytho/DatasetSistemaExperto.csv'
rule_set = pd.read_csv(filepath)

class ExpertSystemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Experto - Consulta Médica")
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
        self.label = QLabel("Formulario de Consulta")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

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

        # Scroll area for symptoms
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(200)  # Set a fixed height for the scroll area
        self.symptoms_widget = QWidget()
        self.symptoms_layout = QVBoxLayout()
        self.symptoms_widget.setLayout(self.symptoms_layout)
        self.scroll_area.setWidget(self.symptoms_widget)
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
        self.symptom_checkboxes = []
        self.submit_button = None

    def start_new_request(self):
        selected_method = self.reasoning_method_combo.currentText()
        if selected_method == "Forward-Chaining":
            self.output_text.append("Iniciando forward-chaining...")
            self.setup_forward_chaining()
        elif selected_method == "Backward-Chaining":
            self.output_text.append("Iniciando backward-chaining...")
            self.setup_backward_chaining()

    def clear_checkboxes(self):
        for checkbox in self.symptom_checkboxes:
            self.symptoms_layout.removeWidget(checkbox)
            checkbox.deleteLater()
        self.symptom_checkboxes.clear()

        if self.submit_button is not None:
            self.layout.removeWidget(self.submit_button)
            self.submit_button.deleteLater()
            self.submit_button = None

    def setup_forward_chaining(self):
        self.clear_checkboxes()
        self.known_facts = set()
        self.known_false = set()

        all_symptoms = set()
        for symptoms in rule_set.iloc[:, 1:].values:
            all_symptoms.update(symptoms[~pd.isna(symptoms)])

        for symptom in sorted(all_symptoms):
            checkbox = QCheckBox(symptom)
            self.symptom_checkboxes.append(checkbox)
            self.symptoms_layout.addWidget(checkbox)

        self.scroll_area.show()  # Show the scroll area

        if self.submit_button is None:
            self.submit_button = QPushButton("Iniciar diagnóstico")
            self.submit_button.clicked.connect(self.run_forward_chaining)
            self.layout.addWidget(self.submit_button)

    def run_forward_chaining(self):
        self.known_facts = set(checkbox.text() for checkbox in self.symptom_checkboxes if checkbox.isChecked())
        self.output_text.append("Síntomas seleccionados: " + ", ".join(self.known_facts))

        derived_conditions = set()
        for _, row in rule_set.iterrows():
            condition = row['Condición']
            symptoms = set(row.dropna().values[1:])
            if symptoms.issubset(self.known_facts):
                derived_conditions.add(condition)

        if derived_conditions:
            self.output_text.append("Condiciones derivadas:")
            for condition in derived_conditions:
                self.output_text.append(f"- {condition}")
        else:
            self.output_text.append("No se pudo derivar ninguna condición con los síntomas proporcionados.")

    def setup_backward_chaining(self):
        self.clear_checkboxes()
        self.known_facts = set()
        self.known_false = set()
        self.remaining_conditions = rule_set['Condición'].tolist()
        self.scroll_area.show()  # Show the scroll area for backward chaining
        self.dynamic_symptom_inquiry()

    def dynamic_symptom_inquiry(self):
        if len(self.remaining_conditions) == 0:
            self.output_text.append("No se pudieron derivar más condiciones.")
            return

        condition = self.remaining_conditions[0]
        condition_symptoms = rule_set.loc[rule_set['Condición'] == condition].dropna(axis=1).values.flatten().tolist()[1:]

        condition_symptoms = [symptom for symptom in condition_symptoms if symptom not in self.known_facts and symptom not in self.known_false]

        if not condition_symptoms:
            self.output_text.append(f"Ya se verificaron todos los síntomas para {condition}.")
            self.process_next_condition()
            return

        self.clear_checkboxes()  # Clear previous checkboxes

        for symptom in condition_symptoms:
            checkbox = QCheckBox(symptom)
            self.symptom_checkboxes.append(checkbox)
            self.symptoms_layout.addWidget(checkbox)

        if self.submit_button is None:
            self.submit_button = QPushButton("Enviar selección")
            self.submit_button.clicked.connect(self.process_symptoms)
            self.layout.addWidget(self.submit_button)

    def process_symptoms(self):
        for checkbox in self.symptom_checkboxes:
            if checkbox.isChecked():
                self.known_facts.add(checkbox.text())
            else:
                self.known_false.add(checkbox.text())

        self.process_next_condition()

    def process_next_condition(self):
        current_condition = self.remaining_conditions[0]
        condition_symptoms = rule_set.loc[rule_set['Condición'] == current_condition].dropna(axis=1).values.flatten().tolist()[1:]

        if all(symptom in self.known_facts for symptom in condition_symptoms):
            self.output_text.append(f"¡Condición derivada: {current_condition}!")
            self.remaining_conditions = []  # Stop when a condition is deduced
        else:
            self.output_text.append(f"No se pudo derivar la condición: {current_condition}.")
            self.remaining_conditions.pop(0)

        if len(self.remaining_conditions) > 0:
            self.dynamic_symptom_inquiry()
        else:
            self.output_text.append("No se pudieron derivar más condiciones.")
            self.clear_checkboxes()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpertSystemWindow()
    window.show()
    sys.exit(app.exec())
