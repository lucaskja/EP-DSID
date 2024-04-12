from cliente_tcp import ClienteTCP
from servidor_tcp import ServidorTCP


class Peer:
    def __init__(self, endereco, porta):
        self.endereco = endereco
        self.porta = porta
        self.cliente = ClienteTCP(endereco, porta)
        self.servidor = ServidorTCP(endereco, porta)


