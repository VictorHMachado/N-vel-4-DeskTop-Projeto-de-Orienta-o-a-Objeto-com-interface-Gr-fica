import sqlite3

DB_FILE = 'dados_simulador.db'


def inicializador_banco():

    with sqlite3.connect(DB_FILE) as conexao:

        cursor = conexao.cursor()

        #cursor.execute("DROP TABLE IF EXISTS historico_partidas")
        cursor.execute("CREATE TABLE IF NOT EXISTS jogadores(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL UNIQUE, dinheiro INTEGER NOT NULL, vitorias INTEGER DEFAULT 0)")

        cursor.execute("CREATE TABLE IF NOT EXISTS historico_partidas(id INTEGER PRIMARY KEY AUTOINCREMENT, vencedor TEXT NOT NULL, regra TEXT NOT NULL, pote INTEGER NOT NULL, data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP )")



def carregar_criar_jogador(nome_jogador: str):

    dinheiro_inicial = 100

    with sqlite3.connect(DB_FILE) as conexao:
        cursor = conexao.cursor()


        cursor.execute("SELECT dinheiro FROM jogadores WHERE nome = ?", (nome_jogador,))
        resultado = cursor.fetchone()

        if resultado:
            dinheiro_salvo = resultado[0]
            print(f"JOGADOR ENCONTRADO!! CARREGANDO JOGADOR {nome_jogador} (R$ {dinheiro_salvo})")

            if dinheiro_salvo <= 0:
                
                cursor.execute("UPDATE jogadores SET dinheiro = ? WHERE nome = ?", (dinheiro_inicial, nome_jogador))

                print(f"Dinheiro de {nome_jogador} reajustado para 100")

                conexao.commit()
                
                return dinheiro_inicial
                
                
            return dinheiro_salvo
        
        else:
            print(f"CRIANDO NOVO JOGADOR... {nome_jogador} (R$ {dinheiro_inicial})")
            cursor.execute("INSERT INTO jogadores (nome, dinheiro) VALUES(?, ?)", (nome_jogador, dinheiro_inicial))
            return dinheiro_inicial

def salvar_progresso(nome_jogador, dinhero_novo):

    with sqlite3.connect(DB_FILE) as conexao:
        cursor = conexao.cursor()

        cursor.execute("UPDATE jogadores SET dinheiro =  ?  WHERE nome = ?", (dinhero_novo, nome_jogador))

def ranking(limite: int = 5):

    with sqlite3.connect(DB_FILE) as conexao:
        cursor = conexao.cursor()

        cursor.execute("SELECT nome, dinheiro, vitorias FROM jogadores ORDER BY dinheiro DESC LIMIT ?", (limite,))
        return cursor.fetchall()

def vencedor(nome_jogador):
    with sqlite3.connect(DB_FILE) as conexao:
        cursor = conexao.cursor()

        cursor.execute("UPDATE jogadores SET vitorias =  vitorias + 1  WHERE nome = ?", (nome_jogador,))



def salvar_partida(vencedor_nome, regra_jogo, pote_total):

    with sqlite3.connect(DB_FILE) as conexao:
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO historico_partidas (vencedor, regra, pote) VALUES(?, ?, ?)", (vencedor_nome, regra_jogo, pote_total))


def verificar_nome_historico(jogador_nome):
    with sqlite3.connect(DB_FILE) as conexao:
        cursor = conexao.cursor()


        try:
            cursor.execute(
                "SELECT 1 FROM historico_partidas WHERE vencedor = ? LIMIT 1", 
                (jogador_nome,)
            )
            
            resultado = cursor.fetchone()

            if resultado:
                return 1 
            else:
                return 0 
        
        except sqlite3.OperationalError:
            return 0
        

def ler_historico(jogador_nome, limite: int = 5):

    with sqlite3.connect(DB_FILE) as conexao:
        cursor = conexao.cursor()

        if jogador_nome:
            cursor.execute("SELECT vencedor, pote, regra, data_hora FROM historico_partidas  WHERE vencedor = ? ORDER BY id DESC LIMIT ?", (jogador_nome, limite))
            resultado = cursor.fetchall()
            if resultado:
                return resultado
            

        cursor.execute("SELECT vencedor, pote, regra, data_hora FROM historico_partidas ORDER BY id DESC LIMIT ?", (limite,))

        return cursor.fetchall()



