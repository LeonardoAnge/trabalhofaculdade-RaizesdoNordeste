import sqlite3
from models import CRIAR_TABELA_USUARIOS, CRIAR_TABELA_UNIDADE, CRIAR_TABELA_CARDAPIO, CRIAR_TABELA_ESTOQUE,CRIAR_TABELA_PEDIDOS, CRIAR_TABELA_ITENS_PEDIDO

class BackEnd:
    def conecta_db(self): #Conectar ao banco de dados
        self.conn = sqlite3.connect("Sistema_cadastros.db")
        self.cursor = self.conn.cursor()

    def desconecta_db(self): #Desconectar do banco
        self.conn.close()

    def cria_tabela(self): #criação das tabelas no banco
        self.conecta_db()

        self.cursor.execute("PRAGMA foreign_keys = ON;") # para habilitar o foreign key
        #criação de tabelas, q foram puxazdas do models
        self.cursor.execute(CRIAR_TABELA_USUARIOS)
        self.cursor.execute(CRIAR_TABELA_UNIDADE)
        self.cursor.execute(CRIAR_TABELA_CARDAPIO)
        self.cursor.execute(CRIAR_TABELA_ESTOQUE)
        self.cursor.execute(CRIAR_TABELA_PEDIDOS)
        self.cursor.execute(CRIAR_TABELA_ITENS_PEDIDO)

        self.conn.commit() #Salvar no Banco de dados
        self.desconecta_db() 
            
            
