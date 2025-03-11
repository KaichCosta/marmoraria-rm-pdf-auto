from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf, atualizar_posicoes

def adicionar_linhas(app, linha_num, y=None):
    linha = QHBoxLayout()
    entry_loc = QLineEdit()
    entry_loc.setPlaceholderText("LOCAL")
    entry_loc.setMaxLength(10)
    linha.addWidget(entry_loc)

    entry_desc = QLineEdit()
    entry_desc.setPlaceholderText("DESCRIÇÃO")
    entry_loc.setMaxLength(30)
    linha.addWidget(entry_desc)

    entry_qtd = QLineEdit()
    entry_qtd.setPlaceholderText("QUANTIDADE")
    entry_loc.setMaxLength(6)
    linha.addWidget(entry_qtd)

    entry_val = QLineEdit()
    entry_val.setPlaceholderText("VALOR")
    entry_loc.setMaxLength(11)
    linha.addWidget(entry_val)

    app.linhas_layout.addLayout(linha)
    # Inicializa a lista caso não exista
    app.linhas.append({
        "loc": entry_loc,
        "desc": entry_desc,
        "qtd": entry_qtd,
        "val": entry_val
    })

    y_base = 293
    y_espaco = 30
    if y is None:
        y = y_base + (linha_num - 1) * y_espaco

    campos = {
        f"loc{linha_num}": 65.15,
        f"desc{linha_num}": 260.5,
        f"qtd{linha_num}": 445.5,
        f"val{linha_num}": 531,
    }
    
    for chave, x in campos.items():
        atualizar_posicoes(chave, x, y)
        print(f"Atualizando {chave}: (x={x}, y={y})")

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

    dados = {}  # Garante que o dicionário começa vazio
    for i, linha in enumerate(self.linhas, start=1):  # Agora percorre as linhas corretamente
        loc = linha["loc"].text() or " "
        desc = linha["desc"].text() or " "
        qtd = linha["qtd"].text() or " "
        val = linha["val"].text() or " "

        dados[f"loc{i}"] = loc
        dados[f"desc{i}"] = desc
        dados[f"qtd{i}"] = qtd
        dados[f"val{i}"] = val

    print(dados)
    novo_pdf = preencher_pdf(self.pdf_path, dados)
    if novo_pdf:
        QMessageBox.information(self, "Sucesso", f"PDF salvo como: {novo_pdf}")
