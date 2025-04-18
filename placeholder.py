#!/usr/bin/env python3


"""
Chat Client for Client-Server Messaging System with TLS/SSL

Connects to a server, registers a unique username, and supports real-time
messaging between users. Handles message listening in a background thread.
"""
import socket
import ssl
import threading
import argparse

def listen_for_messages(client_socket: ssl.SSLSocket) -> None:
    """Continuously listens for messages from the server and prints them.

    Args:
        client_socket: The SSL socket connected to the server.
    """
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Connection to server closed.")
                break
            print(message)
    except Exception as e:
        print(f"Listener thread error: {e}")
    finally:
        client_socket.close()

def main() -> None:
    """Parses arguments and starts the chat client."""
    parser = argparse.ArgumentParser(description="Chat Client")
    parser.add_argument('--host', type=str, required=True, help="Server IP address")
    parser.add_argument('--port', type=int, default=8080, help="Server port number")
    args = parser.parse_args()

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("server.crt")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = context.wrap_socket(client_socket, server_hostname=args.host)
    ssl_socket.connect((args.host, args.port))

    # Register username
    while True:
        username = input("Enter your username: ").strip()
        ssl_socket.send(f"server:register {username}".encode())
        response = ssl_socket.recv(1024).decode()
        print(response)
        if not response.startswith("ERROR"):
            break

    # Start listening thread
    listener = threading.Thread(target=listen_for_messages, args=(ssl_socket,), daemon=True)
    listener.start()

    # Main loop for sending commands
    try:
        while True:
            command = input("Enter command (message, who, exit): ").strip().lower()
            if command == "message":
                recipient = input("Enter recipient username: ").strip()
                message = input("Enter your message: ").strip()
                ssl_socket.send(f"{recipient}:{message}".encode())
            elif command == "who":
                ssl_socket.send("server:who".encode())
            elif command == "exit":
                try:
                    ssl_socket.send("server:exit".encode())
                except BrokenPipeError:
                    print("Lost connection to server during exit.")
                break
            else:
                print("Unknown command. Please try again.")
    finally:
        ssl_socket.close()
        print("Disconnected from chat.")

if __name__ == "__main__":
    main()
