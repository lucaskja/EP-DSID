import sys
import argparse

class Main:
    def __init__(self, endereco, porta, vizinhos=None, lista_chave_valor=None):
      self.endereco = endereco
      self.porta = porta
      self.vizinhos = vizinhos
      self.lista_chave_valor = lista_chave_valor

    @staticmethod
    def parse_arguments():
      parser = argparse.ArgumentParser(description='Rode o arquivo com os argumentos especifícos')
      parser.add_argument('endereco_porta', type=str, help='Endereço e porta no formato <endereco>:<porta>')
      parser.add_argument('vizinhos', type=str, help='lista de vizinhos', nargs='?')
      parser.add_argument('lista_chave_valor', type=str, help='lista de chave e valor', nargs='?')

      return parser.parse_args()

    @staticmethod
    def validate_endereco_porta(endereco_porta):
      parts = endereco_porta.split(':')
      if len(parts) != 2:
          raise ValueError('Endereço e porta deve ser no formato <endereco>:<porta>')
      endereco, porta_str = parts
      try:
          porta = int(porta_str)
      except ValueError:
          raise ValueError('Porta deve ser um número inteiro')
      return endereco, porta

    @classmethod
    def main(cls):
      args = cls.parse_arguments()
      endereco, porta = cls.validate_endereco_porta(args.endereco_porta)
      vizinhos = args.vizinhos
      lista_chave_valor = args.lista_chave_valor
      main_instance = cls(endereco, porta, vizinhos, lista_chave_valor)
      print(main_instance.endereco)
      print(main_instance.porta)
      print(main_instance.vizinhos)
      print(main_instance.lista_chave_valor)

if __name__ == '__main__':
    Main.main()
