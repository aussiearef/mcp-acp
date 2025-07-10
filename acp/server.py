from acp_sdk.server import Server
from acp_sdk.models import Message, MessagePart

from beeai_framework.backend.chat import ChatModel # only needed if Agent is using LLM
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory.token_memory import TokenMemory


server = Server()

@server.agent("MeaningAgent")
async def meaning(words: Message) -> str:
    """A tool function that accepts a parameter called word and returns its meaning."""

    #supported llm names are "ollama", "openai", "watsonx", "groq", "xai", "vertexai", "amazon_bedrock", "anthropic", "azure_openai", "mistralai"
    llm= ChatModel.from_name("openai:gpt-4o")  

    memory = TokenMemory(llm)
    agent = ReActAgent(llm=llm, tools=[], memory=memory)
    response = await agent.run(prompt=f"Find the meaning of the word: {words[0]}. Be concise and return one sentence.",)
    return response.result.text

server.run() 