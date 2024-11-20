from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QMessageBox, QFileDialog, QGroupBox
)
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from nfa import NFA
import sys
import os
from PIL import Image

class NFA_GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicialización de la ventana principal
        self.setWindowTitle("NFA Interface - PyQt6")
        self.setGeometry(100, 100, 700, 800)  # Posición (x, y) y tamaño (ancho, alto)

        # Variables para almacenar los datos del autómata
        self.nfa = NFA()
        self.states = set()
        self.alphabet = set()
        self.start_state = None
        self.accept_states = set()

        # Layout principal
        main_layout = QVBoxLayout()

        # Crear Widgets
        self.create_widgets(main_layout)

        # Configuración del widget central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_widgets(self, layout):
        # Crear el layout para la configuración del NFA
        nfa_config_group = QGroupBox("Configuración del NFA")
        nfa_config_layout = QVBoxLayout()

        # Botones de configuración del NFA
        add_state_button = QPushButton("Añadir Estado")
        add_state_button.clicked.connect(self.add_state)
        define_alphabet_button = QPushButton("Definir Alfabeto")
        define_alphabet_button.clicked.connect(self.define_alphabet)
        set_start_state_button = QPushButton("Definir Estado Inicial")
        set_start_state_button.clicked.connect(self.set_start_state)
        add_accept_state_button = QPushButton("Añadir Estado de Aceptación")
        add_accept_state_button.clicked.connect(self.add_accept_state)
        add_transition_button = QPushButton("Añadir Transición")
        add_transition_button.clicked.connect(self.add_transition)

        # Añadir botones al layout de configuración
        nfa_config_layout.addWidget(add_state_button)
        nfa_config_layout.addWidget(define_alphabet_button)
        nfa_config_layout.addWidget(set_start_state_button)
        nfa_config_layout.addWidget(add_accept_state_button)
        nfa_config_layout.addWidget(add_transition_button)
        nfa_config_group.setLayout(nfa_config_layout)

        # Crear el layout para la validación de cadenas
        operations_group = QGroupBox("Operaciones")
        operations_layout = QHBoxLayout()

        validate_string_button = QPushButton("Validar Cadena")
        validate_string_button.clicked.connect(self.validate_string)
        show_nfa_button = QPushButton("Mostrar NFA")
        show_nfa_button.clicked.connect(self.show_nfa)

        # Añadir botones al layout de operaciones
        operations_layout.addWidget(validate_string_button)
        operations_layout.addWidget(show_nfa_button)
        operations_group.setLayout(operations_layout)

        # Crear layout para la visualización del NFA
        self.image_label = QLabel("Visualización del NFA")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Añadir grupos al layout principal
        layout.addWidget(nfa_config_group)
        layout.addWidget(operations_group)
        layout.addWidget(self.image_label)

    def add_state(self):
        # Pedir al usuario que ingrese un estado
        state, ok = QInputDialog.getText(self, "Añadir Estado", "Ingrese el nombre del estado:")
        if ok and state:
            self.states.add(state)
            self.nfa.add_state(state)
            QMessageBox.information(self, "Estado Añadido", f"Estado '{state}' añadido correctamente.")

    def define_alphabet(self):
        # Pedir al usuario que ingrese los símbolos del alfabeto
        symbols, ok = QInputDialog.getText(self, "Definir Alfabeto", "Ingrese los símbolos del alfabeto (separados por comas):")
        if ok and symbols:
            for symbol in symbols.split(','):
                self.alphabet.add(symbol.strip())
            self.nfa.alphabet = self.alphabet
            QMessageBox.information(self, "Alfabeto Definido", f"Alfabeto definido: {', '.join(self.alphabet)}")

    def set_start_state(self):
        # Pedir al usuario que defina el estado inicial
        state, ok = QInputDialog.getText(self, "Definir Estado Inicial", "Ingrese el estado inicial:")
        if ok and state in self.states:
            self.start_state = state
            self.nfa.set_start_state(state)
            QMessageBox.information(self, "Estado Inicial", f"Estado inicial definido como '{state}'.")
        else:
            QMessageBox.critical(self, "Error", "El estado no existe en el conjunto de estados.")

    def add_accept_state(self):
        # Pedir al usuario que añada un estado de aceptación
        state, ok = QInputDialog.getText(self, "Añadir Estado de Aceptación", "Ingrese el estado de aceptación:")
        if ok and state in self.states:
            self.accept_states.add(state)
            self.nfa.add_accept_state(state)
            QMessageBox.information(self, "Estado de Aceptación", f"Estado de aceptación '{state}' añadido correctamente.")
        else:
            QMessageBox.critical(self, "Error", "El estado no existe en el conjunto de estados.")

   
    def add_transition(self):
        """
        Permite al usuario añadir una transición entre estados.
        Realiza validaciones para asegurarse de que la transición sea válida.
        """
        # Pedir al usuario que ingrese el estado actual
        current_state, ok1 = QInputDialog.getText(self, "Añadir Transición", "Ingrese el estado actual:")
        if not ok1 or current_state not in self.states:
            QMessageBox.critical(self, "Error", "El estado actual no existe.")
            return  # Salir si el estado no es válido

        # Pedir al usuario que ingrese el símbolo
        symbol, ok2 = QInputDialog.getText(self, "Añadir Transición", "Ingrese el símbolo (o deje vacío para ε):")
        if not ok2:
            symbol = None  # Si no se ingresa símbolo, se considera ε (epsilon)
        elif symbol == "":
            symbol = None  # Si el símbolo es una cadena vacía, lo tratamos como ε

        # Validar el símbolo solo si no es None
        if symbol is not None and symbol not in self.alphabet:
            QMessageBox.critical(self, "Error", f"El símbolo '{symbol}' no está en el alfabeto.")
            return  # Salir si el símbolo no es válido

        # Pedir al usuario que ingrese los estados siguientes
        next_state, ok3 = QInputDialog.getText(self, "Añadir Transición", "Ingrese los estados siguientes (separados por comas):")
        if not ok3:
            QMessageBox.critical(self, "Error", "Debe ingresar al menos un estado siguiente.")
            return

        # Convertir los estados siguientes en un conjunto y verificar su existencia
        next_states = set(next_state.split(','))
        if not all(ns in self.states for ns in next_states):
            QMessageBox.critical(self, "Error", "Uno o más estados siguientes no existen.")
            return  # Salir si algún estado siguiente no es válido

        # Agregar la transición al NFA (considerando que el símbolo puede ser None o un símbolo del alfabeto)
        self.nfa.add_transition(current_state, symbol, next_states)
        
        # Mostrar mensaje de éxito
        QMessageBox.information(self, "Transición Añadida", f"Transición añadida: {current_state} --{symbol if symbol else 'ε'}--> {', '.join(next_states)}")

   
    def validate_string(self):
        # Pedir al usuario una cadena a validar
        input_string, ok = QInputDialog.getText(self, "Validar Cadena", "Ingrese la cadena a validar:")
        if ok and input_string is not None:
            result = self.nfa.validate_string(input_string)
            QMessageBox.information(self, "Resultado", f"La cadena {'es aceptada' if result else 'no es aceptada'} por el NFA.")

    
    def show_nfa(self):
        # Mostrar el gráfico del NFA
        self.nfa.plot("nfa_diagram")
        self.update_nfa_image("nfa_diagram.png")

    def update_nfa_image(self, file_path):
        # Cargar la imagen del NFA y mostrarla en la interfaz
        if os.path.exists(file_path):
            image = Image.open(file_path)
            image = image.resize((400, 400), Image.Resampling.LANCZOS)
            image.save("resized_nfa_diagram.png")
            pixmap = QPixmap("resized_nfa_diagram.png")
            self.image_label.setPixmap(pixmap)
        else:
            QMessageBox.critical(self, "Error", "No se pudo cargar la imagen del NFA.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NFA_GUI()
    window.show()
    sys.exit(app.exec())
