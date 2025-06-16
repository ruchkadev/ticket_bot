# Telegram Ticket Bot + FastAPI Landing Page

This project is a simple Telegram bot that collects a user's name and phone number, generates a unique ticket with a QR code, and displays it on a landing page powered by FastAPI.

---

## Features

- Collects name and phone number via a Telegram bot  
- Generates a unique ticket ID and a QR code with a link to the ticket  
- Saves user data to a local JSON file  
- Displays a nicely styled ticket page with a QR code using FastAPI  

---

## Setup

In the `bot.py` file, locate the `TOKEN` variable (line 59) and replace it with your actual Telegram bot token:

```python
TOKEN = "YOUR_BOT_TOKEN"
```

---

## Running the Project

1. Start the FastAPI server using uvicorn:

```bash
uvicorn web:app --reload
```

2. In a separate terminal, run the Telegram bot:

```bash
python bot.py
```

---

## How to Use

- Open Telegram and find your bot  
- Send the `/start` command  
- Follow the instructions: enter your name and phone number  
- Receive a QR code and a link to your personal ticket  
- Open the link to view your ticket on the landing page  

---

## Project Structure

```
.
├── bot.py               # Telegram bot logic, ticket and QR generation
├── web.py               # FastAPI app that serves the ticket page
├── templates/
│   └── ticket.html      # HTML template for the ticket
├── database.json        # User data storage
└── tickets/
    └── qr/              # Folder with generated QR codes
```

---

## License

MIT License
