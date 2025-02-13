import fitz  # PyMuPDF

# Caminho do PDF
caminho_pdf = "pegar-eixo-xy.pdf"  # Substitua pelo caminho correto

# Abrindo o documento
doc = fitz.open(caminho_pdf)

# Pegando a primeira página (ou altere para outra se necessário)
pagina = doc[7]

# Extrair blocos de texto e suas coordenadas
texto_extraido = pagina.get_text("blocks")

# Exibir coordenadas de cada bloco de texto
for bloco in texto_extraido:
    x0, y0, x1, y1, texto, *_ = bloco  # Coordenadas e o texto
    print(f"Texto: {texto.strip()} | Coordenadas: ({x0}, {y0}) -> ({x1}, {y1})")

doc.close()
