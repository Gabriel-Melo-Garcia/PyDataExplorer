import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QVBoxLayout, QSpacerItem, QSizePolicy
)

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.initUI()

    def initUI(self):
        # Define o tamanho mínimo da janela
        self.setMinimumSize(400, 300)

        # Widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Label (QLineEdit)
        self.label = QLineEdit(self)
        self.label.setReadOnly(True)
        self.label.setText(str(self.value))
        self.label.setFixedSize(100, 50)
        self.label.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                text-align: center;
            }
        """)

        # Botão
        button = QPushButton('+', self)
        button.clicked.connect(self.on_btn_press)
        button.setFixedSize(100, 50)

        # Espaçadores para centralizar os widgets
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Adiciona os widgets ao layout
        main_layout.addItem(spacer_top)  # Espaçador no topo
        main_layout.addWidget(self.label, 0, alignment=Qt.AlignmentFlag.AlignCenter)  # Label centralizado
        main_layout.addWidget(button, 0, alignment=Qt.AlignmentFlag.AlignCenter)  # Botão centralizado
        main_layout.addItem(spacer_bottom)  # Espaçador na base

        # Define o widget central
        self.setCentralWidget(central_widget)

        # Mostra a janela
        self.show()

    def on_btn_press(self):
        # Incrementa o valor e atualiza o label
        self.value += 1
        self.label.setText(str(self.value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec())