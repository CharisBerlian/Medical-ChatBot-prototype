from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from auth import init_auth_db, register_user, login_user
init_auth_db()

# Load environment variables
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


app = FastAPI(title="Medical Chatbot API")

# Request/Response Models
class Message(BaseModel):
    text: str

class ChatResponse(BaseModel):
    reply: str

# Root endpoint
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Medical Chatbot API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                code { background: #f4f4f4; padding: 2px 6px; }
                pre { background: #f4f4f4; padding: 10px; border-left: 3px solid #ccc; }
            </style>
        </head>
        <body>
            <h1>🩺 Medical Chatbot API</h1>
            <p>Use <code>/chat</code> POST endpoint for consultations:</p>
            <pre>
curl -X POST http://127.0.0.1:8000/chat \\
-H "Content-Type: application/json" \\
-d '{"text":"What are flu symptoms?"}'
            </pre>
            <p>Or use the <a href="/docs">Swagger docs</a> for testing.</p>
        </body>
    </html>
    """

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(msg: Message):
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a medical assistant. Provide general health information and always recommend consulting a real doctor for serious concerns."
                },
                {
                    "role": "user",
                    "content": msg.text
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1024
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"DeepSeek API error: {response.text}"
            )
            
        reply = response.json()["choices"][0]["message"]["content"]
        return {"reply": reply}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"API request failed: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "deepseek-chat"}


# Add these models
class Reminder(BaseModel):
    medication: str
    dosage: str
    time: str  # Format: "HH:MM"
    days: list[str]  # e.g., ["Mon", "Wed", "Fri"]

# In-memory storage (replace with database later)
reminders_db = []

@app.post("/add-reminder")
async def add_reminder(reminder: Reminder):
    reminders_db.append(reminder.dict())
    return {"message": "Reminder set successfully"}

@app.get("/get-reminders")
async def get_reminders():
    return {"reminders": reminders_db}

class UserCredentials(BaseModel):
    username: str
    password: str
    
@app.post("/register")
async def register(credentials: UserCredentials):
    if register_user(credentials.username, credentials.password):
        return {"message": "Registration successful"}
    else:
        raise HTTPException(status_code=400, detail="Username already exists")

@app.post("/login")
async def login(credentials: UserCredentials):
    if login_user(credentials.username, credentials.password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

