import fitz
posicoes = {}

def centralizar_texto(x, y, texto, fonte="Courier", fonte_size=12):
    if not texto:
        texto = " "
    largura_texto = fitz.get_text_length(texto,fontname=fonte, fontsize=fonte_size)
    x_centralizado = x - (largura_texto / 2)
    return x_centralizado, y

def atualizar_posicoes(chave, x, y):
    posicoes[chave] = (x, y)

def preencher_pdf(pdf_path, dados):
    doc = fitz.open(pdf_path)
    page = doc[8]  #Página 9 do PDF

    try:
        for chave, (x, y) in posicoes.items():
            if chave in dados:  # Certificar-se de que a chave existe no dicionário de dados
                texto = dados[chave]
                linhas = texto.split('\n')  # Quebra manualmente

                for i, linha in enumerate(texto.splitlines()):
                    # Ajusta a posição vertical para cada linha (ex: 14px entre linhas)
                    y_linha = y + (i * 13)
                    x_centralizado, _ = centralizar_texto(x, y_linha, linha, fonte_size=12)
                    page.insert_text(
                        (x_centralizado, y_linha),
                        linha,
                        fontsize=12,
                        fontname="Courier",
                        color=(0, 0, 0),
                        render_mode=0,
                        overlay=True)

        novo_caminho = pdf_path.replace(".pdf", f" Orçamento.pdf")
        doc.save(novo_caminho)
        return novo_caminho
    except Exception as e:
        print(f"Erro ao preencher o PDF: {e}")
        return None
    finally:
        doc.close()
