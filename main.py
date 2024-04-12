import argparse
from peer import Peer


class Main:
    def __init__(self, endereco, porta, vizinhos=None, lista_chave_valor=None):
        self.endereco = endereco
        self.porta = porta
        self.vizinhos = vizinhos
        self.lista_chave_valor = lista_chave_valor
        self.ttl = 1

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
        if not nome_arquivo:
            return None
        with open(nome_arquivo, 'r') as file:
            vizinhos = [vizinho.strip() for vizinho in file.readlines()]
        return vizinhos

    @staticmethod
    def listar_vizinhos(self):
        print(f'Há {len(self.vizinhos)} vizinhos:')
        for i, vizinho in enumerate(self.vizinhos):
            print(f'\t[{i}] {vizinho}')

    def hello(self, peer):
        print("Escolha o vizinho:")
        self.listar_vizinhos(self)
        input_vizinho = input("")
        vizinho = self.vizinhos[int(input_vizinho)]
        print(
            f'Encaminhando mensagem "{self.endereco}:{self.porta} 5 {self.ttl} HELLO" para {vizinho}')
        self.peer.hello(vizinho)

    @staticmethod
    def ler_lista_chave_valor(nome_arquivo):
        if not nome_arquivo:
            return None
        lista_chave_valor = {}
        with open(nome_arquivo, 'r') as file:
            linhas = file.readlines()
            for linha in linhas:
                chave, valor = linha.strip().split(" ")
                lista_chave_valor[chave] = valor
        return lista_chave_valor

    @classmethod
    def run(self):
        args = self.parse_argumentos()
        endereco, porta = self.validar_endereco_porta(args.endereco_porta)
        vizinhos = self.ler_lista_vizinhos(args.vizinhos)
        lista_chave_valor = self.ler_lista_chave_valor(args.lista_chave_valor)
        main_instance = self(endereco, porta, vizinhos,
                             lista_chave_valor)

        peer = Peer(main_instance.endereco, main_instance.porta,
                    main_instance.vizinhos, main_instance.lista_chave_valor)
        peer.start()

        print("""
Escolha o comando
    [0] Listar vizinhos
    [1] HELLO
    [2] SEARCH (flooding)
    [3] SEARCH (random walk)
    [4] SEARCH (busca em profundidade)
    [5] Estatisticas
    [6] Alterar valor padrao de TTL
    [9] Sair
            """)
        while True:
            escolha = input("").split(" ")[0]

            if escolha == "0":
                main_instance.listar_vizinhos()
            elif escolha == "1":
                main_instance.hello(peer)
            elif escolha == "2":
                main_instance.listar_vizinhos()
            elif escolha == "3":
                main_instance.listar_vizinhos()
            elif escolha == "4":
                main_instance.listar_vizinhos()
            elif escolha == "5":
                main_instance.listar_vizinhos()
            elif escolha == "6":
                main_instance.listar_vizinhos()
            elif escolha == "9":
                break
            else:
                print("Opção inválida")


if __name__ == "__main__":
    Main.run()
