import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
import pandas as pd

filepath = 'C:\\Users\\alexi\\Documents\\03 - PYTHON DEV\\DatasetSistemaExperto.csv'
rule_set = pd.read_csv(filepath)


class ExpertSystemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Experto - Consulta Médica")
        self.setGeometry(100, 100, 600, 300)

        # Crear el layout principal
        self.layout = QVBoxLayout()

        # Estilo de la ventana
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f9;
                font-family: Arial;
            }
            QLabel {
                font-size: 24px;
                color: #000000;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 5px;
                padding: 8px;  /* Reducir el padding para hacer más compacto el botón */
                font-size: 18px;  /* Reducir el tamaño de fuente del botón */
            }
            QPushButton:hover {
                background-color: #005f99;
            }
            QComboBox {
                background-color: white;
                foreground-color: black;
                border: 1px solid #ccc;
                padding: 4px;  /* Reducir el padding del combobox */
                font-size: 18px;
            }
        """)

        # Reducir los márgenes del layout principal
        self.layout.setContentsMargins(10, 10, 10, 10)  # Márgenes del layout (izq, arriba, der, abajo)
        self.layout.setSpacing(10)  # Reducir el espaciado entre widgets

        # Etiqueta para el formulario
        self.label = QLabel("Formulario de Consulta")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Crear un layout horizontal para centrar el botón
        button_layout = QHBoxLayout()

        # Botón para iniciar nueva solicitud
        self.new_request_button = QPushButton("Nueva Solicitud")
        self.new_request_button.setFixedWidth(180)  # Ajustar ancho fijo del botón
        self.new_request_button.setFixedHeight(35)  # Ajustar altura fija del botón
        self.new_request_button.clicked.connect(self.start_new_request)

        # Añadir el botón al layout horizontal y centrarlo
        button_layout.addStretch(1)  # Espacio a la izquierda
        button_layout.addWidget(self.new_request_button)  # Añadir el botón
        button_layout.addStretch(1)  # Espacio a la derecha

        # Añadir el layout horizontal (con el botón centrado) al layout principal
        self.layout.addLayout(button_layout)

        # ComboBox para elegir entre forward o backward chaining
        # Creamos un layout horizontal para centrar el label
        label_layout = QHBoxLayout()
        self.reasoning_method_label = QLabel("Selecciona el método de razonamiento:")
        self.reasoning_method_label.setAlignment(Qt.AlignCenter)  # Centrar la etiqueta
        label_layout.addStretch(1)  # Espacio a la izquierda para centrar
        label_layout.addWidget(self.reasoning_method_label)  # Añadir el label centrado
        label_layout.addStretch(1)  # Espacio a la derecha para centrar

        # Añadir el layout del label centrado al layout principal
        self.layout.addLayout(label_layout)

        # Añadir un layout horizontal para centrar el combobox
        combobox_layout = QHBoxLayout()
        self.reasoning_method_combo = QComboBox()
        self.reasoning_method_combo.addItems(["Forward-Chaining", "Backward-Chaining"])
        self.reasoning_method_combo.setFixedWidth(200)
        self.reasoning_method_combo.setFixedHeight(35)  # Ajustar altura fija del combo box

        # Añadir el combobox al layout horizontal y centrarlo
        combobox_layout.addStretch(1)  # Espacio a la izquierda
        combobox_layout.addWidget(self.reasoning_method_combo)  # Añadir el combobox
        combobox_layout.addStretch(1)  # Espacio a la derecha

        # Añadir el layout del combobox al layout principal
        self.layout.addLayout(combobox_layout)

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
