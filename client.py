"""
ChatUDP - Cliente
Envia mensagens ao servidor e recebe broadcasts em tempo real.
Usa duas threads: uma para envio (input do usuário) e outra para recepção.
"""

import socket
import threading
import sys

BUFFER = 4096


def receive_loop(sock: socket.socket):
    """Thread dedicada a receber mensagens do servidor."""
    while True:
        try:
            data, _ = sock.recvfrom(BUFFER)
            message = data.decode("utf-8")
            # Imprime a mensagem recebida sem bagunçar a linha de digitação
            print(f"\r{message}\n> ", end="", flush=True)
        except OSError:
            # Socket foi fechado (saída do programa)
            break
        except Exception as e:
            print(f"\n[ERRO ao receber]: {e}")
            break


def main():
    # --- Configuração de conexão ---
    server_ip = input("IP do servidor (Enter para 127.0.0.1): ").strip() or "127.0.0.1"
    server_port_str = input("Porta do servidor (Enter para 9090): ").strip() or "9090"
    try:
        server_port = int(server_port_str)
    except ValueError:
        print("Porta inválida. Usando 9090.")
        server_port = 9090

    nickname = input("Seu apelido: ").strip()
    if not nickname:
        nickname = "Anônimo"

    server_addr = (server_ip, server_port)

    # --- Criação do socket ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Timeout de recepção para não travar na saída
    sock.settimeout(1.0)

    # --- Registro no servidor ---
    sock.sendto(f"JOIN:{nickname}".encode("utf-8"), server_addr)

    # --- Thread de recepção ---
    recv_thread = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
    recv_thread.start()

    print(f"\n[Chat] Conectado como '{nickname}'. Digite sua mensagem e pressione Enter.")
    print("[Chat] Digite /sair para encerrar.\n")

    # --- Loop de envio ---
    try:
        while True:
            print("> ", end="", flush=True)
            message = input()

            if message.strip().lower() in ("/sair", "/quit", "/exit"):
                sock.sendto(b"QUIT", server_addr)
                print("[Chat] Saindo...")
                break

            if message.strip() == "":
                continue

            sock.sendto(message.encode("utf-8"), server_addr)

    except KeyboardInterrupt:
        sock.sendto(b"QUIT", server_addr)
        print("\n[Chat] Saindo...")
    finally:
        sock.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
