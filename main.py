from fastapi import FastAPI, Query
from schemas import CardapioOut, CardapioCreate, UsuarioOut, UsuarioCreate, UsuarioLogin, LoginOut, EstoqueBase, EstoqueOut,EstoqueUpdate, UnidadeOut, UnidadeCreate, PedidoCreate, PedidoOut, CanaisAtendimento, StatusPagamento, Cargos
from database import BackEnd
import crud



app = FastAPI(title= "Raizes do Nordeste",
              description="API REST para gereciamento da rede de lanchonetes Raizes do Nordeste com FastAPI + SQLite3")
db = BackEnd()
db.cria_tabela()

@app.get("/")
def inicio():
    return {"mensagem": "API funcionando!"}

#Cadastro de usuario
@app.post("/Criar/Usuario",
         response_model= UsuarioOut,
         status_code= 201,
         summary= "Cadastrar um novo usuario.",
         tags = ["Usuario"])
def salvar_cadastro(usuario: UsuarioCreate):
    return crud.salvar_cadastro(db, usuario)

@app.put("/Atualizar/Cargo/Usuario",
         summary= "Atualizar cargo do usuario.",
         tags = ["Usuario"])
def atualizar_cargo(cargo: Cargos, telefone:str):
    return crud.atualizar_cargo(db, cargo, telefone)

#Verificação de Login
@app.post("/Auth/Login",
         response_model= LoginOut,
         status_code= 201,
         summary= "Fazer Login.",
         tags = ["Usuario"])
def verificar_login(usuario: UsuarioLogin):
    return crud.verificar_login(db, usuario)

#Cadastro de pratos
@app.post("/Criar/Cardapio",
         response_model= CardapioOut,
         status_code= 201,
         summary= "Criar um novo prato",
         tags = ["Cardapio"])
def criar_prato(prato: CardapioCreate):
    return crud.cadastrar_prato(db, prato)
   
#Listar Cardapio
@app.get (
    "/List/Cardapio",
    summary = "Listar Cardapio",
    tags = ["Cardapio"]
    )
def listar_pratos(unidade_id:int , offset: int = Query(0, ge=0, description="Número de pratos a pular"), limit: int = Query(50, ge=1, le=200, description="Máximo de pratos a retornar")):
    return crud.listar_pratos(db, unidade_id, limit=limit, offset=offset)

#Atualizar prato
@app.put("/Preco/Cardapio/{prato_id}",
        response_model= CardapioOut,
        summary= "Atualizar preco do prato por ID",
        tags = ["Cardapio"])
def atualizar_prato(usuario: UsuarioLogin, prato_id: int, preco: float):
    return crud.atualizar_prato(db, usuario, preco, prato_id)

#Deletar prato
@app.delete("/Desativar/Cardapio/{prato_id}",
        status_code= 200,
        summary= "Desativa um prato do cardapio por ID",
        tags = ["Cardapio"])
def excluir_prato(prato_id: int):
    return crud.excluir_prato(db, prato_id)

@app.put("/Reativar/Cardapio/{prato_id}",
        status_code= 200,
        summary= "Reativar um prato do cardapio por ID",
        tags = ["Cardapio"])
def reativar_prato(prato_id: int):
    return crud.reativar_prato(db, prato_id)

@app.post("/Criar/Unidade",
        response_model= UnidadeOut,
        status_code= 201,
        summary= "Criar uma nova Unidade",
        tags = ["Unidade"])
def criar_unidade(unidade: UnidadeCreate):
    return crud.criar_unidade(db, unidade)

@app.get("/List/Unidade",
        summary= "Lista de todas unidades",
        tags = ["Unidade"])
def listar_unidade():
    return crud.listar_unidade(db)

#Cadastro de pratos
@app.post("/Criar/Estoque",
        response_model= EstoqueOut,
        status_code= 201,
        summary= "Criar um novo produto",
        tags = ["Estoque"])
def criar_prato(produto: EstoqueBase):
    return crud.cadastrar_produto(db, produto)

#Cadastro de pratos
@app.post("/Estoque/Abastecimento",
        summary= "Abastecer estoque",
        tags = ["Estoque"])
def adicionar_estoque(produto: EstoqueUpdate):
    return crud.adicionar_estoque(db, produto)

@app.get("/List/Estoque/{Unidade_id}",
        summary= "Listar produtos estoque",
        tags = ["Estoque"])
def listar_estoque(unidade_id: int):
    return crud.listar_estoque(db, unidade_id)

@app.post("/Criar/Pedido",
        response_model= PedidoOut,
         status_code= 201,
         summary= "Criar pedido",
         tags = ["Pedidos"])
def criar_pedido(pedido: PedidoCreate, canal: CanaisAtendimento):
    return crud.criar_pedido(db, pedido, canal)

@app.put("/Status/Pedido/{id_pedido}",
         summary= "Atualizar Pedido",
         tags = ["Pedidos"])
def status_pedido(status: StatusPagamento , id_pedido: int):
    return crud.status_pedido(db, status , id_pedido)


@app.get("/List/Pedido/Canal",
        summary= "Listar pedidos feitos em cada canal e que ja foram pagos",
        tags = ["Pedidos"])
def listar_pedidos_canal(canal_pedido: CanaisAtendimento):
    return crud.listar_pedidos_canal(db, canal_pedido)

@app.get("/Cozinha/List/Pedido/{Unidade_id}",
        summary= "Listar pedidos feitos para ser preparados",
        tags = ["Pedidos"])
def listar_pedidos(unidade_id: int):
    return crud.listar_pedidos(db, unidade_id)

@app.put("/Cozinha/Pedido/{id_pedido}",
         status_code= 201,
         summary= "Para atualizar quando tiverem prontos",
         tags = ["Pedidos"])
def atualizar_pedido_cozinha(id_pedido: int):
    return crud.atualizar_pedido_cozinha(db, id_pedido)