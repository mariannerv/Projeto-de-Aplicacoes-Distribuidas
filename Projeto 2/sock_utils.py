# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 2 - sock_utils.py
Grupo: 28
Números de aluno: 55945, 58662
"""

import socket as s


def create_tcp_server_socket(adress, port, queue_size):
    """
    Esta função serve para criar uma socket de servidor TCP onde poderão posteriormente ser
    aceites ligações de clientes.
    
    address - será o endereço anfitrião à qual a socket ficará vinculada.
    port - será a porta onde o servidor atenderá novos pedidos de ligação.
    queue_size - define o número máximo de pedidos de ligação em espera. (ver função listen dos
    objetos da classe socket).
    """

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    sock.bind((adress, port))
    sock.listen(queue_size)

    return sock


def create_tcp_client_socket(adress, port):
    """
    Esta função serve para criar uma socket de ligação para o cliente comunicar com um servidor.
    address será o endereço do servidor onde o cliente se ligará.
    port será a porta onde o servidor atende pedidos de ligação.
    """

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((adress, port))

    return sock


def receive_all(socket, length):
    data = bytearray()
    while len(data) < length:
        packet = socket.recv(length - len(data))
        data.extend(packet)

    return data
