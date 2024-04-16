import argparse
import sys
from random import choice
from time import sleep
from servidor_tcp import ServidorTCP

class Main:
    def __init__(self, endereco, porta, vizinhos=None, lista_chave_valor=None):
        self.endereco = endereco
        self.porta = porta
        self.vizinhos = vizinhos or []
        self.lista_chave_valor = lista_chave_valor or {}

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
            "vizinhos", type=str, help="Arquivo contendo lista de vizinhos", nargs="?"
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

    def listar_vizinhos(self):
        # Exibir a lista de vizinhos
        print(f'Há {len(self.vizinhos)} vizinhos:')
        for i, vizinho in enumerate(self.vizinhos):
            print(f'\t[{i}] {vizinho}')
            
    def hello(self, peer):
        # Função para enviar uma mensagem HELLO para um vizinho escolhido
        print("Escolha o vizinho:")
        self.listar_vizinhos()
        input_vizinho = input("")
        vizinho = self.vizinhos[int(input_vizinho)]
        mensagem = f"{peer.endereco}:{peer.porta} {peer.sequencia} {peer.ttl} HELLO"
        peer.enviar_mensagem(vizinho, mensagem)
        
    def iniciar_flooding(self, peer):
        # Função para enviar uma mensagem SEARCH (flooding)
        input_chave = input("Digite a chave a ser buscada\n")
        ip_origem = f"{peer.endereco}:{peer.porta}"
        mensagem = f"{ip_origem} {peer.sequencia} {peer.ttl} SEARCH FL {peer.porta} {input_chave} 1"
        peer.mensagens_vistas.add((ip_origem, peer.sequencia))
        for vizinho in peer.vizinhos:
            peer.enviar_mensagem(vizinho, mensagem)
    
    def iniciar_random_walk(self, peer):
        # Função para enviar uma mensagem SEARCH (random walk)
        input_chave = input("Digite a chave a ser buscada\n")
        ip_origem = f"{peer.endereco}:{peer.porta}"
        mensagem = f"{ip_origem} {peer.sequencia} {peer.ttl} SEARCH RW {peer.porta} {input_chave} 1"
        vizinho_escolhido = choice(peer.vizinhos)
        peer.enviar_mensagem(vizinho_escolhido, mensagem)
    
    def iniciar_busca_profundidade(self, peer):
        # Função para enviar uma mensagem SEARCH (busca em profundidade)
        input_chave = input("Digite a chave a ser buscada\n")
        noh_mae = f"{peer.endereco}:{peer.porta}"
        mensagem = f"{noh_mae} {peer.sequencia} {peer.ttl} SEARCH BP {peer.porta} {input_chave} 1"
        vizinhos_candidatos = peer.vizinhos.copy()
        proximo_vizinho = choice(vizinhos_candidatos)
        vizinho_ativo = proximo_vizinho
        vizinhos_candidatos.remove(proximo_vizinho)
        peer.enviar_mensagem(proximo_vizinho, mensagem)
    
    def estatisticas(self, peer):
        # Função para exibir estatísticas
        pass
    
    def bye(self, peer):
        # Função para enviar uma mensagem BYE para todos os vizinhos
        print("Saindo...")
        peer.desconectar_vizinhos()
        sleep(2)
        sys.exit(0)

    @classmethod
    def run(self):
        args = self.parse_argumentos()
        endereco, porta = self.validar_endereco_porta(args.endereco_porta)
        vizinhos = self.ler_lista_vizinhos(args.vizinhos)
        lista_chave_valor = self.ler_lista_chave_valor(args.lista_chave_valor)
        main_instance = self(endereco, porta, vizinhos,
                             lista_chave_valor)

        peer = ServidorTCP(main_instance.endereco, main_instance.porta,
                    main_instance.vizinhos, main_instance.lista_chave_valor)
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
                main_instance.listar_vizinhos()
            elif escolha == "1":
                main_instance.hello(peer)
            elif escolha == "2":
                main_instance.iniciar_flooding(peer)
            elif escolha == "3":
                main_instance.iniciar_random_walk(peer)
            elif escolha == "4":
                main_instance.iniciar_busca_profundidade(peer)
            elif escolha == "5":
                main_instance.estatisticas(peer)
            elif escolha == "6":
                input_ttl = input("Digite o novo valor de TTL: ")
                try:
                    main_instance.peer.servidor.ttl = int(input_ttl)
                except ValueError:
                    print("TTL deve ser um número inteiro")
            elif escolha == "9":
                main_instance.bye(peer)
            else:
                print("Opção inválida")
            sleep(1)


if __name__ == "__main__":
    Main.run()
