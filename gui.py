import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf

class PreencherPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.pdf_path = ""

    def init_ui(self):
        self.setWindowTitle("Orçamento PDF Marmoraria R&M")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label_pdf = QLabel("Nenhum PDF selecionado")
        layout.addWidget(self.label_pdf)

        self.btn_selecionar = QPushButton("Selecionar PDF")
        self.btn_selecionar.clicked.connect(self.selecionar_pdf)
        layout.addWidget(self.btn_selecionar)

        self.entry_loc1 = QLineEdit()
        self.entry_loc1.setPlaceholderText("LOCAL")
        layout.addWidget(self.entry_loc1)

        self.entry_desc1 = QLineEdit()
        self.entry_desc1.setPlaceholderText("DESCRIÇÃO")
        layout.addWidget(self.entry_desc1)  

        self.entry_qtd1 = QLineEdit()
        self.entry_qtd1.setPlaceholderText("QUANTIDADE")
        layout.addWidget(self.entry_qtd1)

        self.entry_val1 = QLineEdit()
        self.entry_val1.setPlaceholderText("VALOR")
        layout.addWidget(self.entry_val1)

        self.btn_preencher = QPushButton("Preencher PDF")
        self.btn_preencher.clicked.connect(self.preencher_pdf)
        layout.addWidget(self.btn_preencher)

        self.setLayout(layout)

    def selecionar_pdf(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecionar PDF", "", "Arquivos PDF (*.pdf)")
        if file_path:
            self.pdf_path = file_path
            self.label_pdf.setText(f"Selecionado: {file_path}")

    def enviar_dados(self):
        if not self.pdf_path:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um PDF primeiro.")
            return

        # Capturando os dados da interface
        #Linha 1
        dados = {
            "loc1": self.entry_loc1.text(),
            "desc1": self.entry_desc1.text(),
            "qtd1": self.entry_qtd1.text(),
            "val1": self.entry_val1.text()
        }

        novo_pdf = preencher_pdf(self.pdf_path, dados)

        QMessageBox.information(self, "Sucesso", f"PDF salvo como: {novo_pdf}")