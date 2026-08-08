from database import BackEnd #importação do backend no arquivo database
#importação das classes no aquivo schemas
from schemas import UsuarioCreate, UsuarioLogin, UsuarioOut, LoginOut, EstoqueBase, EstoqueOut, EstoqueCreate, CardapioCreate, CardapioOut, UnidadeOut, UnidadeCreate, PedidoCreate, PedidoUpdate, PedidoOut 
from fastapi import HTTPException #extensão do fastapi, para descrever erros.
import hashlib #Biblioteca para a criação de senhas HASH
import re #Biblioteca para remodelar os caracteres digitados.
import sqlite3 #Biblioteca do banco de dados 'SQLite3'

def salvar_cadastro(db: BackEnd, usuario: UsuarioCreate): # função salvar cadastro
        if usuario.senha != usuario.confirma_senha:# caso senha for diferente do confirmar senha, vai dar um erro.
            raise HTTPException(status_code= 400, detail= "As senha não coincidem. Digite novamente!")

        cpf_limpo = re.sub(r"\D","", usuario.cpf)#re para tirar qlqer carectere digitado que não seja numeros
        if len(cpf_limpo) != 11: #len para contabilizar os carecteres digitandos e caso for diferente de 11, returna o Raise
            raise HTTPException(status_code= 400, detail= "CPF inválido")

        senha_hash = hashlib.sha256(usuario.senha.encode("utf-8")).hexdigest() #Criação de senha HASH

        db.conecta_db()
        try:
            db.cursor.execute("""
            INSERT INTO Usuarios (Telefone, Nome, Email, CPF, Data_de_Nascimento, Senha_hash, Cargo)
            VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (usuario.telefone, usuario.nome, usuario.email, cpf_limpo, usuario.data_nascimento , senha_hash, usuario.cargo)) #inserção de dados no banco usuarios
            
            db.conn.commit()

            return UsuarioOut(telefone = usuario.telefone, nome = usuario.nome, email = usuario.email, cpf = cpf_limpo, data_nascimento= usuario.data_nascimento, cargo = usuario.cargo) # return das informações q acabou de serem salvas, onde a senha não sera salva, apenas senha_hash
        
        except sqlite3.IntegrityError: #Caso nao consiga inserir os dados por ja ter cadastrado cpf ou senha, vai dar erro
            raise HTTPException(status_code= 409, detail= "Este CPF ou Email ja está cadastrado.")
        finally:
            db.desconecta_db()

def verificar_login(db: BackEnd, usuario: UsuarioLogin):
        db.conecta_db()
        try:
            db.cursor.execute("""
            SELECT Cargo, Senha_hash, Nome FROM Usuarios WHERE email =?
            """, (usuario.email,))
            usuario_encontrado = db.cursor.fetchone() #fetchone para salvar a linha de dados que foi puxada.
            if not usuario_encontrado:
                raise HTTPException(status_code= 401, detail="E-mail ou senha inválidos.")
            #como foi puxado 3 dados, usamos o [] para identificar cada tipo de dado e damos um nome.
            cargo_banco = usuario_encontrado[0]
            hash_banco = usuario_encontrado[1]
            nome_user = usuario_encontrado[2]

            hash_digitado = hashlib.sha256(usuario.senha.encode("utf-8")).hexdigest() #senha digitada pelo usuario

            if hash_digitado == hash_banco: #caso senha digitada pelo usuario for diferente de senha do banco, vai da erro
                return LoginOut(cargo = cargo_banco, nome = nome_user,mensagem= "Login realizado com sucesso.")
                
            raise HTTPException(status_code= 401, detail="E-mail ou senha inválidos.")
        
        finally:
            db.desconecta_db()

def cadastrar_prato (db: BackEnd, produto: CardapioCreate):
    db.conecta_db()
    try:
        db.cursor.execute("""
        INSERT INTO Cardapio (Prato, Preco)
        VALUES (?, ?)
""", (produto.prato, produto.preco))
        db.conn.commit() #Commit para salvar no banco de dados
        id = db.cursor.lastrowid #lastrowid, para pegar a ultima linha de id registrada

        return CardapioOut ( id = id, prato = produto.prato, preco = produto.preco ) # return do schema CardapioOut
                
    except sqlite3.IntegrityError:
        raise HTTPException(status_code= 409, detail="Prato ja cadastrado!")
    finally:
        db.desconecta_db()

def cadastrar_produto (db: BackEnd, estoque: EstoqueCreate):
    db.conecta_db()
    try:
        db.cursor.execute("""
        INSERT INTO Estoque (Unidade_id, Cardapio_id, Quantidade)
        VALUES (?, ?, ?)
        """, (estoque.unidade_id, estoque.cardapio_id, estoque.quantidade))
        db.conn.commit()
        
        db.cursor.execute("""
            SELECT Cardapio.id, Cardapio.Prato, Cardapio.Preco, Estoque.Quantidade
            FROM Estoque
            INNER JOIN Cardapio ON Estoque.Cardapio_id = Cardapio.id
            WHERE Estoque.Unidade_id = ? AND Estoque.Cardapio_id = ?
            """, (estoque.unidade_id, estoque.cardapio_id))
            
        estoque_atualizado = db.cursor.fetchone()
        return EstoqueOut (id = estoque_atualizado [0], prato = estoque_atualizado [1], preco = estoque_atualizado[2], quantidade= estoque_atualizado [3])
                        
    except sqlite3.IntegrityError:
        raise HTTPException(status_code= 409, detail="Prato ja cadastrado!")
    finally:
        db.desconecta_db()

def criar_unidade(db: BackEnd, unidade: UnidadeCreate):
    db.conecta_db()
    try:
        db.cursor.execute("""
        SELECT Cargo FROM Usuarios
        WHERE Telefone = ?
    """, (unidade.gerente,))
        gerente = db.cursor.fetchone() #fetchone para salvar os dados
        cargo = gerente[0] #pego a variavel cargo e deu o valor gerente [0]
        if cargo != "Gerente":#apenas usuarios com cargo gerente podem ser registrados como responsavel por unidade.
            raise HTTPException(status_code= 404, detail= "Usuario selecionado nao possui o cargo 'Gerente'!")

        db.cursor.execute("""
        INSERT INTO Unidade (Nome, Gerente)
        VALUES (?, ?)
        """, (unidade.nome, unidade.gerente))
        id_unidade = db.cursor.lastrowid
        db.conn.commit()
        return UnidadeOut (id = id_unidade, nome = unidade.nome, gerente = unidade.gerente)
                    
    except sqlite3.IntegrityError:
        raise HTTPException(status_code= 409, detail="Gerente selecionado ja registrado!")
    finally:
        db.desconecta_db()

def listar_unidade(db:BackEnd):
    db.conecta_db()
    try:
        db.cursor.execute("""
        SELECT id, Nome, Gerente FROM Unidade
    """)
        unidades = db.cursor.fetchall()#fetchal para pegar todas linhas das colunas selecionadas da tabela Unidade.
        if not unidades: #caso nao tenha nenhuma unidade registrada, da erro raise.
            raise HTTPException(status_code= 404, detail= "Nenhuma unidade encontrada em nosso sistema")
    
        return [{"id": unidade [0],
                "nome" : unidade [1],
                "gerente" : unidade [2]}
                for unidade in unidades] # return dos dados da tabela para o main.
        
    except sqlite3.IntegrityError as erro:
        raise HTTPException(status_code= 500, detail= f"Erro no banco de dados: {erro}")
    
    finally:
        db.desconecta_db()

def listar_pratos(db: BackEnd, limit : int = 50, offset: int = 0): #limit para o maximo de pratos a returna e offset para pular os id.
    db.conecta_db()
    try:
        db.cursor.execute("""
        SELECT id, Prato, Preco FROM Cardapio
        LIMIT  ? 
        OFFSET  ? 
""",(limit, offset))
        pratos = db.cursor.fetchall()
        if not pratos:
            raise HTTPException(status_code= 404, detail= "Nenhum prato encontrado em nosso sistema")

        return [{"id": prato [0],
                "prato" : prato [1],
                "preco" : prato [2]}
                for prato in pratos]
    
    except sqlite3.IntegrityError as erro:
         raise HTTPException(status_code= 500, detail= f"Erro no banco de dados: {erro}")

    finally:
        db.desconecta_db()

def listar_estoque(db: BackEnd, unidade_id):
        db.conecta_db()
        try:
            db.cursor.execute("""
            SELECT Cardapio.id, Cardapio.Prato, Cardapio.Preco, Estoque.Quantidade 
            FROM Estoque
            INNER JOIN Cardapio ON Estoque.Cardapio_id = Cardapio.id
            WHERE Estoque.Unidade_id = ?
            """, (unidade_id,))    
            produtos = db.cursor.fetchall()
            if not produtos:
                raise HTTPException(status_code= 404, detail= "Nenhum produto encontrado em nossa unidade!")
            
            return [{"id": produto[0],
                    "prato": produto [1],
                    "preco":produto[2],
                     "quantidade": produto[3]}
                     for produto in produtos]
        
        except sqlite3.IntegrityError as erro:
             raise HTTPException(status_code= 500, detail= f"Erro no banco de dados: {erro}")
        finally:
            db.desconecta_db()

def listar_pedidos(db: BackEnd):
    db.conecta_db()
    try:
        db.cursor.execute("""
        SELECT Pedidos.id, Cardapio.Prato, Cardapio.Preco, ItensPedido.Quantidade 
        FROM Pedidos
        INNER JOIN ItensPedido ON Pedidos.id = ItensPedido.Pedido_id
        INNER JOIN Cardapio ON ItensPedido.Cardapio_id = Cardapio.id
        WHERE Pedidos.Status_pagamento = 'PAGAMENTO_APROVADO' AND Pedidos.Status_pedido = 'Em preparação...'
           """)
        pedidos = db.cursor.fetchall()

        if not pedidos:
            raise HTTPException(status_code= 404, detail= "Nenhum pedido encontrado em nossa unidade!")

        return [{"id": pedido [0],
                "prato": pedido [1],
                "preco": pedido [2],
                "quantidade": pedido[3]}
                for pedido in pedidos]
    
    except sqlite3.IntegrityError as erro:
        raise HTTPException(status_code= 500, detail= f"Erro no banco de dados: {erro}")
    finally:
        db.desconecta_db()

def adicionar_estoque(db: BackEnd, estoque: EstoqueBase): #função para saber se o produto foi registrado ou não no estoque
    produto = buscar_estoque(db, estoque)
    if produto:# caso achou um produto registrado, vai para a função atualizar quantidade
        return atualizar_quantidade (db, estoque)

    else: # caso não tenha achado o produto, vai para função cadastrar_produto
        return cadastrar_produto (db, estoque)

def buscar_estoque(db: BackEnd, estoque: EstoqueBase):#função para buscar na tabela Estoque, para saber se ja tem o pedido
    db.conecta_db()
    try:
        db.cursor.execute("""
        SELECT * FROM Estoque
        WHERE Unidade_id = ? AND Cardapio_id = ?
        """, (estoque.unidade_id, estoque.cardapio_id)) 
        return db.cursor.fetchone() #return o valor para a função adicionar_estoque
          
    finally:
        db.desconecta_db()

def atualizar_quantidade (db:BackEnd, estoque:EstoqueBase):#função para adicionar a quantidade dos produtos no estoque
    db.conecta_db()
    try:
        db.cursor.execute("""
        UPDATE Estoque
        SET Quantidade = Quantidade + ?
        WHERE Unidade_id = ? AND Cardapio_id = ?
        """, (estoque.quantidade, estoque.unidade_id, estoque.cardapio_id))        
         
        db.conn.commit()
        db.cursor.execute("""
            SELECT Cardapio.id, Cardapio.Prato, Cardapio.Preco, Estoque.Quantidade
            FROM Estoque
            INNER JOIN Cardapio ON Estoque.Cardapio_id = Cardapio.id
            WHERE Estoque.Unidade_id = ? AND Estoque.Cardapio_id = ?
            """, (estoque.unidade_id, estoque.cardapio_id)) #pega os valores das tabelas Cardapio e Estoque, para salva no fetchone.
    
        estoque_atualizado = db.cursor.fetchone()
        return EstoqueOut (id = estoque_atualizado [0], prato = estoque_atualizado [1], preco = estoque_atualizado[2], quantidade= estoque_atualizado [3])
                
    finally:
        db.desconecta_db()

def criar_pedido (db: BackEnd, pedido: PedidoCreate):
        db.conecta_db()
        valor_total_pedido = 0.0 #valor inicial do pedido
        try:
            for item in pedido.itens: #um for para passar por todas lista por itens
                db.cursor.execute(""" 
                SELECT Quantidade FROM Estoque WHERE Unidade_id = ? AND Cardapio_id = ? 
                """,(pedido.unidade_id, item.cardapio_id))
                produto = db.cursor.fetchone()
                quantidade = produto [0] #pega a quantidade de produtos no Estoque

                if quantidade < item.quantidade: #caso a quantidade do Estoque for menor q a quantidade pedida, vai dar erro raise
                    raise HTTPException(status_code= 409, detail="Quantidade insuficiente em estoque.")
                     

                db.cursor.execute(""" 
                SELECT Preco FROM Cardapio WHERE id = ? 
                """,(item.cardapio_id,))
                valor = db.cursor.fetchone()
                preco_unitario = valor [0]
                total_pagar = preco_unitario * item.quantidade #total a pagar é o valor unitario vezes quantidade.

                valor_total_pedido += total_pagar #valor total vai adicionando a cada pedido feito.

                db.cursor.execute("""
                UPDATE Estoque
                SET Quantidade = Quantidade - ?
                WHERE Unidade_id = ? AND Cardapio_id = ?
                """,(item.quantidade, pedido.unidade_id, item.cardapio_id))#Retirar produtos do estoque, apos pedido ser feito

            db.cursor.execute("""
            INSERT INTO Pedidos (Canal, Cliente_telefone, Forma_pagamento, Unidade_id, Total, Status_pagamento, Status_pedido)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,(pedido.canalPedido, pedido.cliente_telefone, "MOCK", pedido.unidade_id, valor_total_pedido, "AGUARDANDO_PAGAMENTO", "AGUARDANDO_PAGAMENTO")) #Inserir valores na tabela pedido

            pedido_id = db.cursor.lastrowid #pega o ultimo id registrado.

            for item in pedido.itens:
                db.cursor.execute("""
                INSERT INTO ItensPedido (Pedido_id, Cardapio_id, Quantidade)
                VALUES (?, ? ,?)
                    """, (pedido_id, item.cardapio_id, item.quantidade))  #Para inserir itens pedidos na tabela
                    
            db.conn.commit()
            
            return PedidoOut(id=pedido_id, cliente_telefone=pedido.cliente_telefone , status_pedido="AGUARDANDO_PAGAMENTO")

        
        except sqlite3.IntegrityError:
             db.conn.rollback()
             raise
        finally:
             db.desconecta_db()

