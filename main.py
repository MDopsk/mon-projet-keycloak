from fastapi import FastAPI, HTTPException, Form
from auth.keycloak_config import keycloak_openid

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API d'authentification"}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(username, password)
        return {
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "expires_in": token["expires_in"]
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe invalide.")

from fastapi import Request
from auth.auth_utils import verify_token

@app.get("/verify")
def verify(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant ou invalide.")

    token = auth_header.split(" ")[1]
    user_info = verify_token(token)
    return {"message": "Token valide", "user": user_info}
# Ajouter ces endpoints dans main.py

@app.post("/logout")
def logout(refresh_token: str = Form(...)):
    try:
        keycloak_openid.logout(refresh_token)
        return {"message": "Déconnexion réussie"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Échec de la déconnexion")

@app.post("/refresh")
def refresh(refresh_token: str = Form(...)):
    try:
        token = keycloak_openid.refresh_token(refresh_token)
        return {
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "expires_in": token["expires_in"]
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Refresh token invalide")
