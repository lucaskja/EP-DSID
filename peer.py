from threading import Thread
from socket import *
from servidor_tcp import ServidorTCP
from time import sleep


class Peer:
    def __init__(self, endereco, porta, vizinhos=None, lista_chave_valor=None):
        self.endereco = endereco
        self.porta = porta
        self.vizinhos = vizinhos
        self.lista_chave_valor = lista_chave_valor
        self.servidor = ServidorTCP(endereco, porta)

    def start_servidor(self):
        servidor_thread = Thread(target=self.servidor.start)
        servidor_thread.start()

    def conectar_vizinhos(self):
        if not self.vizinhos:
            return
        for vizinho in self.vizinhos:
            endereco, porta = vizinho.split(":")
            try:
                cliente = socket(AF_INET, SOCK_STREAM)
                cliente.connect((endereco, int(porta)))
                print(f'Conectado ao vizinho: {vizinho}')
                cliente.sendall(b"HELLO")
                cliente.close()
            except Exception as e:
                print(f'Erro ao conectar ao vizinho: {vizinho} - {e}')

    def hello(self, endereco, porta):
            try:
                cliente = socket(AF_INET, SOCK_STREAM)
                cliente.connect((endereco, porta))
                cliente.sendall(b"HELLO")
                print(f'Enviado ao vizinho: {endereco}:{porta}')
                cliente.close()
            except Exception as e:
                print(f'Erro ao conectar ao vizinho: {vizinho} - {e}')

    def start(self):
        self.start_servidor()
        self.conectar_vizinhos()
