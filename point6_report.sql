-- point6_report.sql
-- Single SQL report for requirement point 6
-- When you run this file with: psql -d estoque -f point6_report.sql
-- it will first output a general summary and then a breakdown by category.

-- 1) General inventory summary
SELECT
  (SELECT COUNT(*) FROM item) AS total_item_records,
  (SELECT COALESCE(SUM(value * quantity),0)::numeric(14,2) FROM item) AS total_inventory_value,
  (SELECT COALESCE(SUM(quantity),0) FROM item) AS total_units,
  (SELECT COUNT(DISTINCT COALESCE(category,'Uncategorized')) FROM item) AS total_categories;

-- Blank line to separate outputs visually
SELECT '' AS separator;

-- 2) Breakdown by category (category, number of item rows, total units, total value, average unit value, most recent addition)
SELECT
  COALESCE(category, 'Uncategorized') AS category,
  COUNT(*) AS items_count,
  SUM(quantity) AS total_quantity,
  SUM(value * quantity)::numeric(14,2) AS total_value,
  AVG(value)::numeric(10,2) AS avg_unit_value,
  MAX(created_at) AS last_added_at
FROM item
GROUP BY category
ORDER BY total_value DESC;
