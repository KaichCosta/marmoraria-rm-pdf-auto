from PyQt6.QtWidgets import QTextEdit, QLineEdit, QFileDialog, QMessageBox
from gerador_pdf import preencher_pdf, atualizar_posicoes
from PyQt6.QtCore import Qt   

def dividir_texto_centralizando(texto, limite):
    linhas_usuario = texto.split("\n")
    linhas_finais = []

    for linha in linhas_usuario:
        palavras = linha.strip().split()
        linha_atual = ""

        for palavra in palavras:
            if len(linha_atual + " " + palavra) <= limite:
                if linha_atual:
                    linha_atual += " " + palavra
                else:
                    linha_atual = palavra
            else:
                if linha_atual:  # só adiciona se tiver algo
                    linhas_finais.append(linha_atual)
                linha_atual = palavra

        if linha_atual:
            linhas_finais.append(linha_atual)

    # Garante pelo menos uma linha (um espaço se nada for válido)
    if not linhas_finais:
        return [" "]
    
    return linhas_finais[:2]

def ajustar_cursor(entry, texto_modificado):
    pos_original = entry.textCursor().position()

    entry.blockSignals(True)
    entry.setPlainText(texto_modificado)
    entry.blockSignals(False)

    # Cria um novo cursor depois de setar o texto
    novo_cursor = entry.textCursor()
    if pos_original > len(texto_modificado):
        pos_original = len(texto_modificado)

    novo_cursor.setPosition(pos_original)
    entry.setTextCursor(novo_cursor)

def processar_texto(entry, max_linhas=2, max_chars_por_linha=45, ajustar_altura_flag=False):    
    if isinstance(entry, QTextEdit):
        cursor = entry.textCursor()
        pos_original = cursor.position()

        texto = entry.toPlainText()
        texto_maiusculo = texto.upper()

        # Divide em linhas e aplica quebra
        linhas = texto_maiusculo.split("\n")
        novas_linhas = []

        for linha in linhas:
            while len(linha) > max_chars_por_linha:
                novas_linhas.append(linha[:max_chars_por_linha])
                linha = linha[max_chars_por_linha:]
            novas_linhas.append(linha)
            if len(novas_linhas) >= max_linhas:
                break

        texto_limitado = "\n".join(novas_linhas[:max_linhas])

        if texto_limitado != texto:
            entry.blockSignals(True)
            entry.setPlainText(texto_limitado)
            entry.blockSignals(False)

            # Restaura o cursor na posição anterior (ou o mais perto possível)
            novo_cursor = entry.textCursor()
            nova_pos = min(pos_original, len(texto_limitado))
            novo_cursor.setPosition(nova_pos)
            entry.setTextCursor(novo_cursor)

        if ajustar_altura_flag:
            ajustar_altura(entry)

    elif isinstance(entry, QLineEdit):
        texto = entry.text()
        texto_maiusculo = texto.upper()[:max_chars_por_linha]

        if texto_maiusculo != texto:
            entry.blockSignals(True)
            entry.setText(texto_maiusculo)
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
    entry_val.textChanged.connect(lambda: somar_valores_atualizar_label(app))
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

def somar_valores_atualizar_label(app):
    total = 0
    for linha in app.linhas:
        texto_val = linha["val"].text().replace(",", ".").strip()
        if not texto_val:
            continue  # Campo vazio, ignora
        try:
            val = float(linha["val"].text().replace(",", "."))
            total += val
        except ValueError:
            if any(c.isdigit() for c in texto_val):  # Se digitou algo estranho tipo "1a", aí sim avisa
                print(f"O valor '{linha['val'].text()}' é inválido")

    app.input_total_prazo.setText(f"Total: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
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
        loc_raw = linha["loc"].toPlainText() or " "
        loc = loc_raw.strip()

        desc_raw = linha["desc"].toPlainText() or " "
        desc = desc_raw.strip() 

        qtd = linha["qtd"].text() or " "
        val = linha["val"].text() or " "

        #Dividir em 2 linhas o conteúdo
        y_base = 293
        y_espaco = 30  # Espaço entre cada item na tabela
        y_centro = y_base + (i - 1) * y_espaco  # Define a posição central de cada item

        linhas_loc = dividir_texto_centralizando(loc, 12)  # Divide os caracteres de local em 2 partes de até 12 caracteres)

        if linhas_loc:
            if len(linhas_loc) == 1:
                y_linha1 = y_centro
                atualizar_posicoes(f"loc{i}_1", 60.967, y_linha1)
                dados[f"loc{i}_1"] = linhas_loc[0]
            else:
                espaco_linha = 10.5
                y_linha1 = y_centro - espaco_linha / 2
                y_linha2 = y_centro + espaco_linha / 2
                atualizar_posicoes(f"loc{i}_1", 60.967, y_linha1)
                atualizar_posicoes(f"loc{i}_2", 60.967, y_linha2)
                dados[f"loc{i}_1"] = linhas_loc[0]
                dados[f"loc{i}_2"] = linhas_loc[1]
        else:
            atualizar_posicoes(f"loc{i}_1", 60.967, y_centro)
            dados[f"loc{i}_1"] = " "


        linhas_desc = dividir_texto_centralizando(desc, 45)  # Divide a descrição em partes de até 34 caracteres

        if linhas_desc:
            if len(linhas_desc) == 1:
                y_linha1 = y_centro  # Mantém no centro do retângulo
                atualizar_posicoes(f"desc{i}_1", 275.8064, y_linha1)
                dados[f"desc{i}_1"] = linhas_desc[0]
            else:
                espaco_linha = 14  # espaço entre linhas
                y_linha1 = y_centro - espaco_linha / 2
                y_linha2 = y_centro + espaco_linha / 2
                atualizar_posicoes(f"desc{i}_1", 275.8064, y_linha1)
                atualizar_posicoes(f"desc{i}_2", 275.8064, y_linha2)
                dados[f"desc{i}_1"] = linhas_desc[0]
                dados[f"desc{i}_2"] = linhas_desc[1]
        else:
            atualizar_posicoes(f"desc{i}_1", 275.8064, y_centro)
            dados[f"loc{i}_1"] = " "

        #Ajusta a posição das colunas de quantidade e valor
        atualizar_posicoes(f"qtd{i}", 473.535, y_centro)
        atualizar_posicoes(f"val{i}", 542.55, y_centro)
        dados[f"qtd{i}"] = qtd
        dados[f"val{i}"] = val

    print(dados)
    print(f"Linha {i} - loc: {linhas_loc}")  # ← deve mostrar 1 ou 2 linhas

    doc = preencher_pdf(self.pdf_path, dados)
    if doc:
        novo_pdf = self.pdf_path.replace(".pdf", " Orçamento.pdf")
        doc.save(novo_pdf)
        doc.close()
        QMessageBox.information(self, "Sucesso", f"PDF salvo como: {novo_pdf}")
    else:
        QMessageBox.warning(self, "Erro", "Ocorreu um erro ao preencher o PDF.")
