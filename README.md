# API de Controle Financeiro

API REST desenvolvida em Python com FastAPI para controle de receitas e despesas.

O projeto permite cadastrar usuários, realizar login, criar categorias, registrar transações financeiras e visualizar um resumo financeiro individual de cada usuário.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- pwdlib
- Uvicorn

## Funcionalidades

- Cadastro de usuários
- Login
- Autenticação com JWT
- Hash de senhas
- Controle de acesso por usuário
- CRUD de categorias
- CRUD de transações
- Cadastro de receitas e despesas
- Filtro por tipo de transação
- Filtro por categoria
- Resumo financeiro
- Documentação automática com Swagger

## Estrutura do projeto

```text
api_controle_financeiro/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── requirements.txt
│
└── routers/
    ├── __init__.py
    ├── transacoes.py
    ├── categorias.py
    ├── usuarios.py
    ├── auth.py
    └── resumo.py
```

## Principais rotas

### Usuários

```text
POST /usuarios/
```

Cadastra um novo usuário.

### Autenticação

```text
POST /auth/login
GET  /auth/me
```

O login retorna um token JWT.

A rota `/auth/me` permite verificar o ID do usuário autenticado.

### Categorias

```text
POST   /categorias/
GET    /categorias/
GET    /categorias/{id}
PUT    /categorias/{id}
DELETE /categorias/{id}
```

Permite criar, listar, buscar, atualizar e excluir categorias.

Uma categoria que possui transações cadastradas não pode ser excluída.

### Transações

```text
POST   /transacoes/
GET    /transacoes/
GET    /transacoes/{id}
PUT    /transacoes/{id}
DELETE /transacoes/{id}
```

As transações são vinculadas ao usuário autenticado.

Cada usuário consegue acessar, alterar e excluir somente suas próprias transações.

## Filtros de transações

É possível filtrar por tipo:

```text
GET /transacoes/?tipo=despesa
```

ou:

```text
GET /transacoes/?tipo=receita
```

Também é possível filtrar por categoria:

```text
GET /transacoes/?categoria_id=3
```

Os filtros podem ser combinados:

```text
GET /transacoes/?tipo=despesa&categoria_id=3
```

## Resumo financeiro

Rota:

```text
GET /resumo/
```

Exemplo de resposta:

```json
{
  "total_receitas": 2500,
  "total_despesas": 580,
  "saldo": 1920
}
```

O resumo considera apenas as transações do usuário autenticado.

## Autenticação

Após realizar login, a API retorna um token JWT.

Exemplo:

```json
{
  "access_token": "TOKEN_JWT",
  "token_type": "bearer"
}
```

O token é utilizado nas rotas protegidas para identificar o usuário.

Dessa forma, cada usuário possui acesso somente às próprias transações.

## Banco de dados

O projeto utiliza SQLite.

O banco local é armazenado no arquivo:

```text
financeiro.db
```

O arquivo não é enviado para o GitHub.

As tabelas são criadas automaticamente ao iniciar a aplicação através do SQLAlchemy.

## Como executar o projeto

Clone o repositório:

```bash
git clone https://github.com/felipeperes-softwareeng/api_controle_financeiro.git
```

Entre na pasta:

```bash
cd api_controle_financeiro
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

No Git Bash, ative o ambiente:

```bash
source venv/Scripts/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Inicie o servidor:

```bash
python -m uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação Swagger ficará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Exemplos de uso

### Criar usuário

```json
{
  "nome": "Felipe",
  "email": "felipe@email.com",
  "senha": "senha123"
}
```

### Login

```json
{
  "email": "felipe@email.com",
  "senha": "senha123"
}
```

### Criar categoria

```json
{
  "nome": "Alimentação"
}
```

### Criar transação

```json
{
  "descricao": "Mercado",
  "valor": 400,
  "tipo": "despesa",
  "categoria_id": 1
}
```

## Validações

A API possui algumas validações, como:

- valor da transação deve ser maior que zero
- tipo deve ser `receita` ou `despesa`
- categoria precisa existir
- categorias não podem possuir nomes duplicados
- e-mails não podem ser cadastrados mais de uma vez
- senha precisa possuir pelo menos 6 caracteres
- usuário não pode acessar transações de outro usuário

## Segurança

As senhas não são armazenadas diretamente no banco.

Antes de serem salvas, são transformadas em hash utilizando `pwdlib`.

A autenticação das rotas protegidas é feita através de JWT.

## Documentação

O FastAPI gera automaticamente a documentação da API através do Swagger.

Para acessar:

```text
http://127.0.0.1:8000/docs
```

No Swagger é possível:

- visualizar todas as rotas
- cadastrar usuários
- realizar login
- autenticar utilizando o token
- criar transações
- consultar transações
- alterar transações
- excluir transações
- testar filtros
- consultar o resumo financeiro

## Autor

Felipe Peres d'Oliveira

Projeto desenvolvido para estudo e prática de desenvolvimento Back-End utilizando Python.
