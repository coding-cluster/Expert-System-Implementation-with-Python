import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox
import pandas as pd

filepath = 'C:\\Users\\alexi\\Documents\\03 - PYTHON DEV\\DatasetSistemaExperto.csv'
rule_set = pd.read_csv(filepath)

class ExpertSystemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Experto - Consulta Médica")
        self.setGeometry(100, 100, 200, 100)

        # Crear el layout principal
        self.layout = QVBoxLayout()

        # Etiqueta para el formulario
        self.label = QLabel("Formulario de Consulta")
        self.layout.addWidget(self.label)

        # Botón para iniciar nueva solicitud
        self.new_request_button = QPushButton("Nueva Solicitud")
        self.new_request_button.clicked.connect(self.start_new_request)
        self.layout.addWidget(self.new_request_button)

        # ComboBox para elegir entre forward o backward chaining
        self.reasoning_method_label = QLabel("Selecciona el método de razonamiento:")
        self.layout.addWidget(self.reasoning_method_label)
        self.reasoning_method_combo = QComboBox()
        self.reasoning_method_combo.addItems(["Forward-Chaining", "Backward-Chaining"])
        self.layout.addWidget(self.reasoning_method_combo)

        # Crear un widget central para organizar el layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def start_new_request(self):
        selected_method = self.reasoning_method_combo.currentText()
        if selected_method == "Forward-Chaining":
            print("Iniciando forward-chaining...")
            # Aquí iría la lógica para el forward chaining
        elif selected_method == "Backward-Chaining":
            print("Iniciando backward-chaining...")
            # Aquí iría la lógica para el backward chaining

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpertSystemWindow()
    window.show()
    sys.exit(app.exec())