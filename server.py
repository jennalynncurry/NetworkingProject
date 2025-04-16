#!/usr/bin/env python3
"""
Chat Server for Client-Server Messaging System

Listens on a port, handles client connections, enforces unique usernames,
and supports real-time message forwarding between users. Includes support
for listing users and graceful exits.
"""

import socket
import threading
import argparse
import random
import string

# Dictionary to store active users
users = {}

def generate_unique_username(base_name: str) -> str:
    """Appends a random string to create a unique username.

    Args:
        base_name: Desired base username.

    Returns:
        A modified username guaranteed to be unique.
    """
    while True:
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        new_username = f"{base_name}_{suffix}"
        if new_username not in users:
            return new_username

def handle_client(client_socket: socket.socket, address: tuple[str, int]) -> None:
    """Handles communication with a connected client.

    Args:
        client_socket: The socket connected to the client.
        address: The client's address as a (host, port) tuple.
    """
    username = None
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message.startswith("server:register"):
                requested_username = message.split()[1]
                if requested_username in users:
                    unique_username = generate_unique_username(requested_username)
                    username = unique_username
                    users[username] = client_socket
                    client_socket.send(f"Username taken. You are registered as {username}".encode())
                else:
                    username = requested_username
                    users[username] = client_socket
                    client_socket.send(f"Welcome {username}!".encode())

            elif not username:
                client_socket.send("ERROR:You must register a username first.".encode())
                continue

            elif message.startswith("server:who"):
                active_users = ", ".join(users.keys())
                client_socket.send(f"Active users: {active_users}".encode())

            elif message.startswith("server:exit"):
                client_socket.send("Goodbye!".encode())
                break

            else:
                if ":" not in message:
                    client_socket.send("ERROR:Invalid message format.".encode())
                    continue

                recipient, msg = message.split(":", 1)
                if recipient in users:
                    try:
                        users[recipient].send(f"{username}: {msg}".encode())
                    except Exception:
                        client_socket.send("ERROR:Failed to send message.".encode())
                else:
                    client_socket.send("ERROR:Recipient not found.".encode())
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        if username in users:
            del users[username]
        client_socket.close()

def start_server(port: int) -> None:
    """Starts the server and listens for incoming client connections.

    Args:
        port: Port number to bind the server socket to.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
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
    """Parses command-line arguments and starts the server."""
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument('--port', type=int, default=8080, help="Port to listen on")
    args = parser.parse_args()
    start_server(args.port)

if __name__ == "__main__":
    main()
