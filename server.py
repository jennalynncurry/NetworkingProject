#!/usr/bin/env python3
"""
Chat Server for Client-Server Messaging System

Listens on a port, handles client connections, enforces unique usernames,
and supports real-time message forwarding between users. Includes support
for listing users, graceful exits, and offline message queuing.
"""

import socket
import threading
import argparse

# Dictionary to store active users
users = {}
# Dictionary to store offline messages
offline_messages = {}

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
                    client_socket.send("ERROR:Username already taken".encode())
                else:
                    username = requested_username
                    users[username] = client_socket
                    client_socket.send(f"Welcome {username}!".encode())

                    # Deliver offline messages if any
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
                    # Queue message for offline recipient
                    if recipient not in offline_messages:
                        offline_messages[recipient] = []
                    offline_messages[recipient].append(f"{username}: {msg}")
                    client_socket.send(f"{recipient} is offline. Your message has been saved.".encode())
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
    """Parses command-line arguments and starts the server."""
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument('--port', type=int, default=8080, help="Port to listen on")
    args = parser.parse_args()
    start_server(args.port)

if __name__ == "__main__":
    main()
