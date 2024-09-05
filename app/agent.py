from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
)
from app.constants import AGENT_EXECUTOR_VERBOSE, RETURN_INTERMIDIATE_STEPS
from app.tools_factory import create_db_tools, create_api_tools
from app.utils import Llm
from app.database import session
from app.prompt import (
    get_prompt_for_openai_functions_agent,
)

all_tools = []
llm = Llm.get_llm()
api_tools = create_api_tools(session)
db_tools = create_db_tools(session)

all_tools = api_tools + db_tools  # + builtin_tools


def create_langchain_agent():

    prompt = get_prompt_for_openai_functions_agent()
    prompt.pretty_print()
    agent = create_openai_functions_agent(llm=llm, tools=all_tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        verbose=AGENT_EXECUTOR_VERBOSE,
        handle_parsing_errors=True,
        # max_iterations=3,
        return_intermediate_steps=RETURN_INTERMIDIATE_STEPS,
        # early_stopping_method='generate'
    )
    return agent_executor


if __name__ == "__main__":

    agent = create_langchain_agent()

    while True:
        user_input = input("User: ")

        response = agent.invoke({"input": user_input})

        print(f"Agent: {response['output']}")
