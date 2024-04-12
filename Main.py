import argparse
from cliente_tcp import ClienteTCP
from servidor_tcp import ServidorTCP

class Main:
  def __init__(self, endereco, porta, vizinhos=None, lista_chave_valor=None):
    self.endereco = endereco
    self.porta = porta
    self.vizinhos = vizinhos
    self.lista_chave_valor = lista_chave_valor
    self.cliente = ClienteTCP(self.endereco, 5001)
    self.servidor = ServidorTCP(self.endereco, self.porta)

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
    parts = endereco_porta.split(":")
    if len(parts) != 2:
        raise ValueError("Endereço e porta deve ser no formato <endereco>:<porta>")
    endereco, porta_str = parts
    try:
        porta = int(porta_str)
    except ValueError:
        raise ValueError("Porta deve ser um número inteiro")
    return endereco, porta

  def iniciar_servidor(self):
    self.servidor.bind()

  def connect_to_peer(self, peer_address):
    self.cliente.connect(peer_address)
    print(f"Connected to peer at {peer_address}")

  def enviar_mensagem(self, mensagem):
    self.cliente.send_data(mensagem)
    print(f'Mensagem enviada: {mensagem}')

  def receber_mensagem(self):
    data = self.cliente.receive_data()
    print(f"Mensagem recebida: {data}")

  @classmethod
  def run(self):
    args = self.parse_argumentos()
    endereco, porta = self.validar_endereco_porta(args.endereco_porta)
    main_instance = self(endereco, porta, args.vizinhos, args.lista_chave_valor)
  
    # main_instance.iniciar_servidor()
    # main_instance.servidor.run()

    main_instance.cliente.conectar()

    if main_instance.vizinhos:
      peer_address = tuple(main_instance.vizinhos.split(':'))
      main_instance.connect_to_peer(peer_address)
      main_instance.enviar_mensagem("Hello from Main")
      main_instance.receber_mensagem()
            
if __name__ == "__main__":
  Main.run()
