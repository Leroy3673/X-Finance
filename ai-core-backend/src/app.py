from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.finance_chat_route import finance_chat_route

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(finance_chat_route)
