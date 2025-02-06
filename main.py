import tkinter as tk
from tkinter import filedialog, messagebox
from pdfrw import PdfReader, PdfWriter, PageMerge

def preencher_pdf():
    # Seleciona o arquivo PDF
    caminho_pdf = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if not caminho_pdf:
        return
    
    # Ler o PDF
    pdf = PdfReader(caminho_pdf)
    
    # Capturar os dados da interface
    dados = {
        "campo_nome": entry_nome.get(),
        "campo_valor": entry_valor.get(),
        "campo_data": entry_data.get()
    }
    
    # Preencher os campos do PDF
    for page in pdf.pages:
        annotations = page.Annots or []
        for annotation in annotations:
            field_name = annotation.T and annotation.T[1:-1]
            if field_name in dados:
                annotation.V = f"({dados[field_name]})"
    
    # Salvar o PDF preenchido
    novo_caminho = caminho_pdf.replace(".pdf", "_preenchido.pdf")
    PdfWriter(novo_caminho, trailer=pdf).write()
    messagebox.showinfo("Sucesso", f"PDF salvo como: {novo_caminho}")

# Criando a interface gráfica
root = tk.Tk()
root.title("Preencher Orçamento PDF")

tk.Label(root, text="Nome").pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

tk.Label(root, text="Valor").pack()
entry_valor = tk.Entry(root)
entry_valor.pack()

tk.Label(root, text="Data").pack()
entry_data = tk.Entry(root)
entry_data.pack()

tk.Button(root, text="Selecionar PDF e Preencher", command=preencher_pdf).pack()

root.mainloop()
