import threading
from cliente_tcp import ClienteTCP
from servidor_tcp import ServidorTCP


class Peer:
    def __init__(self, endereco, porta):
        self.endereco = endereco
        self.porta = porta
        self.cliente = ClienteTCP(endereco, porta)
        self.servidor = ServidorTCP(endereco, porta)

    def start_servidor(self):
        self.servidor.bind()
        server_thread = threading.Thread(target=self.servidor.run)
        server_thread.start()
        print(f"Server started on {self.endereco}:{self.porta}")

    def start_cliente(self):
        cliente_thread = threading.Thread(
            target=self.cliente.conectar(self.endereco, self.porta))
        cliente_thread.start()
        print(f"Client started on {self.endereco}:{self.porta}")

    def start(self):
        self.start_servidor()
        self.start_cliente()
        print(f"Peer started on {self.endereco}:{self.porta}")
