#!/usr/bin/env python3
"""
Chat Server for Client-Server Messaging System

Listens on a port, handles client connections, enforces unique usernames,
and supports real-time message forwarding between users. Includes support
for listing users, graceful exits, offline message queuing, and chat rooms.
"""

import socket
import threading
import argparse

users = {}
offline_messages = {}
user_rooms = {}
chat_rooms = {}

def broadcast_to_room(sender, message):
    room = user_rooms.get(sender)
    if not room:
        return
    for user in chat_rooms.get(room, set()):
        if user != sender and user in users:
            try:
                users[user].send(f"{sender} (in {room}): {message}".encode())
            except Exception:
                pass

def handle_client(client_socket: socket.socket, address: tuple[str, int]) -> None:
    username = None
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message.startswith("server:register"):
                requested_username = message.split()[1]
                if requested_username in users:
                    client_socket.send("ERROR:Username already taken".encode())
                else:
                    username = requested_username
                    users[username] = client_socket
                    client_socket.send(f"Welcome {username}!".encode())

                    if username in offline_messages:
                        for msg in offline_messages[username]:
                            client_socket.send(msg.encode())
                        del offline_messages[username]

            elif not username:
                client_socket.send("ERROR:You must register a username first.".encode())
                continue

            elif message.startswith("server:who"):
                active_users = ", ".join(users.keys())
                client_socket.send(f"Active users: {active_users}".encode())

            elif message.startswith("server:exit"):
                client_socket.send("Goodbye!".encode())
                break

            elif message.startswith("server:join"):
                room_name = message.split()[1]
                if username in user_rooms:
                    old_room = user_rooms[username]
                    chat_rooms[old_room].discard(username)
                    broadcast_to_room(username, "has left the room.")
                    if not chat_rooms[old_room]:
                        del chat_rooms[old_room]
                chat_rooms.setdefault(room_name, set()).add(username)
                user_rooms[username] = room_name
                client_socket.send(f"Joined room: {room_name}".encode())
                broadcast_to_room(username, "has joined the room.")

            elif message.startswith("server:leave"):
                if username in user_rooms:
                    room = user_rooms.pop(username)
                    chat_rooms[room].discard(username)
                    broadcast_to_room(username, "has left the room.")
                    if not chat_rooms[room]:
                        del chat_rooms[room]
                    client_socket.send(f"You have left the room {room}".encode())
                else:
                    client_socket.send("You are not in any room.".encode())

            else:
                if ":" in message:
                    recipient, msg = message.split(":", 1)
                    if recipient in users:
                        try:
                            users[recipient].send(f"{username}: {msg}".encode())
                        except Exception:
                            client_socket.send("ERROR:Failed to send message.".encode())
                    else:
                        offline_messages.setdefault(recipient, []).append(f"{username}: {msg}")
                        client_socket.send(f"{recipient} is offline. Your message has been saved.".encode())
                else:
                    if username in user_rooms:
                        broadcast_to_room(username, message)
                    else:
                        client_socket.send("ERROR:No recipient or room. Use <user>:<msg> or join a room.".encode())
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        if username in users:
            del users[username]
        if username in user_rooms:
            room = user_rooms.pop(username)
            chat_rooms[room].discard(username)
            if not chat_rooms[room]:
                del chat_rooms[room]
        client_socket.close()

def start_server(port: int) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen()
    print(f"Server listening on port {port}")
    while True:
        try:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break
    server_socket.close()

def main() -> None:
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument('--port', type=int, default=8080, help="Port to listen on")
    args = parser.parse_args()
    start_server(args.port)

if __name__ == "__main__":
    main()
