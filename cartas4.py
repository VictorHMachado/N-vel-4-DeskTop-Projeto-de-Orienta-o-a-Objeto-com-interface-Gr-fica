import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


import random 
from abc import ABC, abstractmethod
from typing import List
 

class WritingMixin:
    def specil_writing(self, widget, texto, delay=25):

        def proxima_letra(indice=0):
            if indice < len(texto):
                
                widget.insert("end", texto[indice])
                
                widget.see("end")
                
                self.after(delay, proxima_letra, indice + 1)
        
        
        proxima_letra()

import dados_cartas4 as db

def emoji(naipe: str):
        if naipe == "Ouros": return "♦" #"♦️"
        elif naipe == "Espadas": return "♠" #"♠️"
        elif naipe == "Copas": return "♥"   #"♥️"
        elif naipe == "Paus": return "♣"  #"♣️"

class Carta:

    def __init__(self, valor, naipe):
        self.valor = valor  
        self.naipe = naipe  

    def get_valor_numerico(self) -> int:
        
        if self.valor == 'J': return 11
        elif self.valor == 'Q': return 12
        elif self.valor == 'K': return 13
        elif self.valor == 'A': return 14

        else: return int(self.valor)


    def __str__(self):
        return f" {self.valor} de {self.naipe} {emoji(self.naipe)} "
    

