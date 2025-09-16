# 🌱Mangroves Chatbot

This project is an AI-powered chatbot that uses Cohere and FastAPI to provide information about mangrove conservation in the Philippines. The chatbot is grounded on knowledge extracted from the included PDF file (mangroves.pdf) and responds in simple, clear English that can be understood by local communities.

## Set up

Set a virtual environment.
```bash
python -m venv .venv
.venv\Scripts\activate
```

Install Dependencies. The requirements.txt contains your other dependencies.
```
pip install -r requirements.txt
pip install PyMuPDF
```

Run uvicorn for FastAPI.
```
uvicorn main:app --reload
```
```
open the \docs endpoint in your browser
```
## Repository Contents  

---
**`chatbot_with_cohere_api.ipynb`**  
  Notebook where the chatbot logic was first developed and tested.  
  Includes experimentation with Cohere API and PDF text extraction.  

---
**`main.py`**  
  FastAPI application that wraps the chatbot into an API.  
  Provides two endpoints:  
  - `POST /chat` → send a message and receive a chatbot response.  
  - `POST /reset` → reset the conversation history.  

---
**`requirements.txt`**  
  List of dependencies needed to run the project (FastAPI, Cohere, PyMuPDF, Uvicorn).  

---
**`mangroves.pdf`**  
  Knowledge base containing information about mangroves in the Philippines.  
  The PDF is preloaded into memory and used as reference for chatbot responses.  

## Notes
- The chatbot has a conversation limit of 10 user exchanges.
- Restarting or resetting the conversation clears chat history but keeps the system instruction.
- PDF content (mangroves.pdf) is preloaded on server start and used as reference.

