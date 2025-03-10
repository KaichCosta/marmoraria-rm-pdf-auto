from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
#from gerador_pdf import preencher_pdf, atualizar_posicoes, posicoes
from funcoes_gui import selecionar_pdf, enviar_dados, adicionar_linhas
import sys

pdf_padrao = "C:/Users/User/Documents/GitHub/marmoraria-rm-pdf-auto/orcamento-vazio.pdf"
dados = {}

class PreencherPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.contador = 1
        self.pdf_path = pdf_padrao
        self.linhas = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Orçamento PDF Marmoraria R&M")
        self.setGeometry(100, 280, 800, 200)

        self.layout = QVBoxLayout()

        self.label_pdf = QLabel("PDF padrão já selecionado")
        self.layout.addWidget(self.label_pdf)

        self.btn_selecionar = QPushButton("Selecionar outro PDF")
        self.btn_selecionar.clicked.connect(lambda: selecionar_pdf(self))
        self.layout.addWidget(self.btn_selecionar)

        for i in range(1, 4):
            adicionar_linhas(self, i)
            #self.adicionar_linhas(i)

        self.btn_nova_linha = QPushButton("ADICIONAR NOVA LINHA")
        self.btn_nova_linha.clicked.connect(lambda: adicionar_linhas(self, self.contador))
        self.layout.addWidget(self.btn_nova_linha)

        self.btn_preencher = QPushButton("Preencher PDF")
        self.btn_preencher.clicked.connect(lambda: enviar_dados(self))
        self.layout.addWidget(self.btn_preencher)

        self.setLayout(self.layout)
