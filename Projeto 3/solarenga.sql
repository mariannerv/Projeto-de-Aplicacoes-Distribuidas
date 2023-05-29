/*
Aplicações Distribuídas - Projeto 3 - solarenga.sql
Grupo: 28
Números de aluno: 55945, 58662
*/


PRAGMA foreign_keys = ON;

CREATE TABLE legs (
    id TEXT PRIMARY KEY,
    dep_IATA TEXT,
    arr_IATA TEXT,
    dep_datetime TEXT,
    arr_datetime TEXT,
    airlineCodes TEXT,
    duration_mins INTEGER

    
); 

CREATE TABLE weather(
    id INTEGER PRIMARY KEY, 
    dates TEXT,
    location TEXT,
    condition TEXT,
    mintemp_c DECIMAL(4,1),
    maxtemp_c DECIMAL(4,1),	

    FOREIGN KEY (location) REFERENCES locations(IATA) ON DELETE CASCADE
);

CREATE TABLE roundtrips(
    id TEXT PRIMARY KEY,
    cost DECIMAL (10,2),
    id_leg0 TEXT,
    id_leg1 TEXT,
    
    FOREIGN KEY(id_leg0) REFERENCES legs(id) ON DELETE CASCADE,
    FOREIGN KEY(id_leg1) REFERENCES legs(id) ON DELETE CASCADE
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    nome TEXT,
  	IATA VARCHAR(3) UNIQUE,
    wea_name TEXT
);

CREATE TABLE airlines (
    code TEXT PRIMARY KEY,
    nome TEXT
);


INSERT INTO locations (id, nome, IATA, wea_name) VALUES
        (1, 'Lisbon', 'LIS', 'Lisboa'),
        (2, 'Madrid', 'MAD', 'Madrid'),
        (3, 'Paris', 'ORY', 'Paris'),
        (4, 'Dublin', 'DUB', 'Dublin'),
        (5, 'Brussels', 'BRU', 'Bruxelas'),
        (6, 'Liubliana', 'LJU', 'Liubliana'),
        (7, 'Amsterdam', 'AMS', 'Amsterdao'),
        (8, 'Berlin', 'BER', 'Berlim'),
        (9, 'Rome', 'FCO', 'Roma'),
        (10, 'Vienna', 'VIE', 'Viena');
