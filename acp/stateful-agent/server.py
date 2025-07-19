from acp_sdk.server import Server, Context
from acp_sdk.models import Message

from beeai_framework.backend import ChatModel , UserMessage
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory.token_memory import TokenMemory


server = Server()

@server.agent("chat")
async def chat(chat_prompt: Message , context:Context) -> str:
    llm= ChatModel.from_name("openai:gpt-4o")  
    memory = TokenMemory(llm)
    agent = ReActAgent(llm=llm, tools=[], memory=memory)

    # changes for session management

    history = context.session.load_history()
    history_messages = [message async for message in history]

    framework_messages = [UserMessage(str(message)) for message in history_messages] # Different for non-BEE AI frameworks.
    await agent.memory.add_many(framework_messages)

    # end changes for session management

    response = await agent.run(prompt=chat_prompt[0].parts[0].content)
    return response.result.text

server.run() 