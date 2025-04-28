# Client-Server Chat System

## 📚 Overview

This project implements a real-time, push-based client-server chat system written in Python using sockets and threading. It allows multiple clients to connect to a server, register with a unique username, and exchange messages with other users. The system supports both private messages and chat rooms, with additional features like offline message queuing and command-line interaction.

---

## 🚀 How to Run

### 1. Start the Server

```bash
python3 final_server.py --port 8080
```

- The server will listen for incoming client connections on port 8080.
- Make sure to forward the port if you're using GitHub Codespaces or a cloud-based environment.

---

### 2. Start the Client

```bash
python3 final_client.py --host 127.0.0.1 --port 8080
```

- Replace `127.0.0.1` with your server’s IP address if connecting remotely.
- You’ll be prompted to enter a unique username. If it's taken, you'll need to choose a new one.

---

## 🗨️ Supported Features & Commands

### General Commands (outside chat rooms):
- `message` — Prompted to enter recipient and message
- `who` — Lists all active users
- `join <roomname>` — Joins (or creates) a chat room
- `exit` — Gracefully disconnects
- `leave` — Does nothing unless you're already in a room

### In a Chat Room:
- Any message you type is broadcast to the room
- `leave` — Leave the current chat room
- All other inputs are treated as chat (even `exit` and `who`)

---

## 💡 Special Features

### ✅ Offline Messaging
- If a user sends a message to someone who is **offline**, the server stores it.
- Once that recipient connects, any queued messages are delivered instantly.

### ✅ Chat Rooms
- Create or join rooms with `join <roomname>`
- Messages sent inside a room are broadcast to all room members
- Room entry/exit is announced automatically to others in the room
- Use `leave` to exit a room

---

## 🛠️ Implementation Overview

### Server
- Python sockets with multithreaded client handling
- Tracks users and rooms with dictionaries
- Handles direct messages, room messages, and offline queues
- Commands: `register`, `who`, `exit`, `join`, `leave`

### Client
- Dual-threaded: one for sending input, one for receiving messages
- Dynamic prompt updates based on whether you're in a chat room
- Graceful handling of disconnects and username conflicts

---

## 📸 Sample Flow

1. Alice joins room `teamchat`, Bob joins the same.
2. Alice types: `Hello team!`
3. Bob sees: `Alice (in teamchat): Hello team!`
4. Bob types `leave` → he exits the room
5. Alice sends Bob a private message: Bob will see it when he reconnects

---

## 📦 Project Structure

```
NetworkingProject/
├── final_server.py
├── final_client.py
├── README.md
└── screenshots/  # optional
```

---

## ✅ Final Notes

This project demonstrates core networking concepts like:
- TCP socket communication
- Multithreaded server design
- Command parsing
- Message routing and queuing
- Real-time updates in terminal UI

It's lightweight, extensible, and ideal for future upgrades (like TLS encryption or a GUI).
