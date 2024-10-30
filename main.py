import os
from fastapi import FastAPI, Request, Form,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chatbot import handle_chat_query

app = FastAPI()

# Mount the 'static' directory to serve CSS and JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Serve the homepage with the form for the chatbot
    return templates.TemplateResponse("index.html", {"request": request})

# Load the secret key from the environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

# Define a Pydantic model to validate the request body
class ChatRequest(BaseModel):
    user_input: str

@app.post("/chatbot")
async def chat_route(request: Request, chat_request: ChatRequest):
    # Extract the secret key from the request headers
    client_secret = request.headers.get('X-SECRET-KEY')

    # Check if the secret key is valid
    if client_secret != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized access. Invalid secret key.")

    # Process the chat request using chatbot.py logic
    user_input = chat_request.user_input
    chatbot_response = await handle_chat_query(user_input)

    # Return the chatbot response as JSON
    return {"response": chatbot_response}