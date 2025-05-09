from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/",
    client_id="auth-service",
    realm_name="projet_est",
    client_secret_key="VrK1SlBoXF7NdKG5eUbC0vFdGd4AO30b"
)


