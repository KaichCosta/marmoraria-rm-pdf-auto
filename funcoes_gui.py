from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf, atualizar_posicoes

def limitar_texto(entry, limite):
    #Impede que o usuário digite mais caracteres do que o limite
    texto = entry.text()
    if len(texto) > limite:
        entry.setText(texto[:limite])

def dividir_texto(texto, limite):
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 <= limite:
            linha_atual += " " + palavra if linha_atual else palavra
        else:
            linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)
    return linhas   
def adicionar_linhas(app, linha_num, y=None):
    linha = QHBoxLayout()
    entry_loc = QLineEdit()
    entry_loc.setPlaceholderText("LOCAL")
    entry_loc.setMaxLength(12)
    entry_loc.textChanged.connect(lambda: limitar_texto(entry_loc, 12))
    linha.addWidget(entry_loc)

    entry_desc = QLineEdit()
    entry_desc.setPlaceholderText("DESCRIÇÃO")
    #entry_desc.setMaxLength(34)
    #entry_desc.textChanged.connect(lambda: limitar_texto(entry_desc, 34))
    linha.addWidget(entry_desc)

    entry_qtd = QLineEdit()
    entry_qtd.setPlaceholderText("QUANTIDADE")
    entry_qtd.setMaxLength(6)
    entry_qtd.textChanged.connect(lambda: limitar_texto(entry_qtd, 6))    
    linha.addWidget(entry_qtd)

    entry_val = QLineEdit()
    entry_val.setPlaceholderText("VALOR")
    entry_val.setMaxLength(10)
    entry_val.textChanged.connect(lambda: limitar_texto(entry_val, 10))
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
        f"desc{linha_num}": 261,
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

        linhas_desc = dividir_texto(desc, 34)  # Divide a descrição em partes de até 30 caracteres
        y_atual = 293 + (i - 1) * 34  # Guarda a posição inicial Y
        desc_index = i  # Novo contador para as linhas da descrição

        for linha in linhas_desc:
            dados[f"desc{i}"] = linha
            atualizar_posicoes(f"desc{i}", 260.5, y_atual)
            y_atual += 12  # Move para a próxima linha
            desc_index += 1  # Incrementa o índice para a próxima linha

        dados[f"qtd{i}"] = qtd
        dados[f"val{i}"] = val

    print(dados)
    novo_pdf = preencher_pdf(self.pdf_path, dados)
    if novo_pdf:
        QMessageBox.information(self, "Sucesso", f"PDF salvo como: {novo_pdf}")
