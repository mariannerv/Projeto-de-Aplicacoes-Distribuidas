# -*- coding: utf-8 -*-

"""
Aplicações distribuídas - Projeto 2 - ticker_pool.py
Grupo: 28
Números de aluno: 55945, 58662
"""

import time
from datetime import timedelta
import socket as s
import random
import string
import sock_utils

###############################################################################

class resource:

    def __init__(self, resource_id):
        """

        Args:
            resource_id (int): id do recurso 
        """
        self.ID = int(resource_id)
        self.lista_subs = [] #lista de tuplos do tipo (client_id, tempo_limite)
        self.Valor = random.randint(100,200) #valor escolhido entre 100 e 200
        self.NOME = ''.join(random.choice(string.ascii_lowercase)for _ in range(7)) #aqui vai ser criada uma string random com 7 caracteres
        self.SIMBOLO = self.NOME[0] * 3

    def subscribe(self, client_id, time_limit):
        """Adiciona à lista "lista_subs" um tuplo novo com o respetivo cliente e tempo_limite de 
        subscrição.

        Args:
            client_id (int): id do cliente que vai subscrever o recurso
            time_limit (int): tempo de subscrição do recurso
        """
        self.client_id = client_id
        self.time_limit = time_limit
        conju = (self.client_id, int(self.time_limit) + time.time())
        self.lista_subs.append(conju)



    def unsubscribe(self, client_id):
        """Atualiza a lista de subscritores, retirando o cliente com o id "client_id"

        Args:
            client_id (int): id do cliente que vai cancelar subscrição
        """
        new_subs = []
        for i in self.lista_subs:
            if int(client_id) != int(next(iter(i))):
                new_subs.append(i)
        self.lista_subs = new_subs


    def status(self, client_id):  
        """ Esta função verifica se o cliente faz parte da lista de subscritos.

        Args:
            client_id (int): id do cliente

        Returns:
            str: Devolve "SUBSCRIBED" caso o cliente esteja em lista_subs, e UNSUBSCRIBED caso contrário.
        """
        
        for y in self.lista_subs:
            if int(client_id) == int(next(iter(y))):
                return "SUBSCRIBED"
        else:

            return "UNSUBSCRIBED"

    def __repr__(self):
        output = f'Recurso("{self.ID}", "{self.lista_subs}")'
        # R <resource_id> <list of subscribers>
        return output



