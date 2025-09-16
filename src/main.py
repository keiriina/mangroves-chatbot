from fastapi import FastAPI
from pydantic import BaseModel
import cohere
import os
import dotenv
import pymupdf

dotenv.load_dotenv()
co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))
app = FastAPI()

def load_pdf(file_path: str) -> str:
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

pdf_text = load_pdf("../data/mangroves.pdf")

documents = [
    {
        "id": "mangrove-doc",
        "data": {
            "title": "Mangroves in the Philippines",
            "text": pdf_text
        }
    }
]

system_message = """## Task and Context
You are a speaker for the locals of a community that needs to conserve their mangrove systems.

## Style Guide
Speak in a way that can be easily understood by anyone, even people who are not expert in English. Be precise.
"""

messages = [{"role": "system", "content": system_message}]

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    global messages
    try:
        user_count = sum(1 for m in messages if m["role"] == "user")
        if user_count >= 10:
            return {"error": "Conversation limit reached (10 exchanges). Please start a new chat."}

        messages.append({"role": "user", "content": request.message})

        bot_reply = ""
        response = co.chat_stream(
            model="command-r-plus-08-2024",
            messages=messages,
            documents=documents
        )

        for event in response:
            if event.type == "content-delta":
                bot_reply += event.delta.message.content.text

        messages.append({"role": "assistant", "content": bot_reply})
        return {"response": bot_reply}
    except Exception as e:
        return {"error": str(e)}

@app.post("/reset")
def reset_conversation():
    global messages
    messages = [{"role": "system", "content": system_message}]
    return {"status": "Conversation reset"}
