from PyQt6.QtWidgets import QApplication, QWidget, QRadioButton, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
from funcoes_gui import selecionar_pdf, enviar_dados, adicionar_linhas
from PyQt6.QtGui import QIcon
import sys

pdf_padrao = "C:/Users/User/Documents/GitHub/marmoraria-rm-pdf-auto/orcamento-vazio.pdf"
dados = {}

class PreencherPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.contador = 4 
        self.pdf_path = pdf_padrao 
        self.linhas = []  # Lista para guardar os campos dinâmicos

        # Carregar o arquivo de estilos (QSS)
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.linhas_layout = QVBoxLayout()# Layout específico para as linhas
        self.layout.addLayout(self.linhas_layout)  
        self.layout.addLayout(self.grid_layout)  # Adiciona a grade ao layout principal

        self.init_ui()  # Inicializa a interface

    def init_ui(self):
        self.setWindowTitle("Orçamento PDF Marmoraria R&M")
        self.setWindowIcon(QIcon("pdficon.png"))
        self.setGeometry(10, 280, 1000, 200)

        self.label_titulo = QLabel("Orçamento")
        self.label_titulo.setObjectName("titulo")
        self.layout.addWidget(self.label_titulo)

        self.btn_selecionar = QPushButton("Selecionar outro PDF")
        self.btn_selecionar.clicked.connect(lambda: selecionar_pdf(self))
        self.grid_layout.addWidget(self.btn_selecionar, 0, 2)

        self.linhas_layout = QVBoxLayout()
        self.layout.addLayout(self.linhas_layout)

        adicionar_linhas(self, 1, self.grid_layout)
        adicionar_linhas(self, 2, self.grid_layout)
        adicionar_linhas(self, 3, self.grid_layout)

        self.btn_nova_linha = QPushButton("ADICIONAR NOVA LINHA")
        self.btn_nova_linha.clicked.connect(lambda: adicionar_linhas(self, len(self.linhas) + 1, self.grid_layout))
        self.layout.addWidget(self.btn_nova_linha)

                # Total a prazo
        self.label_total_prazo = QLabel("TOTAL A PRAZO")
        self.grid_layout.addWidget(self.label_total_prazo, 5, 1)
        self.input_total_prazo = QLineEdit()
        self.grid_layout.addWidget(self.input_total_prazo, 5, 2)

        # Desconto
        self.label_desconto = QLabel("DESCONTO")
        self.grid_layout.addWidget(self.label_desconto, 5, 3)
        self.radio_5 = QRadioButton("5%")
        self.radio_7 = QRadioButton("7%")
        desconto_layout = QHBoxLayout()
        desconto_layout.addWidget(self.radio_5)
        desconto_layout.addWidget(self.radio_7)
        self.grid_layout.addLayout(desconto_layout, 5, 4)

        # Total à vista
        self.label_total_vista = QLabel("TOTAL A VISTA")
        self.grid_layout.addWidget(self.label_total_vista, 5, 5)
        self.input_total_vista = QLineEdit()
        self.grid_layout.addWidget(self.input_total_vista, 5, 6)

        # Observações
        self.label_obs = QLabel("OBSERVAÇÕES")
        self.grid_layout.addWidget(self.label_obs, 6, 0)
        self.input_obs = QLineEdit()
        self.grid_layout.addWidget(self.input_obs, 7, 0, 1, 7)

        # Botão Ir para próxima página
        self.btn_proxima_pagina = QPushButton("IR PARA PRÓXIMA PÁGINA")
        self.grid_layout.addWidget(self.btn_proxima_pagina, 8, 0, 1, 7)

        self.btn_preencher = QPushButton("Preencher PDF")
        self.btn_preencher.clicked.connect(lambda: enviar_dados(self))
        self.layout.addWidget(self.btn_preencher)

        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreencherPDFApp()
    window.show()
    sys.exit(app.exec())
