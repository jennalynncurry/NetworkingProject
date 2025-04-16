# Client-Server Chat System

## 📚 Overview

This project implements a real-time, push-based client-server chat system written in Python using sockets and threading. It allows multiple clients to connect to a server, register with a unique username, and exchange messages with other users. The system is designed to be lightweight, responsive, and easy to test on a local network or using Codespaces.

---

## 🚀 How to Run

### 1. Start the Server

Run the server on your machine or Codespaces:

```bash
python3 server.py --port 8080
```

- The server will listen for incoming client connections on port 8080.
- Make sure to forward the port in Codespaces and bind to `0.0.0.0` if using two different machines. Use `localhost` if not.

---

### 2. Start the Client

On the same or another terminal (or machine):

```bash
python3 client.py --host 127.0.0.1 --port 8080
```

- Replace `127.0.0.1` with your server's IP if connecting from another computer.
- You’ll be prompted to enter a username. It must be unique.

---

## 🗨️ Supported Client Commands

- **`<recipient>:<message>`** – Sends `<message>` to `<recipient>`.
  - Example: `Bob:Hey there!`
- **`who`** – Lists all active users.
- **`exit`** – Gracefully disconnects from the server.

---

## 🛠️ Design and Implementation

### Server (`server.py`)
- Accepts multiple client connections using threads.
- Each client runs in its own thread and handles:
  - User registration (`server:register`)
  - Message routing (`<recipient>:<message>`)
  - Commands like `server:who` and `server:exit`
- Uses a shared dictionary `users = {username: socket}` to track connected clients.
- Prevents duplicate usernames and removes users cleanly on exit.

### Client (`client.py`)
- Connects to the server via IP and port.
- Prompts the user for a unique username and retries if it's already taken.
- Starts a background listener thread to print incoming messages in real-time.
- Main thread handles input and sends commands to the server.

### Threading Model
- Server uses threads for each client (non-blocking).
- Client uses a dual-thread model: one for sending, one for receiving messages.

---

## ✅ Example Workflow

1. Alice and Bob both run `client.py` and register usernames.
2. Alice types `Bob:Hi Bob!` — Bob immediately sees: `Alice: Hi Bob!`
3. Bob sends `server:who` — sees a list of active users.
4. Alice types `server:exit` — exits chat and her name disappears from the list.

---

## 🧪 Testing Tips

- Try running multiple clients at once.
- Attempt duplicate usernames to verify rejection.
- Use `server:who` and `server:exit` to test cleanup.
- Test across machines or through Codespaces with port forwarding enabled.

---

## 📦 Folder Structure

```
NetworkingProject/
├── client.py
├── server.py
├── README.md
└── screenshots/  (optional for report)
```

---

## 🧠 Final Thoughts

This system demonstrates key networking concepts like TCP sockets, concurrency with threading, and push-style communication. It’s designed to be simple, extensible, and adaptable to future features like group chat, offline messaging, or GUI integration.