def status_pedido(db: BackEnd, pedido: PedidoUpdate, id_pedido):# função para alterar o status_pagamento
    db.conecta_db()
    try:
        db.cursor.execute("""
        UPDATE Pedidos
        SET Status_pagamento = ?
        WHERE id = ?
        """, (pedido.status_pagamento, id_pedido)) 
        db.conn.commit()

        if pedido.status_pagamento == "PAGAMENTO_APROVADO":
            db.cursor.execute("""
            UPDATE Pedidos
            SET Status_pedido = 'Em preparação...'
            WHERE id = ?
            """, (id_pedido,)) 

        if pedido.status_pagamento == "PAGAMENTO_RECUSADO":
            db.cursor.execute("""
            SELECT Cardapio_id, Quantidade FROM ItensPedido
            WHERE Pedido_id = ?     
""",(id_pedido,)) # caso o pagamento for recusado, vai returna a quantidade de produtos para o estoque
            
            retornar_quantidade = db.cursor.fetchall()
            for itens in retornar_quantidade:
                cardapio_id = itens[0]
                quantidade = itens [1]

                db.cursor.execute("""
                UPDATE Estoque
                SET Quantidade = Quantidade + ?
                WHERE Cardapio_id = ?
    """,(quantidade, cardapio_id))
                
        db.conn.commit()

        db.cursor.execute("""
        SELECT id, Cliente_telefone, Status_pedido FROM Pedidos
        WHERE id = ?
        """, (id_pedido,)) 

        carrinho = db.cursor.fetchone()

        return PedidoOut(id=carrinho[0], cliente_telefone=carrinho[1], status_pedido=carrinho[2]
)
              
    finally:
        db.desconecta_db()

