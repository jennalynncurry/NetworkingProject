import socket
import threading
import argparse

# Dictionary to store active users
users = {}

def handle_client(client_socket, address):
    try:
        username = None
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                if message.startswith("server:register"):
                    username = message.split()[1]
                    if username in users:
                        client_socket.send("Username already taken. Try another one.".encode()) #need to fix this so that it enforces
                    else:
                        users[username] = client_socket
                        client_socket.send(f"Welcome {username}!".encode())
                elif message.startswith("server:who"):
                    active_users = ", ".join(users.keys())
                    client_socket.send(f"Active users: {active_users}".encode())
                elif message.startswith("server:exit"):
                    if username:
                        del users[username]
                    client_socket.send("Goodbye!".encode())
                    break
                else:
                    recipient, msg = message.split(":", 1)
                    if recipient in users:
                        users[recipient].send(f"{username}: {msg}".encode())
                    else:
                        client_socket.send("Recipient not found.".encode())
    finally:
        if username and username in users:
            del users[username]
        client_socket.close()

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen()
    print(f"Server listening on port {port}")

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

def main():
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    start_server(args.port)

if __name__ == "__main__":
    main()