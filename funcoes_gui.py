from PyQt6.QtWidgets import QTextEdit, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf, atualizar_posicoes
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt

def limitar_texto(entry, max_linhas=2, max_chars_por_linha=48):
    texto = entry.toPlainText()
    linhas = texto.split("\n")  # Divide o texto nas linhas existentes
    novas_linhas = []

    for linha in linhas:
        while len(linha) > max_chars_por_linha:  # Divide linhas excedentes
            novas_linhas.append(linha[:max_chars_por_linha])
            linha = linha[max_chars_por_linha:]  # Resto da linha

        novas_linhas.append(linha)

        if len(novas_linhas) >= max_linhas:  # Limita o número de linhas
            break

    # Junta o texto limitado
    texto_limitado = "\n".join(novas_linhas[:max_linhas])

    # Bloqueia os sinais para evitar loops infinitos
    entry.blockSignals(True)
    entry.setPlainText(texto_limitado)
    
    # Ajusta o cursor para o final do texto
    cursor = entry.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    entry.setTextCursor(cursor)
    
    # Reativa os sinais
    entry.blockSignals(False)

def dividir_texto_centralizando(texto, limite):
    linhas = []
    atual = ""

    for char in texto:
        if len(atual) >= limite:
            linhas.append(atual)
            atual = ""
        atual += char

    if atual:
        linhas.append(atual)

    return linhas[:2]  # Retorna no máximo 2 linhas


def ajustar_altura(text_edit):
    doc = text_edit.document()
    doc.setTextWidth(text_edit.viewport().width())  
    text_edit.setFixedHeight(min(60, int(doc.size().height()) + 2))

def transformar_maiusculo(entry):
    cursor = entry.textCursor()
    pos = cursor.position()  # Guarda a posição do cursor
    texto = entry.toPlainText().upper()
    entry.blockSignals(True)  # Evita loops infinitos de sinal
    entry.setPlainText(texto)
    entry.blockSignals(False)
    cursor.setPosition(pos)  # Restaura a posição do cursor
    entry.setTextCursor(cursor)

def adicionar_linhas(app, linha_num, y=None):
    entry_loc = QTextEdit()
    entry_loc.setPlaceholderText("LOCAL")
    entry_loc.setObjectName("entry_loc")
    entry_loc.setFixedHeight(30)  # Altura inicial mínima
    entry_loc.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    entry_loc.textChanged.connect(lambda: limitar_texto(entry_loc, 24))
    entry_loc.textChanged.connect(lambda: transformar_maiusculo(entry_loc))

    entry_loc.textChanged.connect(lambda: ajustar_altura(entry_loc))

    entry_desc = QTextEdit()
    entry_desc.setPlaceholderText("DESCRIÇÃO")
    entry_desc.setObjectName("entry_desc")
    entry_desc.setFixedHeight(30)  # Altura inicial mínima
    entry_desc.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    entry_desc.textChanged.connect(lambda: limitar_texto(entry_desc, 96))
    entry_desc.textChanged.connect(lambda: transformar_maiusculo(entry_desc))

    entry_desc.textChanged.connect(lambda: ajustar_altura(entry_desc))

    entry_qtd = QLineEdit()
    entry_qtd.setPlaceholderText("QUANTIDADE")
    entry_qtd.setObjectName("entry_qtd")
    entry_qtd.setMaximumWidth(75)
    entry_qtd.setMaxLength(6)
    entry_qtd.textChanged.connect(lambda: limitar_texto(entry_qtd, 6))    

    entry_val = QLineEdit()
    entry_val.setPlaceholderText("VALOR")
    entry_val.setObjectName("entry_val")
    entry_val.setMaximumWidth(65)
    entry_val.setMaxLength(10)
    entry_val.textChanged.connect(lambda: limitar_texto(entry_val, 10))

    # Adicionando os widgets ao grid, garantindo alinhamento
    app.linhas_layout.addWidget(entry_loc, linha_num, 0)
    app.linhas_layout.addWidget(entry_desc, linha_num, 1)
    app.linhas_layout.addWidget(entry_qtd, linha_num, 2)
    app.linhas_layout.addWidget(entry_val, linha_num, 3)

    # Incrementa o contador de linhas
    app.contador += 1

    # Salva os widgets na lista para referência futura
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
        f"loc{linha_num}": 60.967,
        f"desc{linha_num}": 275.8064,
        f"qtd{linha_num}": 473.535,
        f"val{linha_num}": 542.55,
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
        loc = linha["loc"].toPlainText() or " "
        desc = linha["desc"].toPlainText() or " "
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
