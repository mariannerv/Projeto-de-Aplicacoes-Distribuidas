# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 2 - ticker_skel.py
Grupo: 28
Números de aluno: 55945, 58662
"""

import pickle
from ticker_pool import resource_pool


###############################################################################

class Skeleton:
    def __init__(self,N,K,M):
        self.pool = resource_pool(N,K,M)
        


    def processMessage(self, msg_bytes):

        pedido = self.bytesToList(msg_bytes)
        resposta = []


        #SUBSCR
        if pedido[0] == 10 :

            client_id = int(pedido[3])
            resource_id = int(pedido[1])
            time_limit = int(pedido[2])

            resposta = self.pool.subscribe(resource_id,client_id,time_limit)

        #CANCEL
        elif pedido[0] == 20:
            resource_id = int(pedido[1])
            client_id = int(pedido[2])

            resposta = self.pool.unsubscribe(resource_id,client_id)

        #STATUS
        elif pedido[0] == 30:
            resource_id = int(pedido[1])
            client_id = int(pedido[2])
            
            resposta = self.pool.status(resource_id, client_id)

        #INFOS M
        elif pedido[0] == 40:

            client_id = int(pedido[1])
            resposta = self.pool.infos('M',client_id)
            
            
        #INFOS K
        elif pedido[0] == 50:
            client_id = int(pedido[1])
            resposta = self.pool.infos('K',client_id)
            

        #STATIS  L 
        elif pedido[0] == 60:
            resource_id = int(pedido[1])
            resposta = self.pool.statis('L',resource_id)

            
        elif pedido[0] == 70:

            resposta = self.pool.statis2('ALL')   
          

        return self.listToBytes(resposta)

    # fim do metodo processMessage

    def bytesToList(self, msg_bytes):
        return pickle.loads(msg_bytes)

    def listToBytes(self, resposta):
        return pickle.dumps(resposta)
    
    def clear_expired_subs(self):
        self.pool.clear_expired_subs()