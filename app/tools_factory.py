import json
from pydantic import BaseModel, Field
from database import DatabaseConnection, API
from sqlalchemy.orm import Session
from tools import DbTool, ApiTool
from utils import Llm, fetch_openapi_spec
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.utilities import RequestsWrapper


class UserQuery(BaseModel):
    """get_info_from_prompt"""

    question: str = Field(description="question from the prompt")


llm = Llm.get_llm()

"""Database Tools"""


def create_db_tools(session: Session):

    db_connections = session.query(DatabaseConnection).all()
    tools = []
    for db in db_connections:
        try:
            tool = DbTool(
                name=db.name,
                description=db.description,
                db_conn_details=db.connection_string,
                prompt_query=db.prompt_query,
                args_schema=UserQuery,
                llm=llm,
                verbose=True,
            )
            tools.append(tool)
        except Exception as e:
            print(e) #inject a Logger -inform the user that a db is probably unreachable
            continue
    return tools


"""Openspec API Tools
"""
# TODO: implement basic auth, oauth and oauth2


def create_api_tools(session: Session):

    api_metadata_list = session.query(API).all()
    tools = []
    
    for api in api_metadata_list:
            try:
                raw_spec = fetch_openapi_spec(
                    api.spec_url if api.spec_url else api.file_content
                )
                reduced_spec = reduce_openapi_spec(raw_spec)
                headers = {}
                if api.auth_type == "bearer":
                    headers = {"Authorization": f"Bearer {api.api_key}"}
                elif api.auth_type == "apikey":
                    headers = {"x-api-key": f"{api.api_key}"}
                if api.custom_headers:
                    custom_headers = json.loads(api.custom_headers.replace("'", '"'))
                    headers = {**headers, **custom_headers}
                request_wrapper = RequestsWrapper(headers=headers)
                tool = ApiTool(
                    name=api.name,
                    description=api.description,
                    reduced_openapi_spec=reduced_spec,
                    request_wrapper=request_wrapper,
                    args_schema=UserQuery,
                    llm=llm,
                    verbose=True,
                )
                tools.append(tool)
            except Exception as e:
                print(e)  #inject a Logger -inform the user that a db is probably unreachable
                continue
   
    return tools
