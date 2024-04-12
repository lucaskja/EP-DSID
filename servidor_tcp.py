from socket import *


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
            print(f'Escutando em {self.endereco}:{self.porta}')
        except Exception as e:
            print(f'Erro: {e}')

    def run(self):
        while True:
            client_socket, client_address = self.socket.accept()
            print(f'Conexão do cliente: {client_address}')
            data = client_socket.recv(1024)
            print(f'Recebido: {data.decode()}')
            if not data:
                break
            client_socket.sendall(data)
        client_socket.close()
