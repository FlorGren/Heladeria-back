DROP DATABASE IF EXISTS heladeria;

CREATE DATABASE heladeria;

USE heladeria;

CREATE TABLE sabores (
codigo INT NOT NULL PRIMARY KEY,
nombre VARCHAR(40),
imagen VARCHAR(40)
);

SELECT * FROM sabores;

INSERT INTO sabores VALUES 
(1, 'Vainilla', 'vainilla.jpg'), 
(2, 'Granizado', 'granizado.jpg'), 
(3, 'Chocolate', 'chocolate.jpg'), 
(4, 'Frutilla', 'frutilla.jpg');

DELETE FROM sabores WHERE codigo= 2;

UPDATE sabores
SET nombre= 'Dulce de Leche',
imagen= 'dulcedeleche.jpg'
WHERE codigo= 4;