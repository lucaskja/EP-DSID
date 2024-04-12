from socket import *
from threading import Thread


class ServidorTCP:
    def __init__(self, endereco, porta):
        self.endereco = endereco
        self.porta = porta
        self.socket = None

    def bind(self):
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.bind((self.endereco, self.porta))
            self.socket.listen(1)
            print(f'Servidor criado: {self.endereco}:{self.porta}')
        except Exception as e:
            print(f'Erro: {e}')

    def run(self):
        while True:
            client_socket, client_address = self.socket.accept()
            print(f'Conexão do cliente: {client_address}')
            cliente_thread = Thread(target=self.handle_client, args=(
                client_socket,))
            cliente_thread.start()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f'Recebido: {data}')
        client_socket.close()

    def start(self):
        self.bind()
        self.run()
