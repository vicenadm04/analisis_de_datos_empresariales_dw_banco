-- ============================================================
-- DIM_PROPOSITO
-- Origen: loans.csv.purpose (un valor por préstamo)
-- Normalización: UPPER + TRIM. Descripción legible: capitalize.
-- ============================================================
INSERT INTO DW_BANCO.DIM_PROPOSITO (CODIGO_PROPOSITO, DESCRIPCION)
SELECT DISTINCT
    upper(DW_BANCO.fn_clean_text(purpose)) AS codigo_proposito,
    initcap(replace(lower(DW_BANCO.fn_clean_text(purpose)), '_', ' ')) AS descripcion
FROM STG_BANCO.stg_loan
WHERE DW_BANCO.fn_clean_text(purpose) IS NOT NULL
ON CONFLICT (CODIGO_PROPOSITO) DO NOTHING;

-- Propósito desconocido (fallback)
INSERT INTO DW_BANCO.DIM_PROPOSITO (CODIGO_PROPOSITO, DESCRIPCION)
VALUES ('DESCONOCIDO', 'Propósito desconocido')
ON CONFLICT (CODIGO_PROPOSITO) DO NOTHING;