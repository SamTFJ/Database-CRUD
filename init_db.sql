-- init_db.sql
CREATE TABLE IF NOT EXISTS item (
  id SERIAL PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  value NUMERIC(10,2) NOT NULL DEFAULT 0.00,
  quantity INTEGER NOT NULL DEFAULT 0,
  category VARCHAR(80),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_item_name ON item (name);

-- inicial data (seed)
INSERT INTO item (name, value, quantity, category)
VALUES
  ('Caneta Azul', 1.50, 100, 'Papelaria'),
  ('Caderno 200pg', 12.90, 50, 'Papelaria'),
  ('Copo Plastico', 0.90, 300, 'Utensilios')
ON CONFLICT (id) DO NOTHING;
