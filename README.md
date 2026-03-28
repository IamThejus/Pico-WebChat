# 💬 Pico WebChat

🔴 **Live Demo:** [pico-webchat-8ae310cf.fastapicloud.dev](https://pico-webchat-8ae310cf.fastapicloud.dev/)

A real-time full-stack chat application built with **FastAPI**, **WebSockets**, and **Supabase** — featuring public group chat, private messaging, and **Pico**, a persistent AI companion powered by Groq (LLaMA 3.1).

---

## ✨ Features

- **Public Chat** — Group chat room with message history persisted in Supabase
- **Private Messaging** — Mini popup chat windows between online users
- **Pico AI** — Per-user AI chatbot with persistent memory across sessions (powered by Groq + LLaMA 3.1 8B)
- **Real-time WebSockets** — Instant messaging with auto-reconnect on disconnect
- **JWT Auth + Cookie Middleware** — Session management via HTTP-only cookies
- **Active Users List** — Live sidebar showing who's online

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, Python |
| Real-time | WebSockets (native FastAPI) |
| Database | Supabase (PostgreSQL) |
| AI | Groq API — LLaMA 3.1 8B Instant |
| Auth | JWT (PyJWT) + Cookie middleware |
| Frontend | Vanilla JS, HTML/CSS |

---

## 📁 Project Structure

```
Pico-WebChat/
├── main.py                  # FastAPI app entry point
├── supermiddleware.py       # Cookie/auth middleware
├── routers/
│   ├── api.py               # REST API routes
│   └── websockets.py        # WebSocket endpoints
├── tools/
│   ├── superdb.py           # Supabase DB operations
│   ├── pico_ai.py           # Pico AI (Groq client + system prompt)
│   ├── superjwt.py          # JWT encode/decode
│   ├── superhasher.py       # Password hashing (pwdlib)
│   ├── socket_pico_connections.py  # Active connection state
│   └── models.py            # Pydantic models
├── static/
│   └── script.js            # Frontend WebSocket logic
└── templates/
    ├── login.html
    └── chat.html
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/Pico-WebChat.git
cd Pico-WebChat
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn supabase python-dotenv groq pyjwt pwdlib
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
api_key=your_groq_api_key
```

### 4. Set up Supabase tables

Run the following SQL in your Supabase SQL editor:

```sql
-- Users
create table users (
  id serial primary key,
  username text unique not null,
  password text not null
);

-- Public chat
create table publicchat (
  id serial primary key,
  username text not null,
  message text not null,
  created_at timestamptz default now()
);

-- Private chat
create table privatechat (
  id serial primary key,
  sender text not null,
  receiver text not null,
  message text not null,
  created_at timestamptz default now()
);

-- Pico AI memory
create table pico (
  id serial primary key,
  username text unique not null,
  chat_history jsonb default '[]'
);
```

### 5. Run the app

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000`

---

## 🤖 About Pico

Pico is a built-in AI assistant unique to each user. It remembers your conversation history across sessions (stored in Supabase) and has a distinct personality — casual, witty, and genuinely engaging. Just click **PICO** in the online users list to start a chat.

---

## 📸 Screenshots

<img width="100%" alt="Entry Page" src="https://github.com/user-attachments/assets/4e946d20-f9e8-4fb0-8d4d-4e18e1f7698f" />

<table>
  <tr>
    <td><img alt="Public Chat" src="https://github.com/user-attachments/assets/f2468f40-0aac-4108-96f9-92292e0c70f3" /></td>
    <td><img alt="Main Chat" src="https://github.com/user-attachments/assets/4220eb2d-a156-4853-b5d7-fdf3011739ef" /></td>
  </tr>
  <tr>
    <td><img alt="Private Chat" src="https://github.com/user-attachments/assets/a3a329fb-b35b-478f-a933-0a7235c6f7ed" /></td>
    <td><img alt="Pico AI" src="https://github.com/user-attachments/assets/6c1bca27-3873-4f83-9ad3-529d1f9c32fa" /></td>
  </tr>
</table>

---

## 🚀 Deployment

This app can be deployed on any platform that supports Python + WebSockets, such as **Railway**, **Render**, or **Fly.io**. Make sure to set your environment variables in the platform's dashboard.

---

## 📄 License

MIT License — feel free to use and build on this project.
