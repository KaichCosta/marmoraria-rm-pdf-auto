import fitz  # PyMuPDF

posicoes = {}

def centralizar_texto(x, y, texto, fonte="Courier", fonte_size=12):
    if not texto:
        texto = " "
    largura_texto = fitz.get_text_length(texto, fontname=fonte, fontsize=fonte_size)
    x_centralizado = x - (largura_texto / 2)
    return x_centralizado, y

def atualizar_posicoes(chave, x, y):
    posicoes[chave] = (x, y)

def preencher_pdf(pdf_path, dados):
    doc = fitz.open(pdf_path)
    page = doc[8]  # Página 9 do PDF

    try:
        for chave, (x, y) in posicoes.items():
            if chave in dados:
                texto = dados[chave]

                # LOC e DESC podem ter duas linhas — usar textbox
                if "loc" in chave or "desc" in chave:
                    largura = 150 if "loc" in chave else 390  # largura do retângulo
                    altura = 20  # altura máxima de duas linhas
                    rect = fitz.Rect(x - largura / 2, y - altura / 2, x + largura / 2, y + altura / 2)

                    page.insert_textbox(
                        rect,
                        texto,
                        fontname="Courier",
                        fontsize=12,
                        color=(0, 0, 0),
                        align=1  # centralizado
                    )
                else:
                    # Para qtd e val (uma linha só)
                    x_centralizado, y_centralizado = centralizar_texto(x, y, texto)
                    page.insert_text((x_centralizado, y_centralizado), texto, fontsize=12, fontname="Courier", color=(0, 0, 0))

        return doc  # Retorna o objeto PDF sem salvar ainda
    except Exception as e:
        print(f"Erro ao preencher o PDF: {e}")
        return None
