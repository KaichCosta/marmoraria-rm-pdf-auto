import fitz
posicoes = {}

def centralizar_texto(x, y, texto,fonte="helv", fonte_size=11.5):
    if not texto:
        texto = " "
    largura_texto = fitz.get_text_length(texto,fontname=fonte, fontsize=fonte_size)
    x_centralizado = x - (largura_texto / 2)
    return x_centralizado, y

def atualizar_posicoes(chave, x, y):
    posicoes[chave] = (x, y)

def preencher_pdf(pdf_path, dados):
    doc = fitz.open(pdf_path)
    page = doc[7]  #Página 8 do PDF

    try:
        for chave, (x, y) in posicoes.items():
            if chave in dados:  # Certificar-se de que a chave existe no dicionário de dados
                texto = dados[chave]
                x_centralizado, y_centralizado = centralizar_texto(x, y, texto, fonte_size=11.5)
                # Inserir texto no PDF na posição calculada
                page.insert_text((x_centralizado, y_centralizado), texto, fontsize=11.5, fontname="helv", color=(0, 0, 0))
    
    #novo caminho é variavel para mudar o nome do arqui, posso usar um label pra escolher o nome do cliente epor numa varialvel 'cliente' e por em 'novocaminho'
        novo_caminho = pdf_path.replace(".pdf", " Orçamento.pdf")
        doc.save(novo_caminho)
        return novo_caminho
    except Exception as e:
        print(f"Erro ao preencher o PDF: {e}")
        return None
    finally:
        doc.close()
