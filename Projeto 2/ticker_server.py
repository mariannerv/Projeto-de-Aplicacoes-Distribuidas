#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_server.py
Grupo: 28
Números de aluno: 55945, 58662
"""

# Zona para fazer importação
import sys
import socket as s
import sock_utils
import struct
from ticker_skel import Skeleton 
import select as sel



# código do programa principal


HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
N = int(sys.argv[3])
K = int(sys.argv[4])
M = int(sys.argv[5])

listen_socket = sock_utils.create_tcp_server_socket(HOST, PORT, 1)

servidor_skel = Skeleton(N,K,M)

socket_list = [listen_socket, sys.stdin]
ciclo = True

while ciclo:
    try:
        
        R, W, X = sel.select(socket_list, [], [])  # Espera sockets
        for sckt in R:  # Para socket que vem em R
            if sckt is listen_socket:
                conn_sock, addr = listen_socket.accept()
                addr, port = conn_sock.getpeername()
                print('Novo cliente ligado desde %s:%d' % (addr, port))
                socket_list.append(conn_sock)

            elif sckt is sys.stdin:
                msg = sckt.readline().strip()
                if msg == "EXIT":
                    print("VOU ENCERRAR")
                    sys.exit(0)

            else:
                size_bytes = sckt.recv(4) 
                size = struct.unpack('i', size_bytes)[0]  

                msg_bytes = sock_utils.receive_all(sckt, size)

                if msg_bytes:

                    servidor_skel.clear_expired_subs()

                    resp_bytes = servidor_skel.processMessage(msg_bytes)

                    
                    size_resp_bytes = struct.pack("i", len(resp_bytes))
                    
                    sckt.sendall(size_resp_bytes)
                    sckt.sendall(resp_bytes)  

    except (KeyboardInterrupt, SystemExit):

        for sckt in socket_list:
            sckt.close()
            socket_list.remove(sckt)

        break
    except struct.error:  
        sckt.close()
        socket_list.remove(sckt)
        print('Cliente fechou ligação')

    except:
        print(sys.exc_info())

listen_socket.close()