class resource_pool:
    def __init__(self, N, K, M):
        """

        Args:
            N (int): Número max de subs por acao
            K (int): Numero max de acoes por cliente
            M (int): numero de recursos gerido pelo servidor
        """
        self.maxSubs = int(N)
        self.maxAcoes = int(K)
        self.nRecursos = int(M)

        self.ListaRecursos = []
        for i in range(M):
            r = resource(i)
            self.ListaRecursos.append(r)
            


    def clear_expired_subs(self):

        """Verifica, para cada cliente em lista_subs, se o tempo de subscrição 
        já passou e retira o cliente da lista caso isso se verifique
        """

        current_time = time.time()

        for r in self.ListaRecursos:
            for sub in r.lista_subs:
                if current_time > sub[1]:
                    r.unsubscribe(sub[0])
                else:
                    pass
        



    def subscribe(self, resource_id, client_id, time_limit):
        """subscreve um determinado recurso, durante 
        um tempo de concessão específico (em segundos) para o cliente que está a enviar o pedido

        Args:
            resource_id (int): id do recurso a subscrever
            client_id (int): id do cliente que vai subscrever o recurso
            time_limit (int): tempo de concessão (em segundos)

        Returns:
            str:    • Em geral, se o recurso existir, o servidor deverá registar o pedido, e retornar OK.
                    • Se o pedido for para um recurso já subscrito pelo cliente, o novo Deadline deverá ser atualizado, e
                    retornar OK.
                    • Se o recurso não existir, o servidor deverá retornar UNKNOWN-RESOURCE
                    • Se o cliente já tiver ativas K subscrições, o servidor deverá retornar NOK.
                    • Se o recurso já tiver ativas N subscrições, o servidor deverá retornar NOK.

        """
    
        # encontra o recurso com o ID correspondente
        res = None
        for r in self.ListaRecursos:
            if r.ID == resource_id:
                res = r
                break

        # se o recurso não for encontrado, retorna UNKNOWN-RESOURCE
        if res is None:
            return [11, None]

        # verifica se o cliente já tem K subscrições ativas
        n_active_subs = 0
        for r in self.ListaRecursos:
            
            for sub in r.lista_subs:
                if sub[0] == client_id:
                    n_active_subs += 1
        if n_active_subs >= self.maxAcoes:
            return [11,False]

        # verifica se o recurso já tem N subscrições ativas
        if len(res.lista_subs) >= self.maxSubs:
            return [11, False]

        # subscreve o cliente no recurso, atualizando o tempo limite
        res.subscribe(client_id, time_limit)

        return [11, True]

    def unsubscribe(self, resource_id, client_id):
        """remove uma subscrição ativa numa determinada ação/recurso para o 
        cliente que está a enviar o pedido. 

        Args:
            resource_id (int): id do recurso    
            client_id (int): id do cliente que quer cancelar a subscrição

        Returns:
        str:    • Em geral, se o recurso existir e estiver subscrito pelo cliente, o servidor deverá registar o pedido, e 
                retornar OK.
                • Se o recurso não existir, o servidor deverá retornar UNKNOWN-RESOURCE.
                • Se o pedido for para um recurso não subscrito pelo cliente, o servidor deverá retornar NOK
        """ 
        for y in self.ListaRecursos:
            if int(resource_id) == int(y.ID):
                if y.status(int(client_id)) == "SUBSCRIBED":
                    y.unsubscribe(int(client_id))
                    return [21, True]
                else:
                    return [21, False]
        return [21, None]


    def status(self, resource_id, client_id):
        """é utilizado para obter o estado atual de um determinado recurso face 
        ao cliente em questão

        Args:
            resource_id (int): id do recurso
            client_id (int): id do cliente em questão

        Returns:
            str: • O servidor retorna o estado do recurso solicitado (i.e., SUBSCRIBED, UNSUBSCRIBED). 
                • Se o pedido se referir a um recurso inexistente, o servidor deverá retornar UNKNOWN-RESOURCE
        """
        for y in self.ListaRecursos: 
            if int(resource_id) == int(y.ID):
                return [31, y.status(int(client_id))]
                
        else:
            return [31,None]

    def infos(self, option, client_id):
        """ Utilizado para obter informações sobre o cliente no servidor.

        Args:
            option (str): Opção a escolher, pode ser K ou M.
            client_id (int): id do client em questão.

        Returns:
            str: • INFOS M – retorna  <lista de recursos-ID subscritos pelo cliente> 
                • INFOS K – retorna o <número total de ações a que o cliente ainda pode subscrever>
        """
        res = []
        recursos_subscritos = []
        for y in self.ListaRecursos:
            if y.status(int(client_id)) == "SUBSCRIBED":
                recursos_subscritos.append(y.ID)
        num_subs = len(recursos_subscritos)
        restantes = self.maxAcoes - num_subs

        if option == "M":
            res.append(41)
            res.append(recursos_subscritos)
        elif option == "K":
            res.append(51)
            res.append(restantes)
        return res
        

    def statis(self,option,resource_id):
        """Função para a opção L 

        Args:
            
            resource_id (int): id do recurso em questão

        Returns:
            str: retorna o numero de subscritores do recurso em questão.
        """
        
        for resource in self.ListaRecursos:
            if resource.ID == int(resource_id):
                n_subs = len(resource.lista_subs)
                return [61, n_subs]
                
        else:

            return [61, None]
            
    def statis2(self,option):    
        """Para a opção ALL

        Returns:
            str:  Cada linha é composta por texto com os seguintes campos (separados por espaços): 
                1. A letra R para indicar um recurso;
                2. O ID do recurso;
                3. O número atual de subscritores desse recurso;
                4. A lista de clientes subscritos (ordenada crescentemente pelo cliente-ID). Não apresentar nada,
                se não houver clientes subscritos.
        """
        fi = []
        res = ""
        for recurso in self.ListaRecursos:
            recurso_id = recurso.ID
            num_subs = len(recurso.lista_subs)
            subs_lista = " ".join(str(sub[0]) for sub in recurso.lista_subs)
            res += f"R {recurso_id} {num_subs} {subs_lista}\n"
            fi.append(f"R {recurso_id} {num_subs} {subs_lista}\n")
        return [70, fi]
            



    def __repr__(self):
            output = ""
            for i, resource in enumerate(self.ListaRecursos):
                num_subs = len(resource.lista_subs)
                subs_lista = ", ".join([str(sub[0]) for sub in resource.lista_subs])
                output += f"R {i} {num_subs} [{subs_lista}]\n"
            return output
        
