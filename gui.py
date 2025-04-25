from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QGridLayout, QPushButton, QLabel, QLineEdit, QComboBox
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

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Grid separado para as linhas dinâmicas
        self.linhas_layout = QGridLayout()
        self.linhas_layout.setVerticalSpacing(5)  # Remove espaçamento vertical entre linhas
        self.linhas_layout.setHorizontalSpacing(0)  # Pequeno espaçamento horizontal
        self.linhas_layout.setContentsMargins(0, 0, 0, 0)  # Remove margens extras
        self.layout.addLayout(self.linhas_layout, 1, 0, 1, 8)
    
        self.label_pdf = QLabel(".")
        self.layout.addWidget(self.label_pdf, 0, 0, 1, 2)

        self.entry_loc = QTextEdit()
        self.entry_loc.setPlaceholderText("LOCAL")
        self.entry_loc.textChanged.connect(lambda: processar_texto(self.entry_loc, 2, 24))

        self.entry_desc = QTextEdit()
        self.entry_desc.setPlaceholderText("DESCRIÇÃO")
        self.entry_desc.textChanged.connect(lambda: processar_texto(self.entry_desc, 2, 96))

        self.init_ui()  # Inicializa a interface

    def init_ui(self):
        self.setWindowTitle("Orçamento PDF Marmoraria R&M | CNPJ 32.504.738/0001-82")
        self.setWindowIcon(QIcon("pdficon.png"))
        self.setGeometry(10, 220, 750, 200)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("logo-marmoraria.png"))  # Carregar imagem
        self.logo.setScaledContents(True)  # Permite ajuste automático do tamanho
        self.logo.resize(150, 100)  # Define o tamanho (largura x altura)
        self.logo.move(664, 0)  # Posiciona no eixo

        self.label_titulo = QLabel("ORÇAMENTO")
        self.label_titulo.setObjectName("titulo")
        self.layout.addWidget(self.label_titulo, 0, 0, 1, 3)

        self.linhas_layout.setColumnStretch(0, 1)  # LOCAL menor
        self.linhas_layout.setColumnStretch(1, 3)  # DESCRIÇÃO maior
        self.linhas_layout.setColumnStretch(2, 1)  # QUANTIDADE menor
        self.linhas_layout.setColumnStretch(3, 1)  # VALOR menor

        adicionar_linhas(self, 1)
        adicionar_linhas(self, 2)
        adicionar_linhas(self, 3)

        self.btn_nova_linha = QPushButton("ADICIONAR NOVA LINHA")
        self.btn_nova_linha.clicked.connect(lambda: adicionar_linhas(self, len(self.linhas) + 1))
        self.layout.addWidget(self.btn_nova_linha, 2, 0, 1, 8) # Botão fora da grade

        # Total a prazo
        self.label_total_prazo = QLabel("TOTAL A PRAZO")
        self.layout.addWidget(self.label_total_prazo, 3, 0)
        self.input_total_prazo = QLabel("0,00")
        self.layout.addWidget(self.input_total_prazo, 3, 1)

        # Desconto
        self.label_desconto = QLabel("DESCONTO P/ PAG. A VISTA")
        self.layout.addWidget(self.label_desconto, 3, 3)
        self.desconto = QComboBox()
        self.desconto.addItems(["5%", "7%", "10%"])
        self.desconto.setObjectName("desconto")
        self.layout.addWidget(self.desconto, 3, 4)

        # Total à vista
        self.label_total_vista = QLabel("TOTAL A VISTA")
        self.layout.addWidget(self.label_total_vista, 3, 5)
        self.input_total_vista = QLineEdit()
        self.layout.addWidget(self.input_total_vista, 3, 6)

        # Observações
        self.label_obs = QLabel("OBSERVAÇÕES")
        self.layout.addWidget(self.label_obs, 4, 0, 1, 2)
        self.input_obs = QLineEdit()

        self.layout.addWidget(self.input_obs, 5, 0, 1, 8)

        # Botão Ir para próxima página
        self.btn_proxima_pagina = QPushButton("IR PARA PRÓXIMA PÁGINA")
        self.layout.addWidget(self.btn_proxima_pagina)  # Botão fora da grade

        self.btn_selecionar = QPushButton("SELECIONAR OUTRO PDF")
        self.btn_selecionar.clicked.connect(lambda: selecionar_pdf(self))
        self.layout.addWidget(self.btn_selecionar)

        self.input_nome_cliente = QLineEdit()
        self.input_nome_cliente.setPlaceholderText("NOME DO CLIENTE")
        self.layout.addWidget(self.input_nome_cliente, 6, 4, 1, 2)

        self.btn_preencher = QPushButton("PREENCHER PDF")
        self.btn_preencher.clicked.connect(lambda: enviar_dados(self))
        self.layout.addWidget(self.btn_preencher, 6, 6, 1, 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreencherPDFApp()
    window.show()
    sys.exit(app.exec())
