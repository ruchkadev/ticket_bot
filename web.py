from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path

app = FastAPI()

# Путь к базе и QR-кодам
DB_FILE = 'database.json'
QR_FOLDER = Path('tickets/qr')

app.mount("/qr", StaticFiles(directory=QR_FOLDER), name="qr")

templates = Jinja2Templates(directory="templates")

@app.get("/u/{user_id}")
async def ticket_page(request: Request, user_id: str):
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {}

    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    qr_url = f"/qr/{user_id}.png"

    return templates.TemplateResponse("ticket.html", {"request": request, "user": user, "qr_url": qr_url})
