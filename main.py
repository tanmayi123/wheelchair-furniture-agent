from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import sys
import os
sys.path.append(os.path.dirname(__file__))
from agent import run_agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    room_width_ft: float
    room_length_ft: float
    furniture_needed: list[str]
    wheelchair_type: str
    user_style: str

@app.post("/agent/run")
async def run(request: AgentRequest):
    result = await run_agent(
        room_width_ft=request.room_width_ft,
        room_length_ft=request.room_length_ft,
        furniture_needed=request.furniture_needed,
        wheelchair_type=request.wheelchair_type,
        user_style=request.user_style
    )
    return result

app.mount("/", StaticFiles(directory=".", html=True), name="static")