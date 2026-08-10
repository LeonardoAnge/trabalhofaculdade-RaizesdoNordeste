# Sistema Back-End - Lanchonete Raízes do Nordeste
Nome: Leonardo Angelo da Silva Lima
RU: 4841101
Curso: CST ANÁLISE E DESENVOLVIMENTO DE SISTEMAS
Disciplina: Desenvolvimento Back-End

Uma API desenvolvida para o gerenciamento de uma rede de lanchonetes.
O projeto foi desenvolvido usando FastAPI, SQLite3, Pydantic, Hashlib, Enum, Typing.

Separei e organizei o projeto em varios arquivos onde:
-main.py ficaria responsável pela API e EndPoints.
-crud.py aplicação e regras de negócios.
-database.py e models.py infraestrutura e criação de tabelas.
-schemas.py validação de entrada e saída de dados.

Na criação de cadastro as senhas são armazenadas utilizando uma função de hash com hashlib. Além de um controle estrito baseado em cargos, que apenas usuários específicos poderão
usar certos EndPoints.
Atualização de cargo por id(telefone) de cada usuário, onde apenas o admin poderá fazer isso.
Validação de Login.
Criação de unidades e estoque, onde cada unidade terá seu estoque para controle individual.
Abastecimento de estoque, onde o usuário colocara a unidade desejada e a quantidade de produtos a ser adicionado.
Na criação de pedidos, só poderá ser vendido produtos que tem no estoque da unidade selecionada.
No registro de pedidos, foi feito um sistema de pagamento simulado, onde será registrado o pedido e terá baixa no estoque automaticamente, após a comprovação do pagamento, o pedido entra na fila de 'Preparação...'.
Caso o pagamento der recusado, a quantidade de itens voltaram para o estoque automaticamente e o pedido fica com o status 'Recusado'.
Tela para a cozinha poder atualizar pedidos prontos, deixando o status 'Finalizado'

# Instalação das dependências obrigatórias
pip install fastapi uvicorn

# Comando para ligar o servidor web
uvicorn main:app --reload

#A documentação interativa da API pode ser acessada pelo Swagger:
http://127.0.0.1:8000/docs
