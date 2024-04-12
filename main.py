import argparse
from peer import Peer


class Main:
    def __init__(self, endereco, porta, vizinhos=None, lista_chave_valor=None):
        self.endereco = endereco
        self.porta = porta
        self.vizinhos = vizinhos
        self.lista_chave_valor = lista_chave_valor
        self.peer = Peer(self.endereco, self.porta)

    @staticmethod
    def parse_argumentos():
        parser = argparse.ArgumentParser(
            description="Rode o programa com os argumentos abaixo:"
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
    def validar_endereco_porta(endereco_porta):
        split = endereco_porta.split(":")
        if len(split) != 2:
            raise ValueError(
                "Endereço e porta deve ser no formato <endereco>:<porta>")
        endereco, porta_str = split
        try:
            porta = int(porta_str)
        except ValueError:
            raise ValueError("Porta deve ser um número inteiro")
        return endereco, porta

    @staticmethod
    def ler_lista_vizinhos(nome_arquivo):
        with open(nome_arquivo, 'r') as file:
            vizinhos = file.readlines()
        return vizinhos

    @classmethod
    def run(self):
        args = self.parse_argumentos()
        endereco, porta = self.validar_endereco_porta(args.endereco_porta)
        vizinhos = self.ler_lista_vizinhos(args.vizinhos)
        main_instance = self(endereco, porta, vizinhos,
                             args.lista_chave_valor)

        main_instance.peer.start()

        # if main_instance.vizinhos:
        #    peer_address = tuple(main_instance.vizinhos.split(':'))
        #    main_instance.connect_to_peer(peer_address)
        #    main_instance.enviar_mensagem("Hello from Main")
        #    main_instance.receber_mensagem()


if __name__ == "__main__":
    Main.run()
