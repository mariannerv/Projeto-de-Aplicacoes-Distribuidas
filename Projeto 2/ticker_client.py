#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_client.py
Grupo: 28
Números de aluno: 55945, 58662
"""
# Zona para fazer imports
import socket as s
import sys
import time
from net_client import server_connection
from ticker_stub import TickerStub


# Programa principal


def valida_comando(comando,cliente):
    lista_comandos = comando.strip().split(" ")

    #SUBSCR

    if lista_comandos[0] == 'SUBSCR':
        if len(lista_comandos) < 3:
            return "MISSING ARGUMENTS"
        elif len(lista_comandos) > 3:
            return "TOO MANY ARGUMENTS"
        else: 
            return [lista_comandos[0], lista_comandos[1],lista_comandos[2], cliente]

    #CANCEL

    if lista_comandos[0] == 'CANCEL':
        if len(lista_comandos) < 2:
            return "MISSING ARGUMENTS"
        elif len(lista_comandos) > 2:
            return "TOO MANY ARGUMENTS"
        else: 
            return [lista_comandos[0], lista_comandos[1], cliente]

    #STATUS

    if lista_comandos[0] == 'STATUS':
        if len(lista_comandos) < 2:
            return "MISSING ARGUMENTS"
        elif len(lista_comandos) > 3:
            return "TOO MANY ARGUMENTS"
        else:
            return [lista_comandos[0], lista_comandos[1], cliente]

    #INFOS

    if lista_comandos[0] == 'INFOS':
        if len(lista_comandos) < 2:
            return "MISSING ARGUMENTS"
        elif len(lista_comandos) > 2:
            return "TOO MANY ARGUMENTS"
        else: 
            return [lista_comandos[0], lista_comandos[1], cliente] 
    
    #STATIS

    if lista_comandos[0] == 'STATIS':
        if len(lista_comandos) < 2:
            return "MISSING ARGUMENTS"

        if lista_comandos[1] == "L":
            if len(lista_comandos) < 3:
                return "MISSING ARGUMENTS"
            elif len(lista_comandos) > 3:
                return "TOO MANY ARGUMENTS"
            else:
                return [lista_comandos[0], lista_comandos[1], lista_comandos[2]]


        if lista_comandos[1] == "ALL":
            if len(lista_comandos) == 2:
                return [lista_comandos[0], lista_comandos[1]]
            else:
                return "MISSING ARGUMENTS"

        #EXIT

        if lista_comandos[0] == "EXIT":
            if len(lista_comandos) == 1:
                return [lista_comandos[0]]
            else:
                return "MISSING ARGUMENTS"


        #SLEEP

        if lista_comandos[0] == "SLEEP":
            if len(lista_comandos) == 2:
                return [lista_comandos[0], lista_comandos[1]]
            else:
                return "MISSING ARGUMENTS"

        else:
            return "UNKNOWN COMMAND"





if len(sys.argv) < 4: 
    print("Parâmetros insuficientes. \n Use: python3 ficheiro.py id_cliente host porto")
elif len(sys.argv) > 4:
    print("Demasiados parâmetros foram utilizados. \n Use: python3 ticker_client.py id_cliente host porto")

else: 

    id_cliente = sys.argv[1]
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])


    checker = True


    cliente_stub = TickerStub(HOST,PORT,id_cliente)
    cliente_stub.connect()

    while checker:
        try:

            comando = input("comando > ")

            comando_validado = valida_comando(comando, id_cliente)

            if comando_validado not in ["MISSING ARGUMENTS", "TOO MANY ARGUMENTS", "UNKNOWN COMMAND"]:

                if comando_validado[0] == "EXIT":
                    checker = False
                
                elif comando_validado[0] == "SLEEP":
                    time.sleep(int(comando_validado[1]))

                else:

                    if comando_validado[0] == "SUBSCR":
                        resposta = cliente_stub.subscribe(comando_validado[1:])

                    elif comando_validado[0] == "CANCEL":
                        resposta = cliente_stub.cancel(comando_validado[1:])

                    elif comando_validado[0] == "STATUS":
                        resposta = cliente_stub.status(comando_validado[1:])

                    elif comando_validado[0] == "INFOS":
                        resposta = cliente_stub.infos(comando_validado[1:])
                    
                    elif comando_validado[0] == "STATIS":
                        resposta = cliente_stub.statis(comando_validado[1:])
                    
                    print("Recebi a seguinte resposta do servidor: " + str(resposta))
            
            else: 
                print(comando_validado)
        except KeyboardInterrupt:
            print("Vou encerrar")
            cliente_stub.disconnect()
            exit()