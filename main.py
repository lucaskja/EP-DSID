import argparse
from time import sleep
from sistema_p2p import SistemaP2P


class Main:
    @staticmethod
    def parse_argumentos():
        # Configuração do parser de argumentos da linha de comando
        parser = argparse.ArgumentParser(
            description="Execute o programa com os seguintes argumentos:"
        )
        parser.add_argument(
            "endereco_porta",
            type=str,
            help="Endereço e porta no formato <endereco>:<porta>",
        )
        parser.add_argument(
            "vizinhos",
            type=str,
            help="Arquivo contendo lista de vizinhos",
            nargs="?",
        )
        parser.add_argument(
            "lista_chave_valor",
            type=str,
            help="Arquivo contendo pares chave-valor",
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
    def ler_lista_chave_valor(nome_arquivo):
        if not nome_arquivo:
            return None
        lista_chave_valor = {}
        with open(nome_arquivo, 'r') as file:
            linhas = file.readlines()
            for linha in linhas:
                chave, valor = linha.strip().split(" ")
                print(f"Adicionando par ({chave}, {valor}) na tabela local")
                lista_chave_valor[chave] = valor
        return lista_chave_valor

    @classmethod
    def run(self):
        args = self.parse_argumentos()
        endereco, porta = self.validar_endereco_porta(args.endereco_porta)
        vizinhos = self.ler_lista_vizinhos(args.vizinhos)
        lista_chave_valor = self.ler_lista_chave_valor(args.lista_chave_valor)
        print(f"Lista chave valor: {lista_chave_valor}")
        peer = SistemaP2P(endereco, porta,
                           vizinhos, lista_chave_valor)
        peer.start()

        while True:
            print("""
Escolha o comando
    [0] Listar vizinhos
    [1] HELLO
    [2] SEARCH (flooding)
    [3] SEARCH (random walk)
    [4] SEARCH (busca em profundidade)
    [5] Estatisticas
    [6] Alterar valor padrao de TTL
    [9] Sair""")
            escolha = input("").split(" ")[0]

            if escolha == "0":
                peer.listar_vizinhos()
            elif escolha == "1":
                peer.iniciar_hello(
                )
            elif escolha == "2":
                peer.iniciar_flooding()
            elif escolha == "3":
                peer.iniciar_random_walk()
            elif escolha == "4":
                peer.iniciar_busca_profundidade()
            elif escolha == "5":
                peer.iniciar_estatisticas()
            elif escolha == "6":
                input_ttl = input("Digite o novo valor de TTL:\n")
                try:
                    peer.ttl = int(input_ttl)
                except ValueError:
                    print("TTL deve ser um número inteiro")
            elif escolha == "9":
                peer.iniciar_bye()
            else:
                print("Opção inválida")
            sleep(1)


if __name__ == "__main__":
    Main.run()
