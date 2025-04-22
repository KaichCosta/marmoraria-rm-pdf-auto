from PyQt6.QtWidgets import QApplication,QVBoxLayout, QWidget, QTextEdit, QGridLayout, QPushButton, QLabel, QLineEdit, QComboBox, QScrollArea
from funcoes_gui import selecionar_pdf, enviar_dados, adicionar_linhas, processar_texto
from PyQt6.QtGui import QIcon, QPixmap
import sys

pdf_padrao = "C:/Users/User/Documents/GitHub/marmoraria-rm-pdf-auto/orcamento-vazio.pdf"
dados = {}

class PreencherPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.contador = 4
        self.pdf_path = pdf_padrao
        self.linhas = []

        # Estilo QSS
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Layout principal da janela
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        # Área de rolagem que vai conter TUDO
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout_principal.addWidget(self.scroll_area)

        # Widget interno da scroll area
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout()  # Toda interface vai aqui
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_widget)

        # Adiciona os widgets normalmente nesse novo layout
        self.build_interface()

    def build_interface(self):
        self.setWindowTitle("Orçamento PDF Marmoraria R&M | CNPJ 32.504.738/0001-82")
        self.setWindowIcon(QIcon("pdficon.png"))
        self.setGeometry(100, 100, 800, 600)

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("logo-marmoraria.png"))
        self.logo.setScaledContents(True)
        self.logo.resize(150, 100)
        self.logo.setMaximumHeight(100)
        self.scroll_layout.addWidget(self.logo, 0, 7)

        self.label_titulo = QLabel("ORÇAMENTO")
        self.label_titulo.setObjectName("titulo")
        self.scroll_layout.addWidget(self.label_titulo, 0, 0, 1, 3)

        self.linhas_layout = QGridLayout()
        self.linhas_layout.setColumnStretch(0, 1)
        self.linhas_layout.setColumnStretch(1, 3)
        self.linhas_layout.setColumnStretch(2, 1)
        self.linhas_layout.setColumnStretch(3, 1)

        # Widget para as linhas
        self.linhas_widget = QWidget()
        self.linhas_widget.setLayout(self.linhas_layout)
        self.scroll_layout.addWidget(self.linhas_widget, 1, 0, 1, 8)

        # Três linhas iniciais
        adicionar_linhas(self, 1)
        adicionar_linhas(self, 2)
        adicionar_linhas(self, 3)

        self.btn_nova_linha = QPushButton("ADICIONAR NOVA LINHA")
        self.btn_nova_linha.clicked.connect(lambda: adicionar_linhas(self, len(self.linhas) + 1))
        self.scroll_layout.addWidget(self.btn_nova_linha, 2, 0, 1, 8)

        # Restante da interface...
        self.label_total_prazo = QLabel("TOTAL A PRAZO")
        self.scroll_layout.addWidget(self.label_total_prazo, 3, 0)
        self.input_total_prazo = QLabel("0,00")
        self.scroll_layout.addWidget(self.input_total_prazo, 3, 1)

        self.label_desconto = QLabel("DESCONTO P/ PAG. A VISTA")
        self.scroll_layout.addWidget(self.label_desconto, 3, 3)
        self.desconto = QComboBox()
        self.desconto.addItems(["5%", "7%", "10%"])
        self.scroll_layout.addWidget(self.desconto, 3, 4)

        self.label_total_vista = QLabel("TOTAL A VISTA")
        self.scroll_layout.addWidget(self.label_total_vista, 3, 5)
        self.input_total_vista = QLineEdit()
        self.scroll_layout.addWidget(self.input_total_vista, 3, 6)

        self.label_obs = QLabel("OBSERVAÇÕES")
        self.scroll_layout.addWidget(self.label_obs, 4, 0, 1, 2)
        self.input_obs = QTextEdit("Qualquer alteração que necessite de adequação, será cobrado a parte")
        self.scroll_layout.addWidget(self.input_obs, 5, 0, 1, 8)

        self.btn_proxima_pagina = QPushButton("IR PARA PRÓXIMA PÁGINA")
        self.scroll_layout.addWidget(self.btn_proxima_pagina, 6, 0, 1, 2)

        self.btn_selecionar = QPushButton("SELECIONAR OUTRO PDF")
        self.btn_selecionar.clicked.connect(lambda: selecionar_pdf(self))
        self.scroll_layout.addWidget(self.btn_selecionar, 6, 2, 1, 2)

        self.input_nome_cliente = QLineEdit("NOME DO CLIENTE")
        self.scroll_layout.addWidget(self.input_nome_cliente, 6, 4, 1, 2)

        self.btn_preencher = QPushButton("PREENCHER PDF")
        self.btn_preencher.clicked.connect(lambda: enviar_dados(self))
        self.scroll_layout.addWidget(self.btn_preencher, 6, 6, 1, 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreencherPDFApp()
    window.show()
    sys.exit(app.exec())
