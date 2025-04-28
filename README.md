<<<<<<< HEAD
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
=======
# NetworkingProject
Format: you are expected to submit the source code and an experiment report that reflects
the key steps of the execution of your code. Your code should follow the google
programming guidelines [1], clear and detailed comments of the code are appreciated. For
the experiment report, you need to follow the guidelines of Indiana University [2], you
should also include the description of how to execute your code.
When submit your project files, you should put all your code and file in a folder,
and name the folder as the following naming conventions:
➢ class_name-your_name-team_number-student_number-date
2. Project Details
1. Overview
This project implements a simple push-style client-server chat application for a local
network. The system allows multiple clients to connect to a single server, register
unique usernames, and exchange messages in real-time. The server immediately
pushes messages to recipients without requiring periodic polling.
Key Features
• User Registration: Enforces a unique username for each client.
• Real-Time Message Delivery: Messages are “pushed” from the server to the
recipient as soon as they are sent.
• Online User List: Clients can request a list of all currently active users.
• Graceful Exit: Clients can disconnect cleanly, notifying the server so their username
is freed and no longer displayed.
2. Architecture and Components
2.1 Server
• Port Listening
o Listens on a designated port (e.g., 8080) for incoming connections.
• Threaded Connections
o Spawns a new thread for each client connection, allowing concurrent
handling of multiple clients.
• User Management
o Maintains a dictionary (or map) of active username → socket.
o Ensures usernames are unique. If a requested username is taken, the server
rejects it.
• Real-Time Push
o On receiving a message destined for <recipient>, the server immediately
calls recipient_socket.send(...).
• Commands Handling
o Registration: Processes a registration command (e.g., server:register
<username>).
o List Users: Responds to a request for who is online (e.g., server:who).
o Exit: Handles user exit, removing the user’s entry from the dictionary and
closing the socket.
2.2 Client
• Connection
o Connects to the server using the server’s IP/hostname and port.
• Username Prompt
o Requests a username from the user (e.g., Alice) upon startup.
o Sends a registration command to the server to claim that username.
• Two-Thread Model
0. Main Thread: Waits for console input (input()) to parse commands and
send data to the server.
1. Listener Thread: Continuously listens on the socket for incoming messages
and prints them immediately to the user’s console.
• Supported Commands
o <recipient>:<message> – Sends <message> to <recipient>.
o server:who – Requests a list of online users from the server.
o server:exit – Gracefully disconnects from the server, closing the socket
and freeing the username.
3. Detailed Requirements
3.1 User Registration
• Client
o Prompt user for a username at launch.
o Send a registration request to the server (e.g., server:register
<username>).
• Server
o Validates uniqueness of the username.
o If accepted, records <username, socket> in its dictionary.
o If the username is already taken, instructs the client to pick a different name.
3.2 Real-Time (Push) Message Delivery
• Server
o Upon receiving <recipient>:<message> from a client, immediately
locates <recipient> in the dictionary.
o If <recipient> is online, calls recipient_socket.send(...) to push
the message.
o If <recipient> is offline, informs the sender that delivery failed (or queues
the message, if desired).
• Client
o The listener thread prints messages as soon as they arrive, without any
polling logic.
3.3 Online User List
• Client
o Sends server:who to request the current list of active users.
o The listener thread displays the received list.
• Server
o Replies with a formatted list of currently registered usernames.
3.4 Graceful Exit
• Client
o User types server:exit to disconnect.
o Notifies the server of the exit request, then closes the socket.
• Server
o Removes the user from the internal dictionary.
o Alerts other users if necessary (optional).
4. Implementation Details
1. Imports
o Use Python’s built-in libraries: socket, threading, argparse (optional
for command-line arguments).
2. Server Module (e.g., server.py)
o Parse Arguments: --port <port_number> for specifying the listening
port.
o Start Server Socket: server_socket =
socket.socket(socket.AF_INET, socket.SOCK_STREAM) then
bind() and listen().
o Connection Loop: In a loop, accept() new client connections and spawn a
thread to handle each client.
o Client Handler: The thread responsible for:
▪ Parsing registration commands (server:register).
▪ Storing/validating usernames.
▪ Handling message forwarding.
▪ Responding to server:who and server:exit.
o Data Structures:
▪ users = {username: client_socket, ...} for active users.
3. Client Module (e.g., client.py)
o Parse Arguments: --host <server_ip> and --port <port_number>
if desired.
o Establish Connection: Create a socket and connect() to the server.
o User Registration: Prompt for username and send server:register
<username>.
o Listener Thread: Continuously reads from the socket and prints any
incoming messages to the console.
o Main Loop: Reads user input. Depending on the format
(<recipient>:<message>, server:who, server:exit), sends the
appropriate command to the server.
5. Usage Instructions
1. Start the Server
python server.py --port 8080
o The server will begin listening on localhost:8080.
2. Start a Client
python client.py --host server_ip --port 8080
o When prompted, enter a username, e.g., Alice.
o If the username is accepted, you can begin sending messages.
3. Sending a Message
o In the client console, type <recipient>:<message>, e.g.:
Bob:Hello Bob!
o Bob’s client will immediately display Alice: Hello Bob!.
4. Checking Who’s Online
o Enter server:who in the client console.
o The server responds with a list of currently online users.
5. Exiting
o Type server:exit.
o The client notifies the server that you are disconnecting, then closes.
6. Possible Extensions (Optional)
• Offline Messaging / Message Queues
o Store messages for users who are offline and deliver them once they
reconnect.
• Encryption
o Integrate TLS/SSL or other encryption libraries to secure messages in transit.
• Private Group Chat or Chat Rooms
o Extend the server logic to handle group chat sessions with multiple
recipients.
• User Authentication
o Require a password for username registration to enhance security.
• Graphical User Interface (GUI)
o Replace or supplement the command-line interface with a simple GUI using
libraries like tkinter.
3. Submission Requirements
• Source Code:
Submit all source files along with any scripts needed to set up the virtual
environment.
• Documentation:
Include a README file with instructions on how to run your project and a brief
report describing your design and implementation decisions.
• Testing Evidence:
Provide evidence (screenshots or video recording) showing that your chat system
works as expected in the virtual environment.
4. Evaluation
Performance Levels:
• Excellent (90-100% of points)
o Fully meets requirements, shows strong understanding, robust and well-tested
implementation, code is very clean and well-documented.
• Good (80-89%)
o Meets most requirements with minor issues or omissions, code is mostly
clean, only a few bugs or documentation gaps.
• Needs Improvement (70-79%)
o Partially meets requirements, some notable bugs or missing features, code is
somewhat disorganized or under-documented.
• Incomplete (<70%)
o Fails to meet a significant number of requirements, has major errors or is
non-functional in key areas, documentation is insufficient.
>>>>>>> edf14c5e1b794b5b70177a8690de365d252eb6d2
