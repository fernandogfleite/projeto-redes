import socket
import threading
import os

import argparse

exit_signal = threading.Event()

def send_message(client_socket):
    while not exit_signal.is_set():
        message = input("")
        if message == "/quit":
            exit_signal.set()
            break
        client_socket.send(message.encode())
        

def parse_args():
    parser = argparse.ArgumentParser(description="Informar host e porta do servidor a ser conectado")
    
    parser.add_argument("--host", "-H", required=True, help="Especificar o host")
    parser.add_argument("--port", "-P", required=True, type=int, help="Especificar a porta")
    
    args = parser.parse_args()
    
    return args.host, args.port
    

def main(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(1)
    client.connect((host, port))
    
    message_thread = threading.Thread(target=send_message, args=(client,))
    message_thread.start()

    while not exit_signal.is_set():
        try:
            data = client.recv(1024)
            if not data:
                print("Servidor desconectado.")
                os._exit(0)
            message = data.decode()
            print(message)
        except socket.timeout:
            continue

    client.close()
    
if __name__ == "__main__":
    host, port = parse_args()
    main(host, port)