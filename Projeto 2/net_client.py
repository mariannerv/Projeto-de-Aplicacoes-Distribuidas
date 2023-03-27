"""
Aplicações Distribuídas - Projeto 2 - net_client.py
Grupo: 28
Números de aluno: 55945, 58662
"""


# zona para fazer importação
import sock_utils
import pickle
import struct

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
        self.sock = sock_utils.create_tcp_client_socket(
            self.address, self.port)

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        try:

            # envio da mensagem
            msg_bytes = pickle.dumps(data, -1)  # obtem o objeto serializado
            # calcula o tamanho do objeto serializado
            size_bytes = struct.pack("i", len(msg_bytes))
            self.sock.sendall(size_bytes)  # envia os tamanho do objeto
            self.sock.sendall(msg_bytes)  # envia a lista

            # receção da mensagem
            size_resposta_bytes = self.sock.recv(4)  # tamanho de bytes serializado
            size_resposta = struct.unpack('i', size_resposta_bytes)[
                0]  # deserializa esse numero
            resposta_bytes = sock_utils.receive_all(self.sock, size_resposta)
            resposta = pickle.loads(resposta_bytes)

            return resposta
        except BrokenPipeError:
                # handle broken pipe error
            self.connect()
            return self.send_receive(data)

    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()
