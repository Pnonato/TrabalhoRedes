# ChatUDP 💬

Aplicação de chat em tempo real usando **sockets UDP** e **Python**.  
Desenvolvida como trabalho prático da disciplina de Redes de Computadores.

---

## Como funciona

- O **servidor** fica aguardando mensagens na porta `9090`.
- Cada **cliente** se registra com um apelido e pode enviar mensagens para todos os outros.
- O servidor faz o **broadcast**: redistribui cada mensagem recebida para todos os clientes conectados.
- A comunicação usa **UDP** — sem conexão, leve e direto ao ponto.

```
Cliente A  ──►  Servidor UDP  ──►  Cliente B
                    │
                    └──────────►  Cliente C
```

---

## Pré-requisitos

- Python 3.8 ou superior
- Sem dependências externas (usa apenas a biblioteca padrão)

---

## Como executar

### 1. Inicie o servidor

```bash
python server.py
```

O servidor ficará ouvindo em `0.0.0.0:9090`.

### 2. Inicie um ou mais clientes (em terminais separados)

```bash
python client.py
```

Siga as instruções na tela:
- Informe o IP do servidor (ou Enter para `127.0.0.1`)
- Informe a porta (ou Enter para `9090`)
- Escolha seu apelido

### 3. Converse!

Digite mensagens e pressione **Enter** para enviar.  
Para sair, digite `/sair`.

---

## Testando na mesma máquina

Abra **3 terminais**:

| Terminal | Comando         |
|----------|-----------------|
| 1        | `python server.py` |
| 2        | `python client.py` → apelido: Alice |
| 3        | `python client.py` → apelido: Bob   |

---

## Testando em rede local

1. Descubra o IP da máquina que rodará o servidor:
   - Windows: `ipconfig`
   - Linux/Mac: `ip a` ou `ifconfig`
2. Inicie o servidor nessa máquina.
3. Nos clientes, informe o IP encontrado no passo 1.

---

## Estrutura dos arquivos

```
chat_udp/
├── server.py   # Servidor UDP — gerencia clientes e faz broadcast
├── client.py   # Cliente UDP — envia e recebe mensagens
└── README.md   # Este arquivo
```

---

## Protocolo de mensagens

| Mensagem enviada pelo cliente | Significado                        |
|-------------------------------|------------------------------------|
| `JOIN:<apelido>`              | Registra o cliente no servidor     |
| `QUIT`                        | Informa saída voluntária           |
| Qualquer outro texto          | Mensagem de chat para broadcast    |

---

## Limitações do UDP

Por usar UDP, algumas características se aplicam:
- Mensagens podem ser **perdidas** em redes congestionadas (improvável em rede local).
- Não há garantia de **ordem** de chegada.
- Não há estado de conexão — o servidor rastreia clientes via dicionário em memória.
