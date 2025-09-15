CREATE TABLE item (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    value REAL NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE VIEW general_stock_report AS
SELECT
    COUNT(id) AS total_of_unique_items,
    SUM(quantity) AS total_units_in_stock,
    SUM(quantity * value) AS total_stock_value,
    AVG(value) AS average_price_per_item
FROM
    item;
