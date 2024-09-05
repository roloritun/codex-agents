from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import create_langchain_agent

app = FastAPI()

class Query(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Welcome to the API"}

@app.post("/run")
def run_agent(query: Query):
    try:
        agent = create_langchain_agent()
        response = agent.invoke(query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
