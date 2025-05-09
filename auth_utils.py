from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import requests

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

KEYCLOAK_PUBLIC_KEY_URL = "http://localhost:8080/realms/myrealm/protocol/openid-connect/certs"

def get_keycloak_public_key():
    response = requests.get(KEYCLOAK_PUBLIC_KEY_URL)
    jwks = response.json()
    return jwt.algorithms.RSAAlgorithm.from_jwk(jwks["keys"][0])

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        public_key = get_keycloak_public_key()
        payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="account")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré.")

from fastapi import HTTPException
from keycloak import KeycloakOpenID

from .keycloak_config import keycloak_openid

def verify_token(token: str):
    try:
        # Vérifie et décode le token JWT
        user_info = keycloak_openid.userinfo(token)
        return user_info
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré.")
