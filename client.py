import socket
import threading
import os


exit_signal = threading.Event()

# Função para lidar com a entrada de mensagens do usuário
def send_message(client_socket):
    while not exit_signal.is_set():
        message = input("")
        if message == "quit":
            exit_signal.set()
            break
        client_socket.send(message.encode())

# Configurações do cliente
host = "127.0.0.1"  # O mesmo IP que o servidor
port = 12346       # A mesma porta que o servidor

# Cria um socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.settimeout(1)

# Conecta-se ao servidor
client.connect((host, port))


# Inicia uma thread para enviar mensagens
message_thread = threading.Thread(target=send_message, args=(client,))
message_thread.start()

# Recebe e exibe mensagens do servidor
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