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

""" #Posicionamento X, Y dos centralizamentos
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
        }"""


#era do gui.py 
"""        chave_loc = f"loc{self.contador}"
        chave_desc = f"desc{self.contador}"
        chave_qtd = f"qtd{self.contador}"
        chave_val = f"val{self.contador}"

        atualizar_posicoes(chave_loc, self.contador)
        atualizar_posicoes(chave_desc, self.contador)
        atualizar_posicoes(chave_qtd, self.contador)
        atualizar_posicoes(chave_val, self.contador)

        self.contador += 1
"""