import fitz

def centralizar_texto(x_centro, y, texto, fonte_size=11.5):
    largura_texto = fitz.get_text_length(texto, fontsize=fonte_size)
    x_centralizado = x - (largura_texto / 2)
    return x_centralizado, y

def preencher_pdf(pdf_path, dados):
#Preenche o PDF com os dados informados.
    doc = fitz.open(pdf_path)
    page = doc[7]  #Página 8 do PDF

# Posicionamento centralizado
    x_loc1, y_loc1 = centralizar_texto(65.15, 293, dados["loc1"], fonte_size=11.5)
    x_desc1, y_desc1 = centralizar_texto(260.5, 293, dados["desc1", fonte_size=11.5])
    x_qtd1, y_qtd1 = centralizar_texto(448.5, 293, dados["qtd1", fonte_size=11.5])
    x_val1, y_val1 = centralizar_texto(531, 293, dados["val1", fonte_size=11.5])

# Adicionando texto em posições específicas
    page.insert_text((x_loc1, y_loc1), dados["loc1"], fontsize=11.5, fontname="helv", color=(0, 0, 0))
    page.insert_text((x_desc1, y_desc1), dados["desc1"], fontsize=11.5, fontname="helv", color=(0, 0, 0))
    page.insert_text((x_qtd1, y_qtd1), dados["qtd1"], fontsize=11.5, fontname="helv", color=(0, 0, 0))
    page.insert_text((x_val1, y_val1), dados["val1"], fontsize=11.5, fontname="helv", color=(0, 0, 0))

    novo_caminho = pdf_path.replace(".pdf", "Orçamento.pdf")
    doc.save(novo_caminho)
    doc.close()

    return novo_caminho