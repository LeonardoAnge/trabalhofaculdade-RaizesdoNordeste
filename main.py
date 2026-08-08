from fastapi import FastAPI, Query, HTTPException
from schemas import CardapioOut, CardapioCreate,CardapioUpdate, UsuarioOut, UsuarioCreate, UsuarioLogin, LoginOut, EstoqueBase, EstoqueOut,EstoqueUpdate, UnidadeBase, UnidadeOut, UnidadeCreate, PedidoCreate, PedidoOut, PedidoUpdate
from typing import List
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
    response_model = List [CardapioOut],
    summary = "Listar Cardapio",
    tags = ["Cardapio"]
    )
def listar_pratos(
    offset: int = Query(0, ge=0, description="Número de pratos a pular"),
    limit: int = Query(50, ge=1, le=200, description="Máximo de pratos a retornar")
):
    return crud.listar_pratos(db, limit=limit, offset=offset)

#Atualizar prato
@app.put("/Preco/Cardapio/{prato_id}",
        response_model= CardapioOut,
        summary= "Atualizar preco do prato por ID",
        tags = ["Cardapio"])
def atualizar_prato(usuario: UsuarioLogin, prato_id: int, preco: float):
    return crud.atualizar_prato(db, usuario, preco, prato_id)

#Deletar prato
@app.delete("/Delete/Cardapio/{prato_id}",
        status_code= 200,
        summary= "Deletar um prato do cardapio por ID",
        tags = ["Cardapio"])
def excluir_prato(prato_id: int):
    crud.excluir_prato(db, prato_id)

@app.post("/Criar/Unidade",
        response_model= UnidadeOut,
        status_code= 201,
        summary= "Criar uma nova Unidade",
        tags = ["Unidade"])
def criar_unidade(unidade: UnidadeCreate):
    return crud.criar_unidade(db, unidade)

@app.get("/List/Unidade",
        response_model= list [UnidadeOut],
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
        response_model= EstoqueOut,
        status_code= 201,
        summary= "Abastecer estoque",
        tags = ["Estoque"])
def adicionar_estoque(produto: EstoqueUpdate):
    return crud.adicionar_estoque(db, produto)

@app.get("/List/Estoque/{Unidade_id}",
        response_model= list [EstoqueOut],
        summary= "Listar produtos estoque",
        tags = ["Estoque"])
def listar_estoque(unidade_id: int):
    return crud.listar_estoque(db, unidade_id)

@app.post("/Criar/Pedido",
        response_model= PedidoOut,
         status_code= 201,
         summary= "Criar pedido",
         tags = ["Pedidos"])
def criar_pedido(pedido: PedidoCreate):
    return crud.criar_pedido(db, pedido)

@app.put("/Status/Pedido{id_pedido}",
        response_model= PedidoOut,
         status_code= 201,
         summary= "Atualizar Pedido",
         tags = ["Pedidos"])
def status_pedido(pedido: PedidoUpdate, id_pedido):
    return crud.status_pedido(db, pedido, id_pedido)

@app.get("/List/Pedido/{Unidade_id}",
        response_model= list [EstoqueOut],
        summary= "Listar pedidos feitos",
        tags = ["Pedidos"])
def listar_pedidos():
    return crud.listar_pedidos(db)

@app.put("/Cozinha/Pedido{id_pedido}",
         status_code= 201,
         summary= "Para atualizar pedidos que estão em preparação",
         tags = ["Pedidos"])
def atualizar_pedido_cozinha(id_pedido: int):
    return crud.atualizar_pedido_cozinha(db, id_pedido)