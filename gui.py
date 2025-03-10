from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf, atualizar_posicoes, posicoes
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
        self.btn_selecionar.clicked.connect(self.selecionar_pdf)
        self.layout.addWidget(self.btn_selecionar)

        for i in range(1,4):
            #self.adicionar_linhas(self.contador)
            self.adicionar_linhas(i)

        self.btn_nova_linha = QPushButton("ADICIONAR NOVA LINHA")
        self.btn_nova_linha.clicked.connect(lambda: self.adicionar_linhas(self.contador))
        self.layout.addWidget(self.btn_nova_linha)

        self.btn_preencher = QPushButton("Preencher PDF")
        self.btn_preencher.clicked.connect(self.enviar_dados)
        self.layout.addWidget(self.btn_preencher)

        self.setLayout(self.layout)

    def adicionar_linhas(self, linha_num=None):
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

        # Inicializa a lista caso não exista
        self.linhas.append({
            "loc": entry_loc,
            "desc": entry_desc,
            "qtd": entry_qtd,
            "val": entry_val
        })

        y_base = 293
        y_espaco = 30
        y = y_base + (linha_num - 1) * y_espaco if linha_num else y_base + (self.contador - 1) * y_espaco

        campos = {
            f"loc{linha_num}": 65.15,
            f"desc{linha_num}": 260.5,
            f"qtd{linha_num}": 448.5,
            f"val{linha_num}": 531,
        }

        for chave, x in campos.items():
            atualizar_posicoes(chave, x, y)

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

        # Obter os valores dos atributos dinâmicos

        dados = {}  # Garante que o dicionário começa vazio
        for i, linha in enumerate(self.linhas, start=1):  # Agora percorre as linhas corretamente
            dados[f"loc{i}"] = linha["loc"].text() or " "
            dados[f"desc{i}"] = linha["desc"].text() or " "
            dados[f"qtd{i}"] = linha["qtd"].text() or " "
            dados[f"val{i}"] = linha["val"].text() or " "

        print(dados)
        novo_pdf = preencher_pdf(self.pdf_path, dados)
        if novo_pdf:
            QMessageBox.information(self, "Sucesso", f"PDF salvo como: {novo_pdf}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreencherPDFApp()
    window.show()
    sys.exit(app.exec())