-- Criação das tabelas
CREATE TABLE proprietarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR
);

CREATE TABLE carros (
    id SERIAL PRIMARY KEY,
    modelo VARCHAR,
    cor VARCHAR,
    proprietario_id INTEGER REFERENCES proprietarios(id)
);

-- Inserção de registros
-- Inserir 30 proprietários
INSERT INTO proprietarios (nome)
VALUES
    ('João'),
    ('Maria'),
    ('José'),
    ('Ana'),
    ('Pedro'),
    ('Mariana'),
    ('Carlos'),
    ('Fernanda'),
    ('Rafael'),
    ('Patrícia'),
    ('Lucas'),
    ('Larissa'),
    ('Gustavo'),
    ('Isabela'),
    ('Paulo'),
    ('Camila'),
    ('Daniel'),
    ('Bruna'),
    ('Thiago'),
    ('Aline'),
    ('Rodrigo'),
    ('Vanessa'),
    ('Marcelo'),
    ('Juliana'),
    ('Felipe'),
    ('Carla'),
    ('Eduardo'),
    ('Laura'),
    ('Leonardo'),
    ('Tatiane');


INSERT INTO carros (modelo, cor, proprietario_id)
SELECT
    modelo,
    cor,
    proprietario_id
FROM
    (SELECT
        'Hatch' AS modelo,
        'Amarelo' AS cor,
        id AS proprietario_id
    FROM
        proprietarios
    UNION ALL
    SELECT
        'Sedã' AS modelo,
        'Azul' AS cor,
        id AS proprietario_id
    FROM
        proprietarios
    UNION ALL
    SELECT
        'Conversível' AS modelo,
        'Cinza' AS cor,
        id AS proprietario_id
    FROM
        proprietarios) AS carros_proprietarios
ORDER BY
    RANDOM() 
LIMIT
    90; 
