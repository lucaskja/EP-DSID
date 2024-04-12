import argparse
from cliente_tcp import ClienteTCP
from servidor_tcp import ServidorTCP

class Main:
    def __init__(self, endereco, porta, vizinhos=None, lista_chave_valor=None):
        self.endereco = endereco
        self.porta = porta
        self.vizinhos = vizinhos
        self.lista_chave_valor = lista_chave_valor
        self.client = ClienteTCP(self.endereco, self.porta)
        self.server = ServidorTCP(self.endereco, self.porta)

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(
            description="Run the program with specific arguments"
        )
        parser.add_argument(
            "endereco_porta",
            type=str,
            help="Endereço e porta no formato <endereco>:<porta>",
        )
        parser.add_argument(
            "vizinhos", type=str, help="Lista de vizinhos", nargs="?"
        )
        parser.add_argument(
            "lista_chave_valor",
            type=str,
            help="Lista de chave e valor",
            nargs="?",
        )

        return parser.parse_args()

    @staticmethod
    def validate_endereco_porta(endereco_porta):
        parts = endereco_porta.split(":")
        if len(parts) != 2:
            raise ValueError("Endereço e porta deve ser no formato <endereco>:<porta>")
        endereco, porta_str = parts
        try:
            porta = int(porta_str)
        except ValueError:
            raise ValueError("Porta deve ser um número inteiro")
        return endereco, porta

    def start_server(self):
        self.server.bind()

    def connect_to_peer(self, peer_address):
        self.client.connect(peer_address)
        print(f"Connected to peer at {peer_address}")

    def send_message(self, message):
        self.client.send_data(message)
        print("Message sent")

    def receive_message(self):
        data = self.client.receive_data()
        print(f"Received message: {data}")

    @classmethod
    def run(self):
        args = self.parse_arguments()
        endereco_porta = args.endereco_porta
        endereco, porta = self.validate_endereco_porta(endereco_porta)
        vizinhos = args.vizinhos
        lista_chave_valor = args.lista_chave_valor
        main_instance = self(endereco, porta, vizinhos, lista_chave_valor)
        main_instance.start_server()
        main_instance.server.run()

        if main_instance.vizinhos:
            peer_address = tuple(main_instance.vizinhos.split(':'))
            main_instance.connect_to_peer(peer_address)
            main_instance.send_message("Hello from Main")
            main_instance.receive_message()
            
if __name__ == "__main__":
    Main.run()
