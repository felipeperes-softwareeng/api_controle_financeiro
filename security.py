from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

password_hash = PasswordHash.recommended()

SECRET_KEY = "chave-secreta-do-projeto"
ALGORITHM = "HS256"
TEMPO_TOKEN_MINUTOS = 60

bearer_scheme = HTTPBearer()

def gerar_hash_senha(senha: str):
    return password_hash.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return password_hash.verify(senha, senha_hash)

def criar_token(usuario_id: int):

    expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_TOKEN_MINUTOS)

    dados_token = {
        "sub": str(usuario_id),
        "exp": expiracao
    }

    return jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verificar_token(
    credenciais: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):

    token = credenciais.credentials

    try:
        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = int(dados["sub"])

        return usuario_id

    except:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )