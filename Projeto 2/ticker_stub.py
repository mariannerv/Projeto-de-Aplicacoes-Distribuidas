# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 2 - ticker_sub.py
Grupo: 28
Números de aluno: 55945, 58662
"""

import net_client
import socket as s

###############################################################################

class TickerStub:
    global client_id
    def __init__(self, host,port,client_id):
        self.conn_sock = net_client.server_connection(host, port)
        self.client_id = client_id

    def connect(self):
        self.conn_sock.connect()

    def disconnect(self):
        self.conn_sock.close()
    
    def subscribe(self, pedido):

        msg = [10, pedido[0], pedido[1], pedido[2]]
        res = self.conn_sock.send_receive(msg)

        return res

    def cancel(self, pedido):

        msg = [20, pedido[0], pedido[1]]
        res = self.conn_sock.send_receive(msg)

        return res

    def status(self, pedido):

        msg = [30, pedido[0], pedido[1]]
        res = self.conn_sock.send_receive(msg)

        return res

    def infos(self, pedido):

        msg = []

        if pedido[0] == 'M':
            msg = [40, pedido[1]]
        elif pedido[0] == 'K':
            msg = [50, pedido[1]]
        else: 
            msg = ["Opção Inválida"]

        res = self.conn_sock.send_receive(msg)

        return res

    def statis(self, pedido):

        msg = []

        if pedido[0] == 'L':
            msg = [60, pedido[1]]
        elif pedido[0] == 'ALL':
            msg = [70]
        else:
            msg = ["Opção Inválida"]

        res = self.conn_sock.send_receive(msg)

        return res
