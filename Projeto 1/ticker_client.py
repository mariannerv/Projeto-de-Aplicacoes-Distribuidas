#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo: 28
Números de aluno: 55945, 58662
"""
# Zona para fazer imports
import socket as s
import sys
import time
from net_client import server_connection


# Programa principal


ID = sys.argv[1]
HostName = sys.argv[2]
porto_TCP = int(sys.argv[3])

cliente = server_connection(HostName,porto_TCP)



while True:
    try:
        
        pedido = input("comando >")
        
        p = pedido.split()
        

        if p[0] == "EXIT":
            
            break

        elif p[0] == "SLEEP":

            time.sleep(int(p[1]))
            
        elif p[0] == 'SUBSCR':
            if len(p) < 3:
                print("FALTAM ARGUMENTOS")
            else:
                comando =  p[0] + " " + str(ID) + " " + p[1]+ " " + p[2]
                cliente.connect()
                resposta = cliente.send_receive(comando)
                cliente.close()
                print("Recebi a seguinte resposta do servidor: " + resposta)

        elif p[0] == 'CANCEL' or p[0] == 'STATUS' or p[0] == 'INFOS' or p[0] == 'STATIS':
            if len(p) < 2:
                print('FALTAM ARGUMENTOS')
            else:
                comando =  p[0] + " " + str(ID)
                for i in range(1, len(p)):
                    comando =  comando + " " + p[i]
                cliente.connect()
                resposta = cliente.send_receive(comando)
                print("Recebi a seguinte resposta do servidor: " + resposta)
                cliente.close()
                
        else:
            print('UNKNOWN COMMAND')
            
    except KeyboardInterrupt:
        cliente.close()
        print('Vou desligar')
        break