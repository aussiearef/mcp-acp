
Follow these steps:

1. Run "pip install -r requirements.txt"
2. Run "python db_create.py" to create an example database. Modify this code to insert your desired phone numbers.
3. Run "python get_number_status.py". You must have added mcp_api_key environment variable.
4. Run "python sim_activate_agent.py". You must have added acp_api_key environment variable.
5. Run "python agent-client.py" to test your ACP Agent locally. Edit code to corrext x-api-key's value. OPTIONAL.
6. Run "python3 -m http.server 8080" to start a web server.
7. Open a browser and navigate to http://localhost:8080. The x-api-key is hard-coded in the html file. Change it to match your api key.

Note: x-api-key is hard-coded in the html file for your convenience. In a real project that you will run in Production, secure the x-api-key value.





