-- tests/test_indexes.sql
-- Verifica los índices para la ficha (Postgres)
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename IN ('productos','inventario')
  AND indexname LIKE 'idx_fashion_%';
