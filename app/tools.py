from typing import Any, Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.agent_toolkits.openapi import planner
from langchain_community.agent_toolkits.openapi.spec import ReducedOpenAPISpec
from constants import ALLOW_DANGEROUS_REQUEST, DEFAULT_DB_TOOL_PROMPT, API_TOOL_VERBOSE, DB_TOOL_VERBOSE
from langchain_community.utilities import RequestsWrapper


class DbTool(BaseTool):
    name: str
    description: str
    args_schema: Type[BaseModel]
    db_conn_details: str
    prompt_query: Optional[str] = None
    return_direct = True
    llm: Any

    def _run(self, question: str):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        self.prompt_query
                        if self.prompt_query
                        else DEFAULT_DB_TOOL_PROMPT
                    ),
                ),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        try:
            db = SQLDatabase.from_uri(database_uri=self.db_conn_details)
            agent_executor = create_sql_agent(
                self.llm,
                db=db,
                prompt=prompt,
                agent_type="openai-tools",
                verbose=DB_TOOL_VERBOSE,
                extra_tools=[],
            )
            response = agent_executor.invoke({"input": question})
            return response
        except Exception as e:
            print(e)
        return

    def _arun(self, question: str):
        raise NotImplementedError("does not support async")


class ApiTool(BaseTool):
    name: str
    description: str
    args_schema: Type[BaseModel]
    reduced_openapi_spec: ReducedOpenAPISpec
    return_direct = True
    request_wrapper: RequestsWrapper
    llm: Any

    def _run(self, question: str):
        try:
            agent_executor = planner.create_openapi_agent(
                api_spec=self.reduced_openapi_spec,
                requests_wrapper=self.request_wrapper,
                llm=self.llm,
                allow_dangerous_requests=ALLOW_DANGEROUS_REQUEST,
                verbose=API_TOOL_VERBOSE,
                agent_executor_kwargs=dict(
                    return_intermediate_steps=True,
                    handle_parsing_errors=True,
                    max_iterations=5,
                ),
            )
            response = agent_executor.invoke({"input": question})
            return response
        except Exception as e:
            print(e)
        return

    def _arun(self, question: str):
        raise NotImplementedError("does not support async")
