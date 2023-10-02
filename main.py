import socket
import threading

from coolname import generate_slug


# Função para lidar com a comunicação de um cliente
def handle_client(client):
    while True:
        try:
            # Recebe dados do cliente
            data = client['socket'].recv(1024)
            if not data:
                break

            # Exibe a mensagem recebida para todos os clientes conectados
            message = data.decode()
            if "salvar-nome:" in message:
                client_name = client['name']
                for c in clients:
                    if c == client:
                        c['name'] = message.replace("salvar-nome:", "").strip()
                        break
                data = f"Cliente {client_name} agora é {client['name']}".encode()
                print(data.decode())
            else:
                data = f"{client['name']}: {message}".encode()
                print(f"Recebido: {message}")

            # Reenvia a mensagem para todos os clientes
            for c in clients:
                if c != client:
                    c['socket'].send(data)
        except Exception as e:
            print(f"Erro: {str(e)}")
            break
    
    for c in clients:
        c['socket'].send(f"{client['name']} desconectado.".encode())
    
    # Fecha a conexão com o cliente
    client_socket.close()
    clients.remove(client)
    
    print(f"Cliente {client['name']} desconectado.")
    

# Configurações do servidor
host = "127.0.0.1"
port = 12346

# Cria um socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liga o servidor ao endereço e porta especificados
server.bind((host, port))

# Começa a escutar por conexões entrantes
server.listen(5)

print(f"Servidor de chat ativo em {host}:{port}")

# Lista para armazenar todas as conexões de clientes
clients = []


while True:
    client_socket, addr = server.accept()
    
    if len(clients) >= 1:
        client_socket.send("Servidor cheio.".encode())
        client_socket.close()
        continue
    
    print(f"Conexão aceita de {addr[0]}:{addr[1]}")
    
    name = generate_slug(2)
    client_socket.send(f"Ben-vindo ao chat, {name}.".encode())
    
    for c in clients:
        c['socket'].send(f"{name} conectado.".encode())
    
    client = {
        "socket": client_socket,
        "name": name
    }
    
    if len(clients) > 0:
        clients_online = "Clientes online: \n"
        for c in clients:
            clients_online += f"{c['name']}\n"
        client_socket.send(clients_online.encode())

    # Adiciona o cliente à lista de clientes
    clients.append(client)

    # Inicia uma thread para lidar com a comunicação do cliente
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()