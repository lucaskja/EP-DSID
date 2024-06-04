# EP-DSID

Um Exercício-Programa para a disciplina de Desenvolvimento de Sistemas de Informações Distribuídos (DSID) do curso de Bacharelado em Sistema de Informação da Universidade de São Paulo (USP).

Link do repositório do GitHub: https://github.com/lucaskja/EP-DSID

# Participantes
```
Guilherme Campos Silva Lemes Prestes - 13720460
Lucas Kledeglau Jahchan Alves - 13732182
```

# Descrição
O EP consiste em um sistema de busca peer-to-peer não estruturado, que permite a indexação e busca de arquivos em uma rede de computadores. O sistema é composto por vários servidores, que podem indexar arquivos e realizar buscas por arquivos indexados por outros clientes.

# Execução
Para executar o sistema, é necessário ter o Python 3 instalado. Para rodar o servidor, basta executar o arquivo `main.py` com argumentos `<endereço>:<porta> [vizinhos.txt] [lista_chave_valor.txt]`, onde os argumentos em parenteses são opicionais, tal qual esse exemplo:
```
python3 main.py localhost:5000 vizinhos.txt lista_chave_valor.txt
```
