from fastapi import FastAPI
from database import create_db_and_tables
import auth
import users
from middleware import setup_cors


app = FastAPI(
    title="Basic Chatbot",
    description="This is a simple chatbot",
    version="1.0.0",

)   

setup_cors(app)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
