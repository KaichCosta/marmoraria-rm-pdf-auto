from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf, atualizar_posicoes

def limitar_texto(entry, limite):
    #Impede que o usuário digite mais caracteres do que o limite
    texto = entry.text()
    if len(texto) > limite:
        entry.setText(texto[:limite])

def dividir_texto_centralizando(texto, limite=34):
    if len(texto) <= limite:
        return [texto]
    linhas = [texto[:limite], texto[limite:2*limite].strip()]
    return linhas

def adicionar_linhas(app, linha_num, y=None):
    linha = QHBoxLayout()
    entry_loc = QLineEdit()
    entry_loc.setPlaceholderText("LOCAL")
    entry_loc.setMaxLength(24)
    entry_loc.textChanged.connect(lambda: limitar_texto(entry_loc, 24))
    linha.addWidget(entry_loc)

    entry_desc = QLineEdit()
    entry_desc.setPlaceholderText("DESCRIÇÃO")
    entry_desc.setMaxLength(96)
    entry_desc.textChanged.connect(lambda: limitar_texto(entry_desc, 96))
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
        f"loc{linha_num}": 60.967,#65.15
        f"desc{linha_num}": 275.8064,#
        f"qtd{linha_num}": 473.535,#445.5
        f"val{linha_num}": 542.55,#531
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

        #Dividir em 2 linhas o conteúdo
        y_base = 293
        y_espaco = 30  # Espaço entre cada item na tabela
        y_centro = y_base + (i - 1) * y_espaco  # Define a posição central de cada item

        linhas_loc = dividir_texto_centralizando(loc, 12)  # Divide os caracteres de local em partes de até 15 caracteres)

        if len(linhas_loc) == 1:
            y_linha1 = y_centro  # Mantém no centro do retângulo
            atualizar_posicoes(f"loc{i}_1", 60.967, y_linha1)
            dados[f"loc{i}_1"] = linhas_loc[0]
        else:
            y_linha1 = y_centro - 6  # Primeira linha sobe um pouco
            y_linha2 = y_centro + 6  # Segunda linha desce um pouco
            atualizar_posicoes(f"loc{i}_1", 60.967, y_linha1)
            atualizar_posicoes(f"loc{i}_2", 60.967, y_linha2)
            dados[f"loc{i}_1"] = linhas_loc[0]
            dados[f"loc{i}_2"] = linhas_loc[1]

        linhas_desc = dividir_texto_centralizando(desc, 45)  # Divide a descrição em partes de até 34 caracteres

        if len(linhas_desc) == 1:
            y_linha1 = y_centro  # Mantém no centro do retângulo
            atualizar_posicoes(f"desc{i}_1", 275.8064, y_linha1)
            dados[f"desc{i}_1"] = linhas_desc[0]
        else:
            y_linha1 = y_centro - 6  # Primeira linha sobe um pouco
            y_linha2 = y_centro + 6  # Segunda linha desce um pouco
            atualizar_posicoes(f"desc{i}_1", 275.8064, y_linha1)
            atualizar_posicoes(f"desc{i}_2", 275.8064, y_linha2)
            dados[f"desc{i}_1"] = linhas_desc[0]
            dados[f"desc{i}_2"] = linhas_desc[1]

        #Ajusta a posição das colunas de quantidade e valor
        atualizar_posicoes(f"qtd{i}", 473.535, y_centro)
        atualizar_posicoes(f"val{i}", 542.55, y_centro)
        dados[f"qtd{i}"] = qtd
        dados[f"val{i}"] = val

    print(dados)
    novo_pdf = preencher_pdf(self.pdf_path, dados)
    if novo_pdf:
        QMessageBox.information(self, "Sucesso", f"PDF salvo como: {novo_pdf}")
