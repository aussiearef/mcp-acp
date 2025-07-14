from acp_sdk.server import Server
from acp_sdk.models import Message, Metadata, Author , Dependency, DependencyType, Link, LinkType, Capability
from pydantic import AnyUrl

from beeai_framework.backend.chat import ChatModel # only needed if Agent is using LLM
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory.token_memory import TokenMemory

server = Server()

@server.agent("MeaningAgent", 
              description="A dictionary tool!",
              input_content_types=["text/plain"],
              output_content_types=["text/plain"],
              metadata= Metadata(
                            programming_language="python",
                            framework="beeai_framework",
                            version="1.0",
                            author=Author(name="Aref", email="a@b.com"),
                            dependencies= [Dependency (type= DependencyType.TOOL, name="beeai_framework")],
                            recommended_models=["openai:gpt-4o"],
                            tags=["meaning", "definition", "language processing"],
                            domains=["language", "education", "knowledge"],
                            contributors=[],
                            links=[Link(type= LinkType.HOMEPAGE, url=AnyUrl("https://www.udemy.com/course/draft/6682461/?referralCode=796D178806E9010D7917"))],
                            created_at= "2024-10-01T12:00:00Z",
                            updated_at= "2024-10-01T12:00:00Z",
                            capabilities=[Capability(name="meaning", description="Find the meaning of a word")],
                                 )                  
              )

async def meaning(words: Message) -> str:
    llm= ChatModel.from_name("openai:gpt-4o")  

    memory = TokenMemory(llm)
    agent = ReActAgent(llm=llm, tools=[], memory=memory)
    response = await agent.run(prompt=f"Find the meaning of the word: {words[0]}. Be concise and return one sentence.",)
    return response.result.text

server.run() 