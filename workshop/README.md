
Follow these steps:

1. Run "pip install -r requirements.txt"
2. Run "python db_create.py" to create an example database. Modify this code to insert your desired phone numbers.
3. Run "python get_number_status.py". You must have added mcp_api_key environment variable.
4. Run "python sim_activate_agent.py". You must have added acp_api_key environment variable.
5. Run "python agent-client.py" to test your ACP Agent locally. Edit code to corrext x-api-key's value. OPTIONAL.
6. Run "python -m http.server 8080" to start a web server.
7. Open a browser and navigate to http://localhost:8080. The x-api-key is hard-coded in the html file. Change it to match your api key.

##Authentication

1. MCP Server uses API KEY authentication method. Your ACP server must send x-api-key header to MCP server. The value of x-api-key is hard-coded in sim-activate-agent.py at line 41, for your convenience.

```
async with streamablehttp_client(mcp_url, 
                                     headers={"x-api-key":"123"}) as (read_stream, write_stream, _):
```

In the MCP server code, number_mcp.py, you must have already set an environment variable called 'mcp_api_key'. The value of this environment value must match the value of x-api-key header that you will send to MCP server from ACP server.

```
expected_key = os.environ.get("mcp_api_key")
```

2. ACP server uses OAUTH 2.0 with Google. You must put your GOOGLE CLIENT ID in both chat.html, and in sim-activate-agent.py.

```
<div id="g_id_onload"
      data-client_id="". // <--- PUT YOUR GOOGLE CLIENT ID HERE
      data-callback="handleCredentialResponse">
</div>
```

and in sim-activate-agent.py, you must set correct ISSUER, JWKS_URI and Client ID:

```
OAUTH_ISSUER = "https://accounts.google.com"
JWKS_URI = "https://www.googleapis.com/oauth2/v3/certs"
AUDIENCE = ""    # YOUR_GOOGLE_CLIENT_ID
```








