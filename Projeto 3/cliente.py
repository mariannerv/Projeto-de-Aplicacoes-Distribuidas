#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 3 - Cliente.py
Grupo: 28
Números de aluno: 55945, 58662
"""
# Zona para fazer imports

import requests
import json
import re

# Programa principal

checker = True
while checker:
    try:

        comando = input("comando > ")
        
        lista_comando = comando.strip().split()

        date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$') #Para confirmar se o utilizador usa o formato de datas certo (YYYY-MM-DD)

        if lista_comando[0] == 'EXIT':
            if len(lista_comando) > 1:
                print('Too many arguments!')
            else:
                print('Vou fechar!')
                checker = False
        
        #SEARCH <local partida> <local destino> <data_partida> <data_regresso> <custo>
        if lista_comando[0] == 'SEARCH':
            if len(lista_comando) > 6:
                print(
                    "Argumentos a mais! Use: SEARCH <local partida> <local destino> <data_partida> <data_regresso> <custo> ")
            elif len(lista_comando) < 6:
                print(
                    "Argumentos em falta! Use: SEARCH <local partida> <local destino> <data_partida> <data_regresso> <custo>")

            elif lista_comando[1] not in ['LIS', 'MAD', 'ORY', 'DUB', 'BRU', 'LJU', 'AMS', 'BER', 'FCO', 'VIE']:
                print("Local de partida invalido! Os locais de partida disponiveis sao: LIS, MAD, CDG, DUB, BRU, LJU, AMS, BER, FCO, VIE")
            elif lista_comando[2] not in ['LIS', 'MAD', 'ORY', 'DUB', 'BRU', 'LJU', 'AMS', 'BER', 'FCO', 'VIE']:
                print("Local de destino invalido! Os destinos disponiveis sao: LIS, MAD, ORY, DUB, BRU, LJU, AMS, BER, FCO, VIE")
            elif not date_regex.match(lista_comando[3]):
                print("O formato da data de partida não é o correto, use o formato YYYY-MM-DD")
            elif not date_regex.match(lista_comando[4]):
                print("O formato da data de chegada não é o correto, use o formato YYYY-MM-DD")
            else:
               
                dados_pesquisa = {"local_partida": lista_comando[1], "local_destino": lista_comando[2], "data_partida": lista_comando[3], "data_regresso": lista_comando[4], "custo": lista_comando[5]}
                r = requests.post('http://localhost:5000/search/', json=dados_pesquisa)
                print("Status: " + str(r.status_code))
                print(r.content.decode())
                print(r.headers)
                

        # FILTER DST <location> <airline_code> <ids_viagens>
        elif lista_comando[0] == 'FILTER' and len(lista_comando) > 1:
            if lista_comando[1] == 'DST':
                if len(lista_comando) < 5:
                    print(
                        'Argumentos em falta! Use: FILTER DST <location> <airline_code> <lista_ids_viagens>')
                elif lista_comando[2] not in ['LIS', 'MAD', 'ORY', 'DUB', 'BRU', 'LJU', 'AMS', 'BER', 'FCO', 'VIE']:
                    print("Local de destino invalido! Os destinos disponiveis sao: LIS, MAD, ORY, DUB, BRU, LJU, AMS, BER, FCO, VIE")
                else:
                    viagens = lista_comando[4:]
                    dados_filter = {
                        "location": lista_comando[2], "airline_code": lista_comando[3], "viagens": viagens}
                    r = requests.post('http://localhost:5000/filter/dst', json=dados_filter)
                    print("Status: " + str(r.status_code))
                    print(r.content.decode())
                    print(r.headers)
                    print('***')
            elif lista_comando[1] == 'DIVERSIFY':
                if len(lista_comando) < 3:
                    print('Argumentos em falta! Use: FILTER DIVERSIFY <IDs das viagens>')
                else:
                    viagens = lista_comando[2:]
                    dados_diversify = {'lista_viagens': viagens}
                    r = requests.post('http://localhost:5000/filter/diversify', json=dados_diversify)
                    print("Status: " + str(r.status_code))
                    print(r.content.decode())
                    print(r.headers)
                    print('***')
            else:
                print('Comando inválido! Use FILTER DST ou FILTER DIVERSIFY')

        
        #DETAILS <viagem_id>

        elif lista_comando[0] == 'DETAILS':
            if len(lista_comando) > 2:
                print('Argumentos a mais! Use: DETAILS <viagem_id>')
            elif len(lista_comando) < 2:
                print('Argumentos em falta! Use: DETAILS <viagem_id>')
            else:
                dados_details = {'id_viagem' : lista_comando[1]}
                r = requests.post('http://localhost:5000/details/', json=dados_details)
                print("Status: " + str(r.status_code))
                print(r.content.decode())
                print(r.headers)
                print('***')

        else:
            print("Comando desconhecido. Os comandos disponiveis sao: \n \n - SEARCH <local partida> <local destino> <data_partida> <data_regresso> <custo> \n - FILTER DST <location> <airline_code> <ids_viagens> \n - FILTER DIVERSIFY <lista ids> \n - DETAILS <viagem_id> \n ")


    except KeyboardInterrupt:
        print("Vou fechar!")
        checker = False
