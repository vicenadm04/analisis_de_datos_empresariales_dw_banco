-- ============================================================
-- DIM_TIPO_PRESTAMO
-- No existe en CSV; se deriva del campo "term" de loans.
-- Catálogo controlado: TERM_36, TERM_60 (y futuros).
-- ============================================================
INSERT INTO DW_BANCO.DIM_TIPO_PRESTAMO (CODIGO_TIPO, DESCRIPCION)
VALUES
    ('TERM_36',  'Préstamo a 36 meses'),
    ('TERM_60',  'Préstamo a 60 meses'),
    ('TERM_DESCONOCIDO', 'Plazo desconocido')
ON CONFLICT (CODIGO_TIPO) DO NOTHING;