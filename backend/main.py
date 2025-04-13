from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import openai
import datetime
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Initialize FastAPI
app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database setup
conn = sqlite3.connect("analyzer.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mode TEXT,
        user_input TEXT,
        llm_output TEXT,
        timestamp TEXT
    )
""")
conn.commit()

# Request model
class AnalyzeRequest(BaseModel):
    mode: str
    user_input: str

@app.post("/analyze/")
def analyze(request: AnalyzeRequest):
    try:
        llm_output = f"[MOCK OUTPUT] You selected mode: {request.mode}. Here's a simulated response to: '{request.user_input[:50]}...'"

        # Save to DB
        timestamp = datetime.datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO history (mode, user_input, llm_output, timestamp) VALUES (?, ?, ?, ?)",
            (request.mode, request.user_input, llm_output, timestamp)
        )
        conn.commit()

        return {"response": llm_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/")
def get_history():
    cursor.execute("SELECT id, mode, user_input, llm_output, timestamp FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    return {"history": rows}
