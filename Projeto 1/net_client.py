"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Grupo: 28
Números de aluno: 55945, 58662
"""


import sock_utils

###############################################################################

# definição da classe server_connection 
class server_connection:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        self.sock = None 


    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        self.sock = sock_utils.create_tcp_client_socket(self.address, self.port)
        self.sock.connect((self.address, self.port))

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        self.sock.sendall(data.encode()) 
        resposta = self.sock.recv(1024)
        
        return resposta.decode('utf-8') 

    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()
