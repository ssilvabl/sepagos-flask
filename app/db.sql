-- Crear base de datos
CREATE DATABASE sepagos;

-- Seleccionar la base de datos a utilizar
USE sepagos;

-- Crear tabla users
CREATE TABLE users (
    -- Atributos de la tabla

    -- Llave primaria con autoincremento
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    password VARCHAR(200),
    email VARCHAR(100),
    amount INT,
    date DATETIME,
    rol VARCHAR(50),
    status int
);

-- Creat tabla payments
CREATE TABLE payments (
    -- Atributos

    id INT AUTO_INCREMENT PRIMARY KEY,
    id_users INT,
    name VARCHAR(50),
    amount INT,
    installments INT,
    date_start DATE,
    date_end DATE,
    category VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_users) REFERENCES users(id) ON DELETE CASCADE
);
