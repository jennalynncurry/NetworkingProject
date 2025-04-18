#!/usr/bin/env python3
"""
Chat Client for Client-Server Messaging System
"""

import socket
import threading
import argparse

def listen_for_messages(client_socket: socket.socket) -> None:
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
    parser = argparse.ArgumentParser(description="Chat Client")
    parser.add_argument('--host', type=str, required=True, help="Server IP address")
    parser.add_argument('--port', type=int, default=8080, help="Server port number")
    args = parser.parse_args()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.host, args.port))

    current_room = None

    while True:
        username = input("Enter your username: ").strip()
        client_socket.send(f"server:register {username}".encode())
        response = client_socket.recv(1024).decode()
        print(response)
        if not response.startswith("ERROR"):
            break

    listener = threading.Thread(target=listen_for_messages, args=(client_socket,), daemon=True)
    listener.start()

    try:
        while True:
            prompt = f"[{current_room}] > " if current_room else "Enter command (message, who, exit, join <room>, leave): "
            command = input(prompt).strip()

            if not current_room:
                if command == "who":
                    client_socket.send("server:who".encode())
                elif command == "exit":
                    try:
                        client_socket.send("server:exit".encode())
                    except BrokenPipeError:
                        print("Lost connection to server during exit.")
                    break
                elif command.startswith("join "):
                    room_name = command.split(" ", 1)[1]
                    client_socket.send(f"server:join {room_name}".encode())
                    current_room = room_name
                elif command == "leave":
                    client_socket.send("server:leave".encode())
                elif command == "message":
                    recipient = input("Enter recipient username: ").strip()
                    msg = input("Enter your message: ").strip()
                    client_socket.send(f"{recipient}:{msg}".encode())
                elif ":" in command:
                    client_socket.send(command.encode())
                else:
                    print("Unknown command outside room. Try 'message', 'join <room>', or 'exit'.")
            else:
                if command == "leave":
                    client_socket.send("server:leave".encode())
                    current_room = None
                else:
                    client_socket.send(command.encode())
    finally:
        client_socket.close()
        print("Disconnected from chat.")

if __name__ == "__main__":
    main()