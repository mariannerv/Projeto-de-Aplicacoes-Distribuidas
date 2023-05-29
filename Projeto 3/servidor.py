
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 3 - Servidor.py
Grupo: 28
Números de aluno: 55945, 58662
"""
# Zona para fazer imports

from flask import request, jsonify
from flask import Flask, request, make_response
import sqlite3
from os.path import isfile
import json
from datetime import date, timedelta, datetime
import requests
import random
import string


#Programa principal

app = Flask(__name__)



def connect_db(dbname):
    db_is_created = isfile(dbname)
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute('PRAGMA foreign_keys = ON;')
        with app.open_resource('solarenga.sql', mode='r') as file_sql:
            try:
                cursor.executescript(file_sql.read())
            except sqlite3.Error as e:
                print(f"Error executing SQL script: {e}")
        connection.commit()
    return connection, cursor



apiWeatherKey = 'fad6106037f547f0ae6111209231504'

flightAPIKey = '643a889b5648770f668edea8'





#Conta os dias de bom tempo, com base nos dados retornados pela API
def conta_bom_tempo(partida, regresso, weathers):
    bom_tempo = 0

    for daily_data in weathers['forecast']['forecastday']:
        date_str = daily_data['date']
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if datetime.strptime(partida, "%Y-%m-%d").date() <= date <= datetime.strptime(regresso, "%Y-%m-%d").date():
            if daily_data['day']['condition']['text'] == 'Sunny' or daily_data['day']['condition']['text'] == 'Clear' or daily_data['day']['condition']['text'] == 'Partly cloudy':
                bom_tempo += 1
    return bom_tempo



@app.route('/search/<string:local_partida>/<string:local_destino>/<string:data_partida>/<string:data_regresso>/<string:custo>', methods=['GET'])
@app.route('/search/', methods=['POST'])

def search(local_partida = None, local_destino = None, data_partida = None, data_regresso = None, custo = None):

    conn, cursor = connect_db('solarenga.db')
    
    if request.method == 'POST':
        dados_pesquisa = json.loads(request.data)
        local_partida = dados_pesquisa["local_partida"]
        local_destino = dados_pesquisa["local_destino"]
        data_partida = dados_pesquisa["data_partida"]
        data_regresso = dados_pesquisa["data_regresso"]
        max_price = int(dados_pesquisa["custo"])
        

        # #Dados dos voos todos
        #urlFlight = f'http://localhost:9998/roundtrip/{flightAPIKey}/{local_partida}/{local_destino}/{data_partida}/{data_regresso}/1/0/0/Economy/EUR'
        urlFlight = f'http://lmpinto.eu.pythonanywhere.com/roundtrip/aaaaaaaaaaa/{local_partida}/{local_destino}/{data_partida}/{data_regresso}/1/0/0/Economy/EUR'
        responseFlight = requests.get(urlFlight)
        data = responseFlight.json()

        destino_nome_extenso = ''


        #Para o weather saber que ficheiro tem de procurar, não sei se os ficheiros vão ter estes nomes
        if local_destino == 'LIS':
            destino_nome_extenso = 'lisbon'
        elif local_destino == 'MAD':
            destino_nome_extenso = 'madrid'
        elif local_destino == 'ORY':
            destino_nome_extenso = 'paris'
        elif local_destino == 'DUB':
            destino_nome_extenso = 'dublin'
        elif local_destino == 'BRU':
            destino_nome_extenso = 'brussels'
        elif local_destino == 'LJU':
            destino_nome_extenso = 'liubliana'
        elif local_destino == 'AMS':
            destino_nome_extenso = 'amsterdam'
        elif local_destino == 'BER':
            destino_nome_extenso = 'berlin'
        elif local_destino == 'FCO':
            destino_nome_extenso = 'rome'
        elif local_destino == 'VIE':
            destino_nome_extenso = 'vienna'



        # dados do tempo
        #urlWeather = f'http://localhost:9999/v1/forecast.json?q={destino_nome_extenso}&days=14'
        urlWeather = f'https://lmpinto.eu.pythonanywhere.com/v1/forecast.json?key=aaaaaaaaaaa&q={destino_nome_extenso}&days=14'
        #headersWeather = {'Authorization': f'Bearer {apiWeatherKey}'}
        responseWeather = requests.get(urlWeather)
        weathers = responseWeather.json()




        #Checkar se há 2 ou + dias se bom tempo

        dias = conta_bom_tempo(data_partida,data_regresso,weathers)

        #Se não entrar no loop, é isto que vai imprimir
        r = make_response("Não há 2 ou mais dias de bom tempo pelo que não vai ser efetuada nenhuma pesquisa.")

        if dias >= 2:

            #Filtra os voos diretos, dentro do preço máximo e insere os dados na bd

            #INSERIR DADOS NA TABELA LEGS
            for leg in data['legs']:
                for fare in data['fares']:
                    if leg['stopoversCount'] == 0 and fare['price']['totalAmount'] <= max_price:
                        for segment in leg['segments']:
                            # Add data to the LEGS table
                            airline_codes_str = ','.join(leg['airlineCodes'])
                            cursor.execute("INSERT OR IGNORE INTO legs (id, dep_IATA, arr_IATA, dep_datetime, arr_datetime, airlineCodes, duration_mins) VALUES (?, ?, ?, ?, ?, ?, ?)", (
                                leg['id'], leg['departureAirportCode'], leg['arrivalAirportCode'], segment['departureDateTime'], segment['arrivalDateTime'], airline_codes_str, leg['durationMinutes']))
            conn.commit()
            r = make_response('Registos inseridos com sucesso!')
            
            #INSERIR DADOS NA TABELA ROUNDTRIPS
            registos = set()
            for trip in data['trips']:
                for fare in data['fares']:
                    if fare['price']['totalAmount'] <= max_price:
                        translator = str.maketrans('', '', string.punctuation)
                        trip['id'] = trip['id'].translate(translator)
                        registos.add((trip['id'], fare['price']['totalAmount'],
                                    trip['legIds'][0], trip['legIds'][1]))
            cursor.executemany("INSERT OR IGNORE INTO roundtrips VALUES (?, ?, ?, ?)", registos)
            conn.commit()
            r = make_response('Registos inseridos com sucesso!')
            
            #INSERIR DADOS NA TABELA AIRLINES
            for airline in data['airlines']:
                cursor.execute("INSERT OR IGNORE INTO airlines (code, nome) VALUES (?, ?)", (airline['code'], airline['name']))
                conn.commit()
                r = make_response('Registos inseridos com sucesso!')

            #INSERIR DADOS NA TABELA WEATHER
            local = weathers['location']['name']
            forecastday_list = weathers['forecast']['forecastday'] 
            for forecastday in forecastday_list:
                date = forecastday['date']  
                day_dict = forecastday['day']  
                condition_text = day_dict['condition']['text']
                mintemp_c = day_dict['mintemp_c']
                maxtemp_c = day_dict['maxtemp_c']

                random_id = random.randint(100, 100000000)
                cursor.execute("INSERT OR IGNORE INTO weather (id, dates, location, condition, mintemp_c, maxtemp_c) VALUES (?, ?, ?, ?, ?, ?)",
                            (random_id, date, local, condition_text, mintemp_c, maxtemp_c))

            conn.commit() 
            conn.close()
            r = make_response('Registos inseridos com sucesso!')
        else:
            r = make_response("Não há 2 ou mais dias de bom tempo pelo que não vai ser efetuada nenhuma pesquisa.")
        
        return r

    if request.method == 'GET':
        if request.url == 'http://localhost:5000/search/' + str(local_partida) + '/' + str(local_destino) + '/' + str(data_partida) + '/' + str(data_regresso) + '/' + str(custo):
            
            sql_query = """ 
            SELECT r.id, leg0.dep_IATA, leg0.arr_IATA, SUBSTRING(leg0.dep_datetime , 1, 10), SUBSTRING(leg1.dep_datetime , 1, 10), r.cost
            FROM roundtrips r, legs leg0, legs leg1
            WHERE leg0.id = r.id_leg0 AND leg1.id = r.id_leg1 
            AND leg0.dep_IATA = ?  AND leg0.arr_IATA = ? 
            AND SUBSTRING(leg0.dep_datetime , 1, 10) = ?
            AND SUBSTRING(leg1.dep_datetime , 1, 10) = ?
            AND r.cost <= ?
            """

            query_params = [str(local_partida), str(local_destino), str(data_partida), str(data_regresso), int(custo)]

            cursor.execute(sql_query, query_params)

            trips = cursor.fetchall()


        if trips is not None:
            trips_dict = [{'id': trip[0], 'dep_IATA': trip[1], 'arr_IATA': trip[2],
                        'dep_date': trip[3], 'arr_date': trip[4], 'cost': trip[5]} for trip in trips]
            response_dict = {"Trips": trips_dict}
            r = make_response(json.dumps(response_dict))
            r.headers['Content-Type'] = 'application/json'
        else:
            erro = json.dumps({'describedBy': "http://localhost:5000/suporte/",
                               'httpStatus': '404', 'title': 'Nenhum resultado encontrado'})
            r = make_response(erro)
            r.status_code = 404
        conn.close()
        return r


@app.route('/filter/dst/', methods=['POST'])
def search_dst():
    conn, cursor = connect_db('solarenga.db')


        
    dados_filter = json.loads(request.data)
    location = dados_filter['location']
    airline_code = dados_filter['airline_code']
    viagens = dados_filter['viagens']

    sql_query = """
    SELECT DISTINCT l0.id, r.cost, l0.dep_IATA, l0.arr_IATA, l0.dep_datetime, l0.arr_datetime, l1.id, l1.dep_datetime, l1.arr_datetime
    FROM roundtrips r, legs l0, legs l1
    WHERE r.id IN ({}) AND l1.id = r.id_leg1 AND l0.id = r.id_leg0
    AND l0.arr_IATA = ? AND l0.airlineCodes = ?
    """.format(','.join(['?']*len(viagens)))


    
    query_params = viagens + [location, airline_code]
    cursor.execute(sql_query, query_params)
    results = cursor.fetchall()

    if len(results) > 0:


        headers = ['ID', 'custo', 'dep_IATA', 'arr_IATA', 'dep_datetime', 'arr_datetime',
                'regresso_id', 'regresso_dep_datetime', 'regresso_arr_datetime']

        rows = [list(zip(headers, row)) for row in results]

        r = make_response(rows)
    else:
        
        r = make_response('Não foram encontrados registos para os dados pedidos')
        
    return r


@app.route('/filter/diversify/', methods=['POST'])
def filter_diversify(id_viagem = []):
    conn, cursor = connect_db('solarenga.db')
    

    dados_diversify = json.loads(request.data)
    viagens = dados_diversify['lista_viagens']

    sql_query = """
    SELECT l0.id, MIN(r.cost) AS min_cost, l0.dep_IATA, l0.arr_IATA, l0.dep_datetime, l0.arr_datetime, l1.id, l1.dep_datetime, l1.arr_datetime
    FROM roundtrips r, legs l0, legs l1
    WHERE r.id IN ({}) AND l1.id = r.id_leg1 AND l0.id = r.id_leg0
    GROUP BY l0.id, l0.dep_IATA, l0.arr_IATA, l0.dep_datetime, l0.arr_datetime
    ORDER BY min_cost ASC
    """.format(','.join(['?']*len(viagens)))

    query_params = viagens

    cursor.execute(sql_query, query_params)
    results = cursor.fetchall()

    if len(results) > 0:
            
        headers = ['ID', 'custo', 'dep_IATA', 'arr_IATA', 'dep_datetime', 'arr_datetime', 'regresso_id', 'regresso_dep_datetime', 'regresso_arr_datetime']

        rows = [list(zip(headers, row)) for row in results]

        
        r = make_response(rows)
        
    else:
        r = make_response('Não foram encontrados registos para os dados pedidos')
        

    return r




@app.route('/details/<string:viagem_id>', methods = ['GET'])
@app.route('/details/', methods=['POST'])
def details(viagem_id = None):
    conn, cursor = connect_db('solarenga.db')
    
    if request.method == 'POST':  

        dados_details = json.loads(request.data)
        viagem_id = dados_details['id_viagem']

        sql_query = """
        SELECT DISTINCT l0.id, l1.id, r.cost, l0.dep_datetime, l0.arr_datetime, l0.airlineCodes, l0.dep_IATA, l0.arr_IATA, l0.duration_mins, l1.dep_datetime, l1.arr_datetime, l1.airlineCodes, l1.dep_IATA, l1.arr_IATA, l1.duration_mins, w.dates, w.condition, w.mintemp_c, w.maxtemp_c
        FROM legs l0, legs l1, roundtrips r, weather w, locations l
        WHERE r.id = ? 
            AND l0.id = r.id_leg0 
            AND r.id_leg1 = l1.id 
            AND w.dates BETWEEN SUBSTRING(l0.dep_datetime , 1, 10) AND SUBSTRING(l1.dep_datetime , 1, 10)
            AND l0.arr_IATA = l.IATA 
            AND w.location = l.wea_name;
        """

        query_params = [viagem_id]
        cursor.execute(sql_query, query_params)
        results = cursor.fetchall()

        if len(results) > 0:
                
            headers = ['leg0_id', 'leg1_id', 'cost', 'departure_datetime', 'arrival_datetime', 'airline_codes', 'departure_IATA', 'arrival_IATA', 'duration_mins', 'regresso_departure_datetime',
        'regresso_arr_datetime', 'regresso_airline_codes', 'regresso_departure_IATA', 'regresso_arrival_IATA', 'regresso_duration_mins', 'weather_dates', 'weather_condition', 'min_temp', 'max_temp']
            
            rows = [list(zip(headers, row)) for row in results] #para juntar os headers aos resultados
            
            r = make_response(rows)
            
        else: 
            r = make_response('Não foram encontrados registos para os dados pedidos')
            

        return r

    if request.method == 'GET':
        if request.url == 'http://localhost:5000/details/' + str(viagem_id):
            
            sql_query = """
            SELECT DISTINCT l0.id, l1.id, r.cost, l0.dep_datetime, l0.arr_datetime, l0.airlineCodes, l0.dep_IATA, l0.arr_IATA, l0.duration_mins, l1.dep_datetime, l1.arr_datetime, l1.airlineCodes, l1.dep_IATA, l1.arr_IATA, l1.duration_mins, w.dates, w.condition, w.mintemp_c, w.maxtemp_c
            FROM legs l0, legs l1, roundtrips r, weather w, locations l
            WHERE r.id = ? 
                AND l0.id = r.id_leg0 
                AND r.id_leg1 = l1.id 
                AND w.dates BETWEEN SUBSTRING(l0.dep_datetime , 1, 10) AND SUBSTRING(l1.dep_datetime , 1, 10)
                AND l0.arr_IATA = l.IATA 
                AND w.location = l.wea_name;
            """

            query_params = [viagem_id]
            cursor.execute(sql_query, query_params)
            results = cursor.fetchall()

            if results is not None:
                
                r = make_response(json.dumps(results))
                r.headers['Content-Type'] = 'application/json'
                
            else:
                erro = json.dumps({'describedBy': "http://localhost:5000/suporte/",'httpStatus': '404', 'title': 'Nenhum resultado encontrado'})
                r = make_response(erro)
                r.status_code = 404
            conn.close()
            return r

if __name__ == '__main__':

    connect_db('solarenga.db')
    app.run(debug=True, port=5000)
    

    
