"""
ChatUDP - Servidor
Recebe mensagens dos clientes e redistribui para todos (broadcast).
"""

import socket
import threading

HOST = "0.0.0.0"
PORT = 9090
BUFFER = 4096

# Dicionário de clientes: endereço -> apelido
clients: dict[tuple, str] = {}
lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))


def broadcast(message: str, exclude: tuple = None):
    """Envia uma mensagem para todos os clientes, exceto o remetente (opcional)."""
    data = message.encode("utf-8")
    with lock:
        for addr in list(clients):
            if addr != exclude:
                try:
                    server.sendto(data, addr)
                except Exception as e:
                    print(f"[ERRO ao enviar para {addr}]: {e}")


def handle_message(data: bytes, addr: tuple):
    """Processa cada mensagem recebida."""
    try:
        message = data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return

    # Registro de novo cliente: primeiro pacote deve ser "JOIN:<apelido>"
    if message.startswith("JOIN:"):
        nickname = message[5:].strip() or "Anônimo"
        with lock:
            clients[addr] = nickname
        print(f"[+] {nickname} entrou ({addr[0]}:{addr[1]})")
        broadcast(f"[Servidor] {nickname} entrou no chat!", exclude=addr)
        server.sendto(f"[Servidor] Bem-vindo, {nickname}!".encode("utf-8"), addr)
        return

    # Saída voluntária
    if message == "QUIT":
        with lock:
            nickname = clients.pop(addr, str(addr))
        print(f"[-] {nickname} saiu ({addr[0]}:{addr[1]})")
        broadcast(f"[Servidor] {nickname} saiu do chat.")
        return

    # Mensagem comum — cliente deve estar registrado
    with lock:
        nickname = clients.get(addr)

    if nickname is None:
        # Cliente não registrado: pede que faça JOIN primeiro
        server.sendto(b"[Servidor] Envie JOIN:<apelido> para entrar no chat.", addr)
        return

    formatted = f"[{nickname}] {message}"
    print(formatted)
    broadcast(formatted, exclude=addr)


def receive_loop():
    print(f"[Servidor] Ouvindo em {HOST}:{PORT} (UDP)")
    while True:
        try:
            data, addr = server.recvfrom(BUFFER)
            threading.Thread(target=handle_message, args=(data, addr), daemon=True).start()
        except Exception as e:
            print(f"[ERRO no loop principal]: {e}")


if __name__ == "__main__":
    try:
        receive_loop()
    except KeyboardInterrupt:
        print("\n[Servidor] Encerrando...")
        broadcast("[Servidor] O servidor foi encerrado.")
        server.close()
