# Projeto de Redes de Computadores

## Requisitos
- [Python 3.10.9](https://www.python.org/downloads/release/python-3109/)

## Como executar



- Clone o repositório
```bash
git clone git@github.com:fernandogfleite/projeto-redes.git # SSH
```
```bash
git clone https://github.com/fernandogfleite/projeto-redes.git # HTTPS
```

- Entre na pasta do projeto
```bash
cd projeto-redes
```

- Crie um ambiente virtual
```bash
python -m venv venv 
```

- Ative o ambiente virtual
```bash
source venv/bin/activate # Linux
```
```bash
venv\Scripts\activate # Windows
```

- Instale as dependências
```bash
pip install -r requirements.txt
```

- Abra um terminal e execute o servidor
```bash
python server.py --host <host> --port <porta> --max-clients <maximo de clientes>
```
```bash
python server.py -H <host> -P <porta> -M <maximo de clientes> # Versão simplificada do comando
```

- Abra outros terminais e execute o cliente
```bash
python client.py --host <host> --port <porta>
```
```bash
python client.py -H <host> -P <porta> # Versão simplificada do comando
```

- Durante a execução do cliente é possível enviar mensagens no chat, alterar o nome de usuário e sair do chat
```bash
# Enviar mensagem
<mensagem>

# Alterar nome de usuário
/name <novo nome>

# Sair do chat
/quit
```