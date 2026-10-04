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
- Receitas e despesas
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
