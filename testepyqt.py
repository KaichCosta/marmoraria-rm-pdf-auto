#antigo enviar dados 
def enviar_dados(self):
        if not self.pdf_path:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um PDF primeiro.")
            return

        # Capturando os dados da interface
        #Linha 1
'''     dados = {
            f"loc{i}": getattr(self, f'entry_loc{i}').text() or " " for i in range(1, self.contador)
        }
        dados.update({
            f"desc{i}": getattr(self, f'entry_desc{i}').text() or " " for i in range(1, self.contador)
        })
        dados.update({
            f"qtd{i}": getattr(self, f'entry_qtd{i}').text() or " " for i in range(1, self.contador)
        })
        dados.update({
            f"val{i}": getattr(self, f'entry_val{i}').text() or " " for i in range(1, self.contador)
        })
'''
