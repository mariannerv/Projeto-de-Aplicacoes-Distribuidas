# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 1 - sock_utils.py
Grupo: 28
Números de aluno: 55945, 58662
"""

import socket as s

def create_tcp_server_socket(adress, port, queue_size):

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    sock.bind((adress, port))
    sock.listen(queue_size) 
    
    return sock

def create_tcp_client_socket(adress, port):
    
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    return sock


def receive_all(socket, length):
    msg = ''
    qty = 0
    while qty < length:
        ms = socket.recv(length - qty)
        qty += len(ms)
        msg+=ms
    return msg
        
