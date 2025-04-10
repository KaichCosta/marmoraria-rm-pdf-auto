from PyQt6.QtWidgets import QTextEdit, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf, atualizar_posicoes
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt



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

from PyQt6.QtGui import QTextCursor

def processar_texto(entry, max_linhas=2, max_chars_por_linha=45, ajustar_altura_flag=False):
    
    if isinstance(entry, QTextEdit):
        texto = entry.toPlainText().upper()  # Transforma em maiúsculo
        linhas = texto.split("\n")  # Divide o texto em linhas
        novas_linhas = []

        for linha in linhas:
            # Divide linhas excedentes
            while len(linha) > max_chars_por_linha:
                novas_linhas.append(linha[:max_chars_por_linha])
                linha = linha[max_chars_por_linha:]
            novas_linhas.append(linha)
            if len(novas_linhas) >= max_linhas:
                break

        # Junta o texto limitado
        texto_limitado = "\n".join(novas_linhas[:max_linhas])
        entry.blockSignals(True)
        entry.setPlainText(texto_limitado)

        # Ajusta o cursor para o final
        cursor = entry.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        entry.setTextCursor(cursor)

        # Ajusta a altura do QTextEdit, se necessário
        if ajustar_altura_flag:
            ajustar_altura(entry)
        entry.blockSignals(False)

    elif isinstance(entry, QLineEdit):
        texto = entry.text().upper()[:max_chars_por_linha]  # Transforma em maiúsculo e limita caracteres
        entry.blockSignals(True)
        entry.setText(texto)
        entry.blockSignals(False)

def ajustar_altura(entry):

    linhas = entry.toPlainText().split("\n")
    altura_por_linha = 30  # Altura em pixels por linha
    altura_minima = 30  # Altura inicial mínima

    nova_altura = max(altura_minima, len(linhas) * altura_por_linha)
    entry.setFixedHeight(nova_altura)

def adicionar_linhas(app, linha_num, y=None):
    entry_loc = QTextEdit()
    entry_loc.setPlaceholderText("LOCAL")
    entry_loc.setObjectName("entry_loc")
    entry_loc.setFixedHeight(30)  # Altura inicial mínima
    entry_loc.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    entry_loc.textChanged.connect(lambda: processar_texto(entry_loc, max_linhas=2, max_chars_por_linha=12, ajustar_altura_flag=True))

    entry_desc = QTextEdit()
    entry_desc.setPlaceholderText("DESCRIÇÃO")
    entry_desc.setObjectName("entry_desc")
    entry_desc.setFixedHeight(30)  # Altura inicial mínima
    entry_desc.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    entry_desc.textChanged.connect(lambda: processar_texto(entry_desc, max_linhas=2, max_chars_por_linha=45, ajustar_altura_flag=True))

    entry_qtd = QLineEdit()
    entry_qtd.setPlaceholderText("QUANTIDADE")
    entry_qtd.setObjectName("entry_qtd")
    entry_qtd.setMaximumWidth(75)
    entry_qtd.setMaxLength(6)
    entry_qtd.textChanged.connect(lambda: processar_texto(entry_qtd, max_linhas=1, max_chars_por_linha=6))

    entry_val = QLineEdit()
    entry_val.setPlaceholderText("VALOR")
    entry_val.setObjectName("entry_val")
    entry_val.setMaximumWidth(65)
    entry_val.setMaxLength(10)
    entry_val.textChanged.connect(lambda: processar_texto(entry_val, max_linhas=1, max_chars_por_linha=10))

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
