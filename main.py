from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_text()
        name1, name2 = data.split(",")

        compatibility = random.randint(0, 100)
        
        if compatibility > 80:
            message = f"💖 {name1} and {name2} are a perfect match! 💕"
        elif compatibility > 50:
            message = f"😍 {name1} and {name2} have a strong connection! 🔥"
        elif compatibility > 30:
            message = f"😊 There's potential for {name1} and {name2}! 💌"
        else:
            message = f"💔 {name1} and {name2} might just be better as friends."

        response = {
            "name1": name1,
            "name2": name2,
            "compatibility": f"{compatibility}%",
            "message": message
        }

        await websocket.send_json(response)
