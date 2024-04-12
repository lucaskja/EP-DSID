from socket import *


class ClienteTCP:
    def __init__(self, endereco, porta):
        self.endereco = endereco
        self.porta = porta
        self.socket = None

    def conectar(self):
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.endereco, 5000))
            print(f'Conectado em {self.endereco}:{self.porta}')
        except Exception as e:
            print(f'Erro ao conetar: {e}')

    def enviar_dados(self, data):
        try:
            self.socket.sendall(data.encode())
        except Exception as e:
            print(f'Error sending data: {e}')

    def receber_dados(self, buffer_size=1024):
        try:
            data = self.socket.recv(buffer_size)
            return data.decode()
        except Exception as e:
            print(f'Erro ao receber os dados: {e}')

    def fechar_conexao(self):
        try:
            self.socket.close()
            print(f'Cliente: {self.socket} fechou a conexao')
        except Exception as e:
            print(f'Erro, cliente {self.socket} fechando a conexao: {e}')
