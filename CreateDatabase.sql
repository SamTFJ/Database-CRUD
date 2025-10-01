CREATE DATABASE crud;

\c crud

CREATE TABLE Product (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    value REAL NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Client (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE Salesman (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE Sales (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    salesman_id BIGINT NOT NULL REFERENCES Salesman(id),
    client_id BIGINT NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    total_value REAL NOT NULL,
    sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_client -- Restrição de Chave estrangeira
    FOREIGN KEY (client_id)
    REFERENCES Client(id)
);

CREATE TABLE Sale_Items (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    sale_id BIGINT NOT NULL REFERENCES Sales(id),
    product_id BIGINT NOT NULL REFERENCES Product(id),
    quantity INT NOT NULL,
    item_value REAL NOT NULL
);

CREATE OR REPLACE VIEW general_stock_report AS
SELECT
    COUNT(id) AS total_of_unique_items,
    SUM(quantity) AS total_units_in_stock,
    SUM(quantity * value) AS total_stock_value,
    AVG(value) AS average_price_per_item
FROM
    Product;


CREATE OR REPLACE VIEW sales_report AS
SELECT
    s.id AS sale_id,
    c.name AS client_name,
    sm.name AS salesman_name,
    p.name AS product_name,
    si.quantity AS quantity_sold,
    si.item_value AS item_value,
    s.total_value AS total_sale_value,
    s.sale_date AS sale_date
FROM
    Sales s
JOIN
    Client c ON s.client_id = c.id
JOIN
    Salesman sm ON s.salesman_id = sm.id
JOIN
    Sale_Items si ON s.id = si.sale_id
JOIN
    Product p ON si.product_id = p.id;  