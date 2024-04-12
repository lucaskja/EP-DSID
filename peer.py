from threading import Thread
from cliente_tcp import ClienteTCP
from servidor_tcp import ServidorTCP


class Peer:
    def __init__(self, endereco, porta, vizinhos=None, par_chave=None):
        self.endereco = endereco
        self.porta = porta
        self.vizinhos = vizinhos
        self.par_chave = par_chave
        self.cliente = ClienteTCP(endereco, porta)
        self.servidor = ServidorTCP(endereco, porta)

    def start_servidor(self):
        self.servidor.bind()
        servidor_thread = Thread(target=self.servidor.run)
        servidor_thread.start()

    def start_cliente(self, endereco, porta):
        cliente_thread = Thread(
            target=self.cliente.conectar(endereco, porta))
        cliente_thread.start()

    def start(self):
        self.start_servidor()
        self.start_cliente(self.endereco, self.porta)
        print(f"Peer started on {self.endereco}:{self.porta}")
