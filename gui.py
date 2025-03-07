from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf, atualizar_posicoes, posicoes
import sys 
pdf_padrao = "C:/Users/User/Documents/GitHub/marmoraria-rm-pdf-auto/orcamento-vazio.pdf"
dados = {}

class PreencherPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.pdf_path = pdf_padrao
        self.contador = 4


    def init_ui(self):
        self.setWindowTitle("Orçamento PDF Marmoraria R&M")
        self.setGeometry(100, 280, 800, 200)

        self.layout = QVBoxLayout()

        self.label_pdf = QLabel("PDF padrão já selecionado")
        self.layout.addWidget(self.label_pdf)

        self.btn_selecionar = QPushButton("Selecionar outro PDF")
        self.btn_selecionar.clicked.connect(self.selecionar_pdf)
        self.layout.addWidget(self.btn_selecionar)

        self.adicionar_linha_inicial(1)
        self.adicionar_linha_inicial(2)
        self.adicionar_linha_inicial(3)

        self.btn_nova_linha = QPushButton("ADICIONAR NOVA LINHA")
        self.btn_nova_linha.clicked.connect(self.novos_campos)
        self.layout.addWidget(self.btn_nova_linha)

        self.btn_preencher = QPushButton("Preencher PDF")
        self.btn_preencher.clicked.connect(self.enviar_dados)
        self.layout.addWidget(self.btn_preencher)

        self.setLayout(self.layout)

        """======================================
        ---------------INICIO LINHA 1---------------
        ======================================"""
    def adicionar_linha_inicial(self, linha_num):
        linha = QHBoxLayout()
        entry_loc = QLineEdit()
        entry_loc.setPlaceholderText("LOCAL")
        linha.addWidget(entry_loc)

        entry_desc = QLineEdit()
        entry_desc.setPlaceholderText("DESCRIÇÃO")
        linha.addWidget(entry_desc)

        entry_qtd = QLineEdit()
        entry_qtd.setPlaceholderText("QUANTIDADE")
        linha.addWidget(entry_qtd)

        entry_val = QLineEdit()
        entry_val.setPlaceholderText("VALOR")
        linha.addWidget(entry_val)

        self.layout.addLayout(linha)

        # Dicionário JA COMEÇA com esses dados
        setattr(self, f'entry_loc{linha_num}', entry_loc)
        setattr(self, f'entry_desc{linha_num}', entry_desc)
        setattr(self, f'entry_qtd{linha_num}', entry_qtd)
        setattr(self, f'entry_val{linha_num}', entry_val)

    def novos_campos(self):
        linha = QHBoxLayout()
        entry_loc = QLineEdit()
        entry_loc.setPlaceholderText("LOCAL")
        linha.addWidget(entry_loc)

        entry_desc = QLineEdit()
        entry_desc.setPlaceholderText("DESCRIÇÃO")
        linha.addWidget(entry_desc)

        entry_qtd = QLineEdit()
        entry_qtd.setPlaceholderText("QUANTIDADE")
        linha.addWidget(entry_qtd)

        entry_val = QLineEdit()
        entry_val.setPlaceholderText("VALOR")
        linha.addWidget(entry_val)

        self.layout.addLayout(linha)

        '''

        dados[chave_loc] = entry_loc
        dados[chave_desc] = entry_desc
        dados[chave_qtd] = entry_qtd
        dados[chave_val] = entry_val

        # Atualizar dicionário posicoes
        '''

        setattr(self, f'entry_loc{self.contador}', entry_loc)
        setattr(self, f'entry_desc{self.contador}', entry_desc)
        setattr(self, f'entry_qtd{self.contador}', entry_qtd)
        setattr(self, f'entry_val{self.contador}', entry_val)

        y_base = 293
        y_espaco = 30
        y = y_base + (self.contador - 1) * y_espaco

        atualizar_posicoes(f"loc{self.contador}", 65.15, y)
        atualizar_posicoes(f"desc{self.contador}", 260.5, y)
        atualizar_posicoes(f"qtd{self.contador}", 448.5, y)
        atualizar_posicoes(f"val{self.contador}", 531, y)

        self.contador += 1


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

        dados = {}
        for i in range(1, self.contador):
            # Obter os valores dos atributos dinâmicos
            try:
                loc = getattr(self, f'entry_loc{i}').text() or " "
                desc = getattr(self, f'entry_desc{i}').text() or " "
                qtd = getattr(self, f'entry_qtd{i}').text() or " "
                val = getattr(self, f'entry_val{i}').text() or " "
            #Adicionar ao dicionário de dados
                dados[f"loc{i}"] = loc
                dados[f"desc{i}"] = desc
                dados[f"qtd{i}"] = qtd
                dados[f"val{i}"] = val
            except AttributeError:
        # Caso alguma linha não exista, ignore
                QMessageBox.warning(self, "Erro", f"Erro ao acessar os campos da linha {i}. Verifique se os campos foram criados corretamente.")
                return
        novo_pdf = preencher_pdf(self.pdf_path, dados)

        QMessageBox.information(self, "Sucesso", f"PDF salvo como: {novo_pdf}")
