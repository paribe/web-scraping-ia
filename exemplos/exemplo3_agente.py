import os
from decouple import config
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_openai import ChatOpenAI

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

def executar_agente():
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    browser = create_sync_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
    tools = toolkit.get_tools()
    agent_chain = initialize_agent(
        tools, llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    result = agent_chain.invoke(
        input='qual time está na primeira colocação do brasileirão na tabela do site https://ge.globo.com/futebol/brasileirao-serie-a/? E o último colocado?'
    )
    return result