class Baralho:

    naipes = ['Copas', 'Paus', 'Ouros', 'Espadas']
    valores = ['2', '3', '4' , '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self):
        self._cartas = [Carta(valor, naipe) for valor in self.valores for naipe in self.naipes]
        # self.embaralhar

    def embaralhar(self):
        random.shuffle(self._cartas) 
        print("Baralho embaralhado")

    def dar_carta(self): 
        if self._cartas:
            return self._cartas.pop() # RETIRA UMA CARTA DA LISTA DE CARTAS E "RETURN" ELA
        return None # BARALHO VAZIO

    def __len__(self):
        if self._cartas:
            return len(self._cartas) 
        return 0 

class Jogador():

    def  __init__(self, nome, dinheiro):
        self.nome = nome
        self.mao = []
        self.pontos = 0
        self.dinheiro = dinheiro

    def receber_carta(self, nova_carta):
        self.mao.append(nova_carta)    

    def mostrar_mao(self):
        cartas_str = "| ".join(str(c) for c in self.mao)

        return f"Mão de {self.nome}: {cartas_str}"
        

    def limpar_mao(self):
        self.mao.clear()

    def __str__(self):
        return self.nome

class Sistema_Pontuacao(ABC):
    @abstractmethod
    def calcular_pontos(self, mao):
        pass
    
    @abstractmethod
    def verificar_vencedor(self, jogadores):
        pass

class Regra_Ponderada(Sistema_Pontuacao):

    pesos_naipes = {'Ouros': 1, 'Espadas': 2, 'Copas': 3, 'Paus': 4}

    def calcular_pontos(self, mao: List[Carta]):
        total = 0

        for carta in mao:
            peso = self.pesos_naipes.get(carta.naipe, 1.0)
            total += carta.get_valor_numerico() * peso

        return total

        

    def verificar_vencedor(self, jogadores: List[Jogador]) -> List[Jogador]:
        maior_pont = -9999
        vencedores = []
        log_pontos = []
        
        for jogador in jogadores:
            jogador.pontos = self.calcular_pontos(jogador.mao)
            log_pontos.append(f"{jogador.nome}: {jogador.pontos} pontos")

            if jogador.pontos > maior_pont:
                vencedores = [jogador]
                maior_pont = jogador.pontos
            elif jogador.pontos == maior_pont:
                vencedores.append(jogador)
        return vencedores, log_pontos

        
class Regra_Combate(Sistema_Pontuacao):

    pesos_naipes = {'Ouros': -1, 'Espadas': 1, 'Copas': -1, 'Paus': 1}

    def calcular_pontos(self, mao: List[Carta]):
        total = 0

        for carta in mao:
            peso = self.pesos_naipes.get(carta.naipe, 1.0)
            total += carta.get_valor_numerico() * peso

        return total


    def verificar_vencedor(self, jogadores: List[Jogador]) -> List[Jogador]:
        maior_pont = -9999
        vencedores = []
        log_pontos = []
        
        for jogador in jogadores:
            jogador.pontos = self.calcular_pontos(jogador.mao)
            log_pontos.append(f"{jogador.nome}: {jogador.pontos} pontos")

            if jogador.pontos > maior_pont:
                vencedores = [jogador]
                maior_pont = jogador.pontos
            elif jogador.pontos == maior_pont:
                vencedores.append(jogador)

        return vencedores, log_pontos

class Jogo():

    def __init__(self, lista_jogadores: List[Jogador]):
        self.baralho = Baralho()
        self.jogadores = lista_jogadores
        self.sistema_pontuacao = None
        self.aposta = 20


    def distribuir_n(self, n_cartas: int):

        for jogadores in self.jogadores:

            jogadores.dinheiro -= self.aposta

            for n in range(n_cartas):
                carta_dada = self.baralho.dar_carta()
                if carta_dada:
                    jogadores.receber_carta(carta_dada)
                else:
                    print("Baralho Sem Cartas")
                    return
                

    def liberar_maos(self):
        for jogadores in self.jogadores:
            jogadores.mostrar_mao()
            
        
            

    def limpar_maos_jogadores(self):
        for jogadores in self.jogadores:
            self.baralho._cartas += jogadores.mao
            jogadores.limpar_mao()
        
    def preparar_rodada(self):
        self.limpar_maos_jogadores()
        self.baralho.embaralhar()

            

    def calcular_resultado(self, vencedores, valor_aposta):

        dinheiro_distribuido = (len(self.jogadores) * valor_aposta)/len(vencedores)

        nomes = []

        for ganhador in vencedores:

            ganhador.dinheiro += dinheiro_distribuido
            nomes.append(ganhador.nome)

        return nomes, dinheiro_distribuido





# --- DESKTOP 4, INTERFACE GRAFICA PARA O SIMULADOR 👇 ---

class App(ctk.CTk, WritingMixin):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Cartas OO")
        self.geometry("900x650")

        self.tema = "Dark"
        
        db.inicializador_banco()
        
        self.jogo = None
        
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.menu_principal()


    def alternar_tema(self):
        if self.tema == "Dark":
            ctk.set_appearance_mode("Light")
            self.tema = "Light"

        else:
            ctk.set_appearance_mode("Dark") 
            self.tema = "Dark"

    def menu_principal(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.container, text="🃏 Configuração da Partida 🃏", font=("Arial", 24, "bold")).pack(pady=30)

        ctk.CTkLabel(self.container, text="Jogadores (separados por vírgula):").pack()
        self.entry_nomes = ctk.CTkEntry(self.container, width=400, placeholder_text="Ex: Victor,Hugo,Silvino")
        self.entry_nomes.pack(pady=5)

        ctk.CTkLabel(self.container, text="Número de Cartas por Mão:").pack(pady=(20,0))
        self.entry_cartas = ctk.CTkEntry(self.container, width=100)
        self.entry_cartas.insert(0, "5")
        self.entry_cartas.pack(pady=5)

        ctk.CTkButton(self.container, text="INICIAR JOGO", command=self.iniciar_jogo, height=50).pack(pady=40)
        
        ctk.CTkButton(self.container, text="Ver Ranking Global", fg_color="gray", command=self.mostrar_ranking).pack()

        ctk.CTkButton(self.container, text="Ver Historico de Partidas", fg_color="gray", command=self.mostrar_historico).pack()

        switch_tema = ctk.CTkSwitch(
            self.container, 
            text="Modo Claro", 
            command=self.alternar_tema
        )
        
        if self.tema == "Light":
            switch_tema.select()
            
        switch_tema.pack(pady=20)

    def iniciar_jogo(self):
        nomes_str = self.entry_nomes.get()
        if not nomes_str:
            messagebox.showerror("Erro", "Digite pelo menos um nome!")
            return

        nomes_lista = [nomes.strip() for nomes in nomes_str.split(',') if nomes.strip()]
        
        lista_obj_jogadores = []
        for nome in nomes_lista:
            dinheiro = db.carregar_criar_jogador(nome)

            if dinheiro <= 0:
                print(f"Dinheiro de {nome} reajustado para 100")

            lista_obj_jogadores.append(Jogador(nome, dinheiro))
        
        self.jogo = Jogo(lista_obj_jogadores)
        self.num_cartas_rodada = int(self.entry_cartas.get())
        

        self.mostrar_mesa() #👇



    def mostrar_mesa(self):
        for widget in self.container.winfo_children():
            widget.destroy()


        frame_top = ctk.CTkFrame(self.container)
        frame_top.pack(fill="x", pady=5)

        ctk.CTkLabel(frame_top, text="Regra:").pack(side="left", padx=10)
        self.combo_regra = ctk.CTkOptionMenu(frame_top, values=["Ponderada", "Combate"])
        self.combo_regra.pack(side="left")

        ctk.CTkLabel(frame_top, text="Valor da Aposta:").pack(side="left", padx=10)
        self.aposta_escolhida = ctk.CTkOptionMenu(frame_top, values=["20", "40", "80"])
        self.aposta_escolhida.pack(side="left")

        

        ctk.CTkButton(frame_top, text="JOGAR RODADA", command=self.jogar_rodada, fg_color="green").pack(side="right", padx=10)


        self.txt_log = ctk.CTkTextbox(self.container, width=800, height=500, font=("Consolas", 14))
        self.txt_log.pack(pady=10)
        self.txt_log.insert("end", "--- JOGO INICIADO ---\nPrepare-se para jogar!\n")

        
        ctk.CTkButton(self.container, text="Sair / Voltar", fg_color="red", command=self.menu_principal).pack(pady=10)

    def jogar_rodada(self):

        regra_nome = self.combo_regra.get()
        sistema = Regra_Ponderada() if regra_nome == "Ponderada" else Regra_Combate()
        self.jogo.sistema_pontuacao = sistema
        
        aposta = int(self.aposta_escolhida.get())


        for player in self.jogo.jogadores:
            if player.dinheiro < aposta:
                messagebox.showwarning("Fim de Jogo", f"{player.nome} faliu! O jogo acabou.")
                self.menu_principal()
                return



        self.txt_log.delete("0.0", "end")
        self.txt_log.insert("end", f"=== NOVA RODADA ({regra_nome}) - Aposta R${aposta} ===\n\n")


        self.jogo.preparar_rodada()
        self.jogo.distribuir_n(self.num_cartas_rodada)


        self.txt_log.insert("end", "--- CARTAS NA MESA ---\n")
        
        for player in self.jogo.jogadores:
            self.txt_log.insert("end", f"{player.mostrar_mao()}\n")
            
            
  

        vencedores, log_pontos = sistema.verificar_vencedor(self.jogo.jogadores)
        
        self.txt_log.insert("end", "\n--- PONTUAÇÕES ---\n")
        for linha in log_pontos:
            self.txt_log.insert("end", linha + "\n")


        nomes_venc, valor_ganho = self.jogo.calcular_resultado(vencedores, aposta)
        

        nomes_venc_str = ", ".join(nomes_venc)
        db.salvar_partida(nomes_venc_str, regra_nome, aposta * len(self.jogo.jogadores))
        for player in self.jogo.jogadores:
            db.salvar_progresso(player.nome, player.dinheiro)
            if player in vencedores:
    
                db.vencedor(player.nome)   
                


        mensagem_final =  "\n" + "="*40 + "\n"
        if len(vencedores) > 1:
            mensagem_final += f"EMPATE! Vencedores: {nomes_venc_str}\n"

        else:
            mensagem_final += f"VITORIA! Vencedor: {nomes_venc_str}\n"



        mensagem_final += f"Prêmio: R${valor_ganho:.2f}\n"
        mensagem_final += "="*40 + "\n\n"
        mensagem_final += "--- SALDOS ATUAIS ---\n"
        for jog in self.jogo.jogadores:
            mensagem_final += f"{jog.nome}: R${jog.dinheiro:.2f}\n"
            


        self.specil_writing(self.txt_log, mensagem_final)


    def mostrar_ranking(self):
        win_rank = ctk.CTkToplevel(self)
        win_rank.title("Ranking Global")
        win_rank.geometry("400x400")

        win_rank.attributes("-topmost", True)
        
        texto = ctk.CTkTextbox(win_rank, width=380, height=380)
        texto.pack(padx=10, pady=10)
        
        ranking = db.ranking(10)
        texto.insert("end", "TOP JOGADORES (Riqueza)\n\n")
        for i, item in enumerate(ranking):

            nome = item[0]
            dinheiro = item[1]
            texto.insert("end", f"{i+1}. {nome} - R${dinheiro:.2f}\n")

    
    def mostrar_historico(self):

        janela_hist = ctk.CTkToplevel(self)
        janela_hist.title("Histórico de Partidas")
        janela_hist.geometry("500x500")
        
        janela_hist.attributes("-topmost", True) 



        frame_filtro = ctk.CTkFrame(janela_hist)
        frame_filtro.pack(fill="x", padx=10, pady=10)

        entry_filtro = ctk.CTkEntry(frame_filtro, placeholder_text="Digite um nome para filtrar...")
        entry_filtro.pack(side="left", expand=True, fill="x", padx=5)


        texto_box = ctk.CTkTextbox(janela_hist, width=480, height=380)
        texto_box.pack(padx=10, pady=10)

                
        def atualizar_lista():
            nome = entry_filtro.get().strip() 
            
            texto_box.delete("0.0", "end")

            
            if db.verificar_nome_historico(nome):
                dados = db.ler_historico(nome, 10)
                texto_box.insert("end", f"--- FILTRANDO POR: {nome.upper()} ---\n\n")
            else:
                dados = db.ler_historico(None, 10)
                texto_box.insert("end", "--- HISTÓRICO GERAL (Últimas 10) ---\n\n")

            if not dados:
                texto_box.insert("end", "Nenhuma partida encontrada.\n")
                return

            for (vencedor, pote, regra, data) in dados:
                data_simples = data.split('.')[0]
                linha = f"[{data_simples}] {vencedor}\n   Modo: {regra} | Ganhou: R${pote:.2f}\n"
                texto_box.insert("end", linha)
                texto_box.insert("end", "-"*45 + "\n")


        btn_buscar = ctk.CTkButton(frame_filtro, text="Filtrar", width=80, command=atualizar_lista)
        btn_buscar.pack(side="right", padx=5)

        atualizar_lista()


if __name__ == "__main__":

    app = App()
    app.mainloop()

