import fitz

def centralizar_texto(x, y, texto, fonte_size=11.5):
    largura_texto = fitz.get_text_length(texto, fontsize=fonte_size)
    x_centralizado = x - (largura_texto / 2)
    return x_centralizado, y

def preencher_pdf(pdf_path, dados):
#Preenche o PDF com os dados informados.
    doc = fitz.open(pdf_path)
    page = doc[7]  #Página 8 do PDF
# Posicionamento X, Y dos centralizamentos
    posicoes = {
        "loc1": (65.15, 293),
        "desc1": (260.5, 293),
        "qtd1": (448.5, 293),
        "val1": (531, 293),
    }
    for chave, (x,y) in posicoes.items():
        x_centralizado, y_centralizado = centralizar_texto(x, y, dados[chave], fonte_size=11.5)
    # Adicionando texto em posições específicas
        page.insert_text((x_centralizado, y_centralizado), dados[chave], fontsize=11.5, fontname="helv", color=(0, 0, 0))

# Adicionando texto em posições específicas

    novo_caminho = pdf_path.replace(".pdf", "Orçamento.pdf")
    doc.save(novo_caminho)
    doc.close()
    return novo_caminho