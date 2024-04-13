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
        self.ttl = 1
        self.sequencia = 1

    def start_servidor(self):
        servidor_thread = Thread(target=self.servidor.start)
        servidor_thread.start()

    def conectar_vizinhos(self):
        if not self.vizinhos:
            return
        for vizinho in self.vizinhos:
            endereco, porta = vizinho.split(":")
            self.enviar(vizinho, f"{endereco}:{porta} {self.sequencia} {self.ttl} HELLO")

    def enviar(self, vizinho, mensagem):
        print(f'Tentando adicionar vizinho {vizinho}')
        try:
            print(f'Encaminhando mensagem "{mensagem}" para {vizinho}')
            cliente = socket(AF_INET, SOCK_STREAM)
            cliente.connect((vizinho.split(":")[0], int(vizinho.split(":")[1])))
            cliente.sendall(mensagem.encode())
            print(f'\nEnvio feito com sucesso: {mensagem}')
            cliente.close()
        except Exception as e:
            print(f'\tErro ao conectar!')
        finally:
            self.sequencia += 1

    def start(self):
        self.start_servidor()
        sleep(0.5)
        self.conectar_vizinhos()
