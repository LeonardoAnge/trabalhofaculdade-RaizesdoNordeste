CRIAR_TABELA_USUARIOS ="""
            CREATE TABLE IF NOT EXISTS Usuarios(
            Telefone TEXT PRIMARY KEY,
            Nome TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            CPF TEXT NOT NULL UNIQUE,
            Data_de_Nascimento TEXT NOT NULL,
            Senha_hash TEXT NOT NULL,
            Cargo TEXT NOT NULL)
        """
CRIAR_TABELA_UNIDADE = """
            CREATE TABLE IF NOT EXISTS Unidade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Gerente TEXT NOT NULL UNIQUE,
            FOREIGN KEY (Gerente) REFERENCES Usuarios(Telefone))
        """
CRIAR_TABELA_CARDAPIO ="""
            CREATE TABLE IF NOT EXISTS Cardapio(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Prato TEXT COLLATE NOCASE UNIQUE NOT NULL,
            Preco REAL NOT NULL,
            Ativo INTEGER NOT NULL DEFAULT 1)
        """
CRIAR_TABELA_ESTOQUE ="""
            CREATE TABLE IF NOT EXISTS Estoque(
            Unidade_id INTEGER NOT NULL,
            Cardapio_id INTEGER NOT NULL,
            Quantidade INT NOT NULL,
            PRIMARY KEY (Unidade_id, Cardapio_id),
            FOREIGN KEY (Unidade_id) REFERENCES Unidade(id),
            FOREIGN KEY (Cardapio_id) REFERENCES Cardapio(id))
        """
CRIAR_TABELA_PEDIDOS = """
            CREATE TABLE IF NOT EXISTS Pedidos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Unidade_id INTEGER NOT NULL,
            Canal TEXT NOT NULL,
            Cliente_telefone TEXT NOT NULL,
            Forma_pagamento TEXT NOT NULL,
            Total REAL NOT NULL,
            Status_pagamento TEXT NOT NULL,
            Status_pedido TEXT NOT NULL,
            FOREIGN KEY (Unidade_id) REFERENCES Unidade(id),
            FOREIGN KEY (Cliente_telefone) REFERENCES Usuarios (Telefone)
            )
"""
CRIAR_TABELA_ITENS_PEDIDO = """
            CREATE TABLE IF NOT EXISTS ItensPedido(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Pedido_id INT NOT NULL,
            Cardapio_id INT NOT NULL,
            Quantidade INT NOT NULL,
            FOREIGN KEY (Pedido_id) REFERENCES Pedidos (id),
            FOREIGN KEY (Cardapio_id) REFERENCES Cardapio (id)) 
"""