def atualizar_pedido_cozinha(db:BackEnd, id_pedido):#função para os cozinheiros atualizar caso o pedido esteja pronto
    db.conecta_db()
    try:
        db.cursor.execute("""
        UPDATE Pedidos
        SET Status_pedido = 'FINALIZADO'
        WHERE id = ?
        """, (id_pedido,)) 
        db.conn.commit()

        db.cursor.execute("""
        SELECT * FROM Pedidos
        WHERE id = ?
        """, (id_pedido,)) 

        pedido_pronto = db.cursor.fetchone()

        return {"id": pedido_pronto [0],
                "Unidade_id": pedido_pronto[1],
                "Canal ": pedido_pronto[2],
                "Cliente_telefone ": pedido_pronto[3],
                "Forma_pagamento ": pedido_pronto[4],
                "Total ": pedido_pronto[5],
                "Status_pagamento" : pedido_pronto[6],
                "Status_pedido ": pedido_pronto[7]} #return os dados para o main
    
    finally:
        db.desconecta_db()

def atualizar_prato(db:BackEnd, usuario: UsuarioLogin, preco, prato_id):#função para atualizar o preço dos pratos
    db.conecta_db()
    try:
        db.cursor.execute("""
        SELECT Cargo, Senha_hash FROM Usuarios WHERE email =?
        """, (usuario.email,))
        usuario_encontrado = db.cursor.fetchone()
        if not usuario_encontrado: #Caso nao ache o usuario, por ter digitado senha ou email invalido, return raise
            raise HTTPException(status_code= 401, detail="E-mail ou senha inválidos.")
        
        cargo_banco = usuario_encontrado[0]
        hash_banco = usuario_encontrado[1]
        
        hash_digitado = hashlib.sha256(usuario.senha.encode("utf-8")).hexdigest()
        
        if hash_digitado != hash_banco:
            raise HTTPException(status_code= 401, detail="E-mail ou senha inválidos.")
        
        if cargo_banco != "Gerente":#return raise, para caso o cargo do usuario for diferente de gerente
            raise HTTPException(status_code= 403, detail="Usuario não tem permissão para atualizar prato!")                  

        db.cursor.execute("""
        UPDATE Cardapio
        SET Preco = ?
        WHERE id = ?
        """, (preco, prato_id))
                            
        if db.cursor.rowcount == 0: #return raise, para caso a contagem de linhas atualizadas seja igual a 0
            raise HTTPException(status_code= 404, detail="Prato não encontrado em nosso sistema!")
                            
        db.conn.commit()
        db.cursor.execute("""
        SELECT id, Prato, Preco FROM Cardapio WHERE id = ?
        """, (prato_id,))
        
        prato_atualizado = db.cursor.fetchone()
        return CardapioOut (id = prato_atualizado [0], prato = prato_atualizado [1], preco = prato_atualizado [2])
    
    finally:
        db.desconecta_db()

def excluir_prato(db: BackEnd, prato_id: int):
    db.conecta_db()
    try:
        db.cursor.execute("""
        DELETE FROM Cardapio WHERE id = ?
    """, (prato_id,)) #deleta os pratos com o id enviado

        if db.cursor.rowcount == 0:
            raise HTTPException(status_code= 404, detail="Prato não encontrado em nosso sistema!")

        db.conn.commit()
                     
    finally:
        db.desconecta_db()