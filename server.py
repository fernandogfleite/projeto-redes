import socket
import threading
import argparse

from coolname import generate_slug


def handle_client(client):
    while True:
        try:
            data = client['socket'].recv(1024)
            if not data:
                break

            message = data.decode()
            if message.startswith("salvar-nome:"):
                client_name = client['name']
                
                for c in clients:
                    if c == client:
                        new_name = message.replace("salvar-nome:", "").strip()
                        if new_name != "":
                            c['name'] = new_name
                        else:
                            invalid_name = True
                            c['socket'].send(f"Nome não pode ser vazio.".encode())
                            data = "Nome inválido".encode()
                        
                        break
                if not invalid_name:
                    data = f"Cliente {client_name} agora é {client['name']}".encode()
                    
                print(data.decode())
            else:
                data = f"{client['name']}: {message}".encode()
                print(f"Recebido: {message}")

            for c in clients:
                if c != client and data != "Nome inválido".encode():
                    c['socket'].send(data)
        except Exception as e:
            print(f"Erro: {str(e)}")
            break
    
    for c in clients:
        if c != client:
            c['socket'].send(f"{client['name']} desconectado.".encode())
    
    client_socket.close()
    clients.remove(client)
    
    print(f"Cliente {client['name']} desconectado.")
    
def parse_args():
    parser = argparse.ArgumentParser(description="Informar host, porta que o servidor deve escutar e número máximo de clientes")
    
    parser.add_argument("--host", "-H", required=True, help="Especificar o host")
    parser.add_argument("--port", "-P", required=True, type=int, help="Especificar a porta")
    parser.add_argument("--max-clients", "-M", required=False, type=int, default=3, help="Especificar o número máximo de clientes")
    
    args = parser.parse_args()
    
    return args.host, args.port, args.max_clients

host, port, max_clients = parse_args()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

print(f"Servidor de chat ativo em {host}:{port}")


clients = []

while True:
    client_socket, addr = server.accept()
    
    if len(clients) >= max_clients:
        client_socket.send("Servidor cheio.".encode())
        client_socket.close()
        
        continue
    
    print(f"Conexão aceita de {addr[0]}:{addr[1]}")
    
    name = generate_slug(2)
    client_socket.send(f"Bem-vindo ao chat, {name}.\n".encode())
    
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

    clients.append(client)

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
