from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf
pdf_padrao = "C:/Users/User/Documents/GitHub/marmoraria-rm-pdf-auto/orcamento-vazio.pdf"
class PreencherPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.pdf_path = pdf_padrao

    def init_ui(self):
        self.setWindowTitle("Orçamento PDF Marmoraria R&M")
        self.setGeometry(100, 280, 800, 200)

        layout = QVBoxLayout()

        self.label_pdf = QLabel("PDF padrão já selecionado")
        layout.addWidget(self.label_pdf)

        self.btn_selecionar = QPushButton("Selecionar outro PDF")
        self.btn_selecionar.clicked.connect(self.selecionar_pdf)
        layout.addWidget(self.btn_selecionar)
        """======================================
        ---------------INICIO LINHA 1---------------
        ======================================"""
        Linha1 = QHBoxLayout()
        self.entry_loc1 = QLineEdit()
        self.entry_loc1.setPlaceholderText("LOCAL")
        Linha1.addWidget(self.entry_loc1)

        self.entry_desc1 = QLineEdit()
        self.entry_desc1.setPlaceholderText("DESCRIÇÃO")
        Linha1.addWidget(self.entry_desc1)  

        self.entry_qtd1 = QLineEdit()
        self.entry_qtd1.setPlaceholderText("QUANTIDADE")
        Linha1.addWidget(self.entry_qtd1)

        self.entry_val1 = QLineEdit()
        self.entry_val1.setPlaceholderText("VALOR")
        Linha1.addWidget(self.entry_val1)

        layout.addLayout(Linha1)
        """======================================
        ---------------FIM LINHA 1---------------
        ======================================"""
        """======================================
        ---------------INICIO LINHA 2---------------
        ======================================"""
        Linha2 = QHBoxLayout()
        
        self.entry_loc2 = QLineEdit()
        self.entry_loc2.setPlaceholderText("LOCAL")
        Linha2.addWidget(self.entry_loc2)

        self.entry_desc2 = QLineEdit()
        self.entry_desc2.setPlaceholderText("DESCRIÇÃO")
        Linha2.addWidget(self.entry_desc2)

        self.entry_qtd2 = QLineEdit()
        self.entry_qtd2.setPlaceholderText("QUANTIDADE")
        Linha2.addWidget(self.entry_qtd2)

        self.entry_val2 = QLineEdit()
        self.entry_val2.setPlaceholderText("VALOR")
        Linha2.addWidget(self.entry_val2)

        layout.addLayout(Linha2)
        """======================================
        ---------------FIM LINHA 2---------------
        ======================================"""
        """======================================
        ---------------INICIO LINHA 3---------------
        ======================================"""
        Linha3 = QHBoxLayout()
        
        self.entry_loc3 = QLineEdit()
        self.entry_loc3.setPlaceholderText("LOCAL")
        Linha3.addWidget(self.entry_loc3)

        self.entry_desc3 = QLineEdit()
        self.entry_desc3.setPlaceholderText("DESCRIÇÃO")
        Linha3.addWidget(self.entry_desc3)

        self.entry_qtd3 = QLineEdit()
        self.entry_qtd3.setPlaceholderText("QUANTIDADE")
        Linha3.addWidget(self.entry_qtd3)

        self.entry_val3 = QLineEdit()
        self.entry_val3.setPlaceholderText("VALOR")
        Linha3.addWidget(self.entry_val3)

        layout.addLayout(Linha3)
        """======================================
        ---------------FIM LINHA 3---------------
        ======================================"""  
        self.btn_preencher = QPushButton("Preencher PDF")
        self.btn_preencher.clicked.connect(self.enviar_dados)
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
            "loc1": self.entry_loc1.text() or " ",
            "desc1": self.entry_desc1.text() or " ",
            "qtd1": self.entry_qtd1.text() or " ",
            "val1": self.entry_val1.text() or " ",
            #-------------linha 2----------------        
            "loc2": self.entry_loc2.text() or " ",
            "desc2": self.entry_desc2.text() or " ",
            "qtd2": self.entry_qtd2.text() or " ",
            "val2": self.entry_val2.text() or " ",
            #-------------linha 3----------------        
            "loc3": self.entry_loc3.text() or " ",
            "desc3": self.entry_desc3.text() or " ",
            "qtd3": self.entry_qtd3.text() or " ",
            "val3": self.entry_val3.text() or " "
        }

        novo_pdf = preencher_pdf(self.pdf_path, dados)

        QMessageBox.information(self, "Sucesso", f"PDF salvo como: {novo_pdf}")