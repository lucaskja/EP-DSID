from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep
from random import choice


class ServidorTCP:
    def __init__(self, endereco, porta, vizinhos=None, lista_chave_valor=None):
        # Inicializa o servidor com o endereço, porta, lista de vizinhos e lista de chave-valor.
        self.endereco = endereco
        self.porta = porta
        self.vizinhos = vizinhos
        self.vizinhos_conectados = []
        self.lista_chave_valor = lista_chave_valor
        self.socket = None
        self.mensagens_vistas_flooding = set()
        self.mensagens_vistas_busca_profundidade = set()
        self.ttl = 100
        self.sequencia = 1

    def bind(self):
        # Liga o servidor ao endereço e porta especificados.
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.bind((self.endereco, self.porta))
            self.socket.listen(1)
            print(f'Servidor criado: {self.endereco}:{self.porta}\n')
        except Exception as e:
            print(f'Erro Bind: {e}')

    def run(self):
        # Inicia o servidor e aguarda conexões de clientes.
        while True:
            client_socket, client_address = self.socket.accept()
            # print(f'Conexão do cliente: {client_address}')
            cliente_thread = Thread(target=self.handle_client, args=(
                client_socket,))
            cliente_thread.start()

    def handle_client(self, client_socket):
        # Lida com as mensagens recebidas dos clientes.
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f'Mensagem recebida: {data}')
            try:
                self.trata_mensagem(data)
            except Exception as e:
                print(f'Erro Handle Client: {e}')
        client_socket.close()
        
    def conectar_vizinhos(self):
        # Envia uma mensagem HELLO para cada vizinho.
        if not self.vizinhos:
            return
        for vizinho in self.vizinhos:
            print(f'Tentando adicionar vizinho {vizinho}')
            self.enviar_mensagem(vizinho, f"{self.endereco}:{self.porta} {self.sequencia} {self.ttl} HELLO")
            
    def desconectar_vizinhos(self):
        # Envia uma mensagem BYE para cada vizinho.
        if not self.vizinhos:
            return
        for vizinho in self.vizinhos:
            self.enviar_mensagem(vizinho, f"{self.endereco}:{self.porta} {self.sequencia} {self.ttl} BYE")
        
    def enviar_mensagem(self, vizinho, mensagem):
        # Envia uma mensagem para um vizinho específico.
        try:
            print(f'Encaminhando mensagem "{mensagem}" para {vizinho}')
            cliente = socket(AF_INET, SOCK_STREAM)
            cliente.connect((vizinho.split(":")[0], int(vizinho.split(":")[1])))
            cliente.sendall(mensagem.encode())
            print(f'\tEnvio feito com sucesso: {mensagem}')
            cliente.close()
        except Exception as e:
            print(f'\tErro ao conectar! {e}')
            
    def processa_hello(self, mensagem):
        # Adiciona o vizinho na lista de vizinhos conectados.
        origin = mensagem.split(" ")[0]
        if origin not in self.vizinhos_conectados:
            self.vizinhos_conectados.append(origin)
            print(f'\tAdicionando vizinho na tabela: {origin}')
        else:
            print(f'\tVizinho ja esta na tabela: {origin}')
            
    def processa_valor(self, mensagem):
        # Processa a mensagem VAL e exibe a chave e o valor.
        mensagem_split = mensagem.split(" ")
        chave = mensagem_split[5]
        valor = mensagem_split[6]
        print(f'\tValor encontrada!\n\t\tchave: {chave} valor: {valor}')
                    
    def processa_flooding(self, mensagem):
        # Pegar o endereco de origem, a sequencia, o ttl, a chave, o hop count da mensagem
        mensagem_split = mensagem.split(" ")
        endereco_origem = mensagem_split[0]
        sequencia = mensagem_split[1]
        ttl = int(mensagem_split[2])
        chave = mensagem_split[6]
        hop_count = int(mensagem_split[7])
        
        # Verificar se a mensagem ja foi vista
        if (endereco_origem, sequencia) in self.mensagens_vistas_flooding:
            print(f'\tFlooding: Mensagem repetida! {mensagem}')
            return
        
        # Adicionar a mensagem na lista de mensagens vistas
        self.mensagens_vistas_flooding.add((endereco_origem, sequencia))
        
        # Verificar se a chave esta na lista chave valor
        if chave in self.lista_chave_valor:
            print(f'\tChave encontrada!')
            self.enviar_mensagem(endereco_origem, f"{self.endereco}:{self.porta} {self.sequencia} {self.ttl} VAL FL {chave} {self.lista_chave_valor[chave]} {hop_count}")
            return
        
        # Decrementar TTL e verificar se ele é maior que 0
        ttl -= 1
        if ttl == 0:
            print(f'\tTTL igual a zero, descartando mensagem')
            return
        
        # Incrementar hop count e enviar a mensagem para todos os vizinhos
        for vizinho in self.vizinhos:
            if vizinho == endereco_origem:
                continue
            self.enviar_mensagem(vizinho, f"{endereco_origem} {sequencia} {ttl} SEARCH FL {self.porta} {chave} {hop_count + 1}")
            
        
    def processa_random_walk(self, mensagem):
        # Pegar o endereco de origem, a sequencia, o ttl, a chave, o hop count da mensagem
        mensagem_split = mensagem.split(" ")
        endereco_origem = mensagem_split[0]
        sequencia = mensagem_split[1]
        ttl = int(mensagem_split[2])
        chave = mensagem_split[6]
        hop_count = int(mensagem_split[7])
        
        # Verificar se a chave esta na lista chave valor
        if chave in self.lista_chave_valor:
            print(f'\tChave encontrada!')
            self.enviar_mensagem(endereco_origem, f"{self.endereco}:{self.porta} {self.sequencia} {self.ttl} VAL RW {chave} {self.lista_chave_valor[chave]} {hop_count}")
            return
        
        # Decrementar TTL e verificar se ele é maior que 0
        ttl -= 1
        if ttl == 0:
            print(f'\tTTL igual a zero, descartando mensagem')
            return
        
        # Incrementar hop count e enviar a mensagem para um vizinho aleatorio
        vizinho_escolhido = choice(self.vizinhos)
        self.enviar_mensagem(vizinho_escolhido, f"{endereco_origem} {sequencia} {ttl} SEARCH RW {self.porta} {chave} {hop_count + 1}")
    
    def processa_busca_profundidade(self, mensagem):
        # Pegar o endereco de origem, a sequencia, o ttl, a chave, o hop count da mensagem
        mensagem_split = mensagem.split(" ")
        endereco_origem = mensagem_split[0]
        sequencia = mensagem_split[1]
        ttl = int(mensagem_split[2])
        chave = mensagem_split[6]
        hop_count = int(mensagem_split[7])

        # Verificar se a chave esta na lista chave valor
        if chave in self.lista_chave_valor:
            print(f'\tChave encontrada!')
            self.enviar_mensagem(endereco_origem, f"{self.endereco}:{self.porta} {self.sequencia} {self.ttl} VAL BP {chave} {self.lista_chave_valor[chave]} {hop_count}")
            return
        
        # Decrementar TTL e verificar se ele é maior que 0
        ttl -= 1
        if ttl == 0:
            print(f'\tTTL igual a zero, descartando mensagem')
            return
        
        # Verifica se é a primeira vez que a mensagem é vista
        if (endereco_origem, sequencia) not in self.mensagens_vistas_busca_profundidade:
            # Adiciona o endereço origem à lista de vizinhos candidatos
            vizinhos_candidatos = self.vizinhos.copy()
            vizinhos_candidatos.remove(endereco_origem)
            # Adiciona a mensagem à lista de mensagens vistas
            self.mensagens_vistas_busca_profundidade.add((endereco_origem, sequencia))
        else:
            vizinhos_candidatos = self.vizinhos.copy()
        
        # Verifica a condição de parada
        if endereco_origem == self.endereco and not vizinhos_candidatos:
            print("BP: Não foi possível localizar a chave", chave)
            return

        # Encontra o próximo vizinho ativo
        if self.endereco == endereco_origem:
            proximo = endereco_origem
        else:
            proximo = choice(vizinhos_candidatos)

        # Envia a mensagem para o próximo vizinho ativo
        self.enviar_mensagem(proximo, mensagem)
    
    def processa_bye(self, mensagem):
        # Remove o vizinho da lista de vizinhos conectados.
        endereco_origem = mensagem.split(" ")[0]
        print(f'\tRemovendo vizinho da tabela {endereco_origem}')
        self.vizinhos_conectados.remove(endereco_origem)
        
    def trata_mensagem(self, mensagem):
        # Trata a mensagem recebida.
        mensagem_split = mensagem.split(" ")
        if mensagem_split[3] == "HELLO":
            self.processa_hello(mensagem)
        elif mensagem_split[3] == "VAL":
            self.processa_valor(mensagem)
        elif mensagem_split[3] == "BYE":
            self.processa_bye(mensagem)
        elif mensagem_split[4] == "FL":
            self.processa_flooding(mensagem)
        elif mensagem_split[4] == "RW":
            self.processa_random_walk(mensagem)
        elif mensagem_split[4] == "BP":
            self.processa_busca_profundidade(mensagem)
        else:
            print(f'Mensagem desconhecida: {mensagem}')
        self.sequencia += 1
            

    def start(self):
        # Inicia o servidor e conecta os vizinhos.
        self.bind()
        servidor_thread = Thread(target=self.run)
        servidor_thread.start()
        sleep(0.5)
        self.conectar_vizinhos()
