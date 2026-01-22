from fastmcp import FastMCP
from mcp import McpError
from fastmcp.server.dependencies import get_http_headers
from pydantic import BaseModel
import asyncio
import httpx
from authlib.jose import JsonWebToken, JsonWebKey, JWTClaims
from authlib.jose.util import extract_header

mcp = FastMCP(stateless_http=True)

class Greeting(BaseModel):
    message: str

# Configuration for OAuth 2.0 provider
OAUTH_ISSUER = "https://dev-of6fy7icbrna3p24.us.auth0.com/"  # Issuer URL - Change to your own ISSUER URL
JWKS_URI = "https://dev-of6fy7icbrna3p24.us.auth0.com/.well-known/jwks.json"  # JWKS endpoint - Change to your own URL
AUDIENCE = "https://dev-of6fy7icbrna3p24.us.auth0.com/api/v2/"  # API Identifier - # JWKS endpoint - Change to your own URL

async def get_public_key(kid: str) -> dict:
    """Fetch public key for the given key ID (kid) from the JWKS endpoint."""

    async with httpx.AsyncClient() as client:
        response = await client.get(JWKS_URI)
        response.raise_for_status()
        keys = response.json()["keys"]
        for key in keys:
            return key
        raise ValueError(f"No public key found for kid: {kid}")

@mcp.tool("Greetings")
async def greetings(name: str) -> Greeting:
    """A tool function that accepts a parameter called name and returns a personalised greeting message."""
    headers = get_http_headers()
    authorization_header = headers.get("Authorization")

    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.replace("Bearer ", "", 1)
        try:
            # Decode JWT to get kid
            token_obj = JsonWebToken(algorithms=["RS256"])
            header_segment = token.split(".")[0]
            header = extract_header(header_segment.encode("utf-8"), error_cls=McpError)
            kid = header.get("kid")
            if not kid:
                raise ValueError("No kid in token header")

            # Fetch public key
            jwk = await get_public_key(kid)
            public_key = JsonWebKey.import_key(jwk)

            # Validate JWT
            claims: JWTClaims = token_obj.decode(token, public_key)
            claims.validate(iss=OAUTH_ISSUER, aud=AUDIENCE, required_scopes=None)
            user_id = claims.get("sub", "Unknown")  # Use sub for Client Credentials Grant
            print("User Id:", user_id)
            print("Kid:", kid)
            print("Claims:", claims)
        except Exception as e:
            print(f"Token validation failed: {e}")
    else:
        print("No valid Authorization header found")

    return Greeting(message=f"Special greetings to, {name}")

async def main():
    await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())