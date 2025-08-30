from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
import cohere
import os
import dotenv
import pymupdf

# env
dotenv.load_dotenv()
co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

# FastAPI app
app = FastAPI()

# extract PDF text
def load_pdf(file_path: str) -> str:
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# preload PDF into memory
pdf_text = load_pdf("mangroves.pdf")

# further improvements: maybe use not just one pdf source but 5 then set them up in a rag-based system.
documents = [
    {
        "id": "mangrove-doc",
        "data": {
            "title": "Mangroves in the Philippines",
            "text": pdf_text
        }
    }
]

# System message
system_message = """## Task and Context
You are a speaker for the locals of a community that needs to conserve their mangrove systems.

## Style Guide
Speak in a way that can be easily understood by anyone, even people who are not expert in English. Be precise.
"""

# Conversation state
conversation = [
    {
        "role": "system",
        "content": system_message
    }
]

# data validation
class ChatRequest(BaseModel):
    message: str

 # chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    global messages

    # Limit convo to 10 user exchanges
    user_count = sum(1 for m in messages if m["role"] == "user")
    if user_count >= 10:
        return {"error": "Conversation limit reached (10 exchanges). Please start a new chat."}

    # Append user message
    messages.append({"role": "user", "content": request.message})

    # generate
    bot_reply = ""
    response = co.chat_stream(
        model="command-r-plus-08-2024",
        messages=messages,
        documents=documents
    )

    for event in response:
        if event.type == "content-delta":
            bot_reply += event.delta.message.content.text

    # Save bot response to convo history
    messages.append({"role": "assistant", "content": bot_reply})

    return {"response": bot_reply}

# clear convo history
@app.post("/reset")
def reset_conversation():
    """Reset conversation history."""
    global messages
    messages = [{"role": "system", "content": system_message}]
    return {"status": "Conversation reset"}
