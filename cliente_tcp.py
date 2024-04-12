from socket import *

class ClienteTCP:
  def __init__(self, endereco, porta):
      self.endereco = endereco
      self.porta = porta
      self.socket = None

  def connect(self):
      try:
          self.socket = socket(AF_INET, SOCK_STREAM)
          self.socket.connect((self.endereco, self.porta))
          print(f"Connected to {self.endereco}:{self.porta}")
      except Exception as e:
          print(f"Error: {e}")

  def send_data(self, data):
      try:
          self.socket.sendall(data.encode())
      except Exception as e:
          print(f"Error sending data: {e}")

  def receive_data(self, buffer_size=1024):
      try:
          data = self.socket.recv(buffer_size)
          return data.decode()
      except Exception as e:
          print(f"Error receiving data: {e}")

  def close(self):
      try:
          self.socket.close()
          print("Connection closed")
      except Exception as e:
          print(f"Error closing connection: {e}")
