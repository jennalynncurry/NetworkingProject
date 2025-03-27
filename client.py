import socket
import threading
import argparse

def listen_for_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except:
            print("An error occurred. Exiting...")
            client_socket.close()
            break

def main():
    parser = argparse.ArgumentParser(description="Chat Client")
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.host, args.port))

    username = input("Enter your username: ")
    client_socket.send(f"server:register {username}".encode())

    threading.Thread(target=listen_for_messages, args=(client_socket,)).start()

    while True:
        command = input("Enter command (message, who, exit): ").strip().lower()
        if command == "message":
            recipient = input("Enter recipient username: ").strip()
            message = input("Enter your message: ").strip()
            client_socket.send(f"{recipient}:{message}".encode())
        elif command == "who":
            client_socket.send("server:who".encode())
        elif command == "exit":
            client_socket.send("server:exit".encode())
            break
        else:
            print("Unknown command. Please try again.")

    client_socket.close()

if __name__ == "__main__":
    main()