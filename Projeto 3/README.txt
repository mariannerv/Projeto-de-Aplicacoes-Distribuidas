NOTAS:

POSSÍVEIS IATAs para usar nas locations: LIS, MAD, ORY, DUB, BRU, LJU, AMS, BER, FCO, VIE (Lisboa, Madrid, Paris, Dublin, Bruxelas, Liubliana, Amsterdão, Berlim, Roma e Viena respetivamente)

- Como a Flight API precisa de um local de partida e de chegada, assumimos que o utilizador passa estes dois parametros ao cliente + o custo.

- Como temos de ler os ficheiros json disponibilizados no moodle para ler os dados sobre o tempo no destino (e sobre os voos), decidimos que no comando search
o utilizador vai ter de passar também a data de partida e de regresso no formato YYYY-MM-DD. 

- É necessário correr o comando SEARCH no terminal do cliente antes de aceder ao link pelo Firefox.

- Quando se fala em lista de IDs de viagens nós assumimos que são os IDs na tabela Roundtrips.



Limitações:


- No DETAILS, como os ids das Roundtrips na base de dados contêm sinais e afins, por norma dá erro. Mudei na base de dados manualmente um dos IDs por forma a testar
por isso se quiser pode utilizar o seguinte ID num browser e funciona: 481194dfaf478a75ms 

- Só mesmo o DETAILS e o SEARCH é que dão para ser vizualizados pelo browser, de resto tem de ser pelo terminal do cliente.

- Se não houver nenhum voo dentro do preço máximo que o cliente dá, o programa corre sem problemas mas não imprime nenhuma mensagem, simplesmente
não adiciona nada às tabelas Legs e Roundtrips.

SEARCH LIS MAD 2023-04-21 2023-04-25 250 , por exemplo adiciona dados às tabelas Weathers e Airlines mas não adiciona nada às outras tabelas
pois não existem voos dentro deste preço.

- No comando FILTER DST, não dá para filtrar pelos dias de sol. Não conseguimos fazer com que a query funcionasse para isso. 

- No comando DETAILS não conseguimos pôr as datas todas na mesma row por isso vão ser retornadas 5 rows para cada dia mas os dados que não sejam da tabela Weathers vão ser os mesmos.


