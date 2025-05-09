"""
Utilidades de hash de senha e JWT para a API.

- hash_password / verify_password  ➜ bcrypt
- create_access_token              ➜ gera JWT assinado
- get_current_user                 ➜ dependência FastAPI para validar Bearer
"""

from datetime import datetime, timedelta
from typing import Union
import os

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

# --------------------------------------------------------------------------- #
# Configurações
# --------------------------------------------------------------------------- #
_JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change_me")
_JWT_ALGORITHM: str = "HS256"
_JWT_EXP_HOURS: int = 24

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_bearer_scheme = HTTPBearer()   # usado como dependência nos endpoints


# --------------------------------------------------------------------------- #
# Funções: Senha
# --------------------------------------------------------------------------- #
def hash_password(password: str) -> str:
    """Gera o hash bcrypt para uma senha em texto-plano."""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha em texto-plano com o hash armazenado."""
    return _pwd_context.verify(plain_password, hashed_password)


# --------------------------------------------------------------------------- #
# Funções: JWT
# --------------------------------------------------------------------------- #
def create_access_token(subject: Union[int, str],
                        expires_hours: int = _JWT_EXP_HOURS) -> str:
    """
    Cria um JWT contendo a claim ``sub`` e tempo de expiração.

    Parameters
    ----------
    subject : int | str
        Identificador do usuário (id ou email) para armazenar em ``sub``.
    expires_hours : int
        Horas até a expiração do token. Padrão = 24.
    """
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, _JWT_SECRET_KEY, algorithm=_JWT_ALGORITHM)


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(_bearer_scheme)
) -> str:
    """
    Dependência FastAPI que valida o token Bearer e devolve a claim ``sub``.

    Lança ``HTTPException 401`` se o token for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token.credentials,
                             _JWT_SECRET_KEY,
                             algorithms=[_JWT_ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token inválido")
