import os
from fastapi import FastAPI, HTTPException
from groq import Groq
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise Exception("no api key found")
client = Groq(api_key=groq_api_key)

chat_history = []
custom_promts = ["who are you", "who made you"]
custom_reply = "I’m your helpful AI assistant built by Wajahath Ali with the loving name of his brother Zeeshan."

class ChatRequest(BaseModel):
    message:str
def get_user_message(user_message, stream=False):
    chat_history.append({"role": "user", "content": user_message})
    chat_completion = client.chat.completions.create(
        messages=chat_history,
        model="llama-3.3-70b-versatile",
        stream=stream,
    )
    reply =  chat_completion.choices[0].message.content

    chat_history.append({"role": "assistant", "content": reply})
    return reply

@app.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    try:
        user_message = request.message.lower().strip()
        if any(user_message == p for p in custom_promts):
            return {"Zeeshu AI" : custom_reply}
        
        reply = get_user_message(request.message)
        return {"Zeeshu AI" : reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
       