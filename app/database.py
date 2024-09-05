from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class API(Base):
    __tablename__ = 'apis'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    spec_url = Column(String, nullable=False)
    file_content = Column(Text)
    description = Column(Text)
    auth_type = Column(String, nullable=False)  # 'apikey', 'oauth2', etc.
    api_key = Column(String)
    oauth_token_url = Column(String)
    client_id = Column(String)
    client_secret = Column(String)
    custom_headers = Column(String)
    url_params = Column(String)

class DatabaseConnection(Base):
    __tablename__ = 'database_connections'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    connection_string = Column(String, nullable=False)
    description = Column(Text)
    prompt_query= Column(Text)

class BuiltinTool(Base):
    __tablename__ = 'builtin_tools'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    function_code = Column(Text, nullable=False)
    description = Column(Text)
    required_api_key = Column(String)

def init_db():
    engine = create_engine('sqlite:///data/database.db')  # Use your preferred database
    Base.metadata.create_all(engine)
    return engine

engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()
