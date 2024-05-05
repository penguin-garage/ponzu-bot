from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from ponzu_bot.chatter import DEFAULT_INITIAL_PROMPT
# from langchain import hub
from ponzu_bot.qa import penguin_vector_search

def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    # Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return executor

def ponzu_bot_agent():
    tools = [penguin_vector_search]

    llm = ChatOpenAI(model="gpt-4-turbo")
    # prompt = hub.pull("hwchase17/openai-tools-agent")
    agent = create_agent(llm, tools, DEFAULT_INITIAL_PROMPT)
    return agent
