
# Workshop Instructions
This directory includes a MCP server with two MCP tools, an A2A-compatible AI Agent, and a HTML/Javascript code to simulate a chat bot, where you can activate a SIM (mobile or cell phone) number.

## Setting up
Follow these steps, after creating and activating a virtual Python environment:

1. Sign up with Google.
2. Go to https://console.cloud.google.com/apis/credentials
3. Create a Project, or select an existing Project.

   <img width="413" height="52" alt="image" src="https://github.com/user-attachments/assets/c71bbad5-ca22-45c6-958e-531538fa1920" />
   
4. Click on 'Create credentials' and select 'OAuth client ID'
  
   <img width="543" height="307" alt="image" src="https://github.com/user-attachments/assets/268417d2-5e61-4fce-bee5-5a3f73aaa02c" />

5. Enter `http://localhost:9000`, for both Javascript URLs and the return URL.
6. Complete all the steps, and at the end, grab the Client ID. You must put this Client ID in both `sim-activate-agent.py` and in `chat.html` files.


7. Run `pip install -r requirements.txt` in the terminal, inside your virtual environment.
8. Run `python db_create.py` to create an example database. Modify this code to insert your desired phone numbers.
9. Create an environment variable called 'mcp_api_key'. Set its value to 123.
10. Run `python number_mcp.py`. You must have added mcp_api_key environment variable in Terminal beforehand.
11. Run `python sim_activate_agent.py`. 
12. Run `python agent-client.py` to test your A2A Agent locally. Edit code to corrext x-api-key's value. OPTIONAL.
13. Run `python -m http.server 8080` to start a web server, so that you can run chat.html.
14. Open a browser and navigate to `http://localhost:8080/chat.html`. 

## Authentication

1. MCP Server uses API KEY authentication method. Your A2A agent must send x-api-key header to MCP server. The value of x-api-key is hard-coded in sim-activate-agent.py at line 41, for your convenience.

```
async with streamablehttp_client(mcp_url, 
                                     headers={"x-api-key":"123"}) as (read_stream, write_stream, _):
```

In the MCP server code, number_mcp.py, you must have already set an environment variable called 'mcp_api_key'. The value of this environment value must match the value of x-api-key header that you will send to MCP server from A2A agent.

```
expected_key = os.environ.get("mcp_api_key")
```

2. A2A agent uses OAUTH 2.0 with Google. You must put your GOOGLE CLIENT ID in both chat.html, and in sim-activate-agent.py.

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








