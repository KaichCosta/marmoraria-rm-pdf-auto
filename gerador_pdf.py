import fitz
def selecionar_pdf(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecionar PDF", "", "Arquivos PDF (*.pdf)")
        if file_path:
            self.pdf_path = file_path
            self.label_pdf.setText(f"Selecionado: {file_path}")

    def preencher_pdf(self):
        if not self.pdf_path:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um PDF primeiro.")
            return

        # Capturando os dados da interface
        #Linha 1
        loc1 = self.entry_loc1.text()
        desc1 = self.entry_desc1.text()
        qtd1 = self.entry_qtd1.text()
        val1 = self.entry_val1.text()

        # Abrindo o PDF
        doc = fitz.open(self.pdf_path)
        page = doc[7]  # Oitava página do PDF

        # Configuração da fonte
        fonte_size = 11.5
        fonte = fitz.Font("helv")  # Helvetica padrão  
        # Função para centralizar texto
def centralizar_texto(x_centro, y, texto):
    largura_texto = fonte.text_length(texto, fontsize=fonte_size)
    x_novo = x_centro - (largura_texto / 2)
    return x_novo, y

# Posicionamento centralizado
x_loc1, y_loc1 = centralizar_texto(65.15, 293, loc1)
x_desc1, y_desc1 = centralizar_texto(260.5, 293, desc1)
x_qtd1, y_qtd1 = centralizar_texto(448.5, 293, qtd1)
x_val1, y_val1 = centralizar_texto(531, 293, val1)

# Adicionando texto em posições específicas
page.insert_text((x_loc1, y_loc1), loc1, fontsize=fonte_size, fontname="helv", color=(0, 0, 0))
page.insert_text((x_desc1, y_desc1), desc1, fontsize=fonte_size, fontname="helv", color=(0, 0, 0))
page.insert_text((x_qtd1, y_qtd1), qtd1, fontsize=fonte_size, fontname="helv", color=(0, 0, 0))
page.insert_text((x_val1, y_val1), val1, fontsize=fonte_size, fontname="helv", color=(0, 0, 0))