import fitz

def centralizar_texto(x, y, texto,fonte="helv", fonte_size=11.5):
    if not texto:
        texto = " "
    largura_texto = fitz.get_text_length(texto,fontname=fonte, fontsize=fonte_size)
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
#-------------linha 2-----------
        "loc2": (65.15, 323),
        "desc2": (260.5, 323),
        "qtd2": (448.5, 323),
        "val2": (531, 323),
#-------------linha 3-----------
        "loc3": (65.15, 353),
        "desc3": (260.5, 353),
        "qtd3": (448.5, 353),
        "val3": (531, 353),
    }
    for chave, (x,y) in posicoes.items():
        x_centralizado, y_centralizado = centralizar_texto(x, y, dados[chave], fonte_size=11.5)
    # Adicionando texto em posições específicas
        page.insert_text((x_centralizado, y_centralizado), dados[chave], fontsize=11.5, fontname="helv", color=(0, 0, 0))

#novo caminho é variavel para mudar o nome do arqui, posso usar um label pra escolher o nome do cliente epor numa varialvel 'cliente' e por em 'novocaminho'
    novo_caminho = pdf_path.replace(".pdf", " Orçamento.pdf")
    doc.save(novo_caminho)
    doc.close()
    return novo_caminho
