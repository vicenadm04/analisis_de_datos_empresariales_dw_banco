WITH suc_clean AS (
    SELECT
        id_sucursal     AS codigo_sucursal,
        DW_BANCO.fn_clean_text(nombre_sucursal) AS nombre_sucursal,
        DW_BANCO.fn_clean_text(ciudad)          AS ciudad,
        DW_BANCO.fn_clean_text(state_name_us)   AS provincia,
        DW_BANCO.fn_clean_text(state_us)        AS region,  -- code de estado como "región"
        activa          AS activa_raw,
        id_sucursal
    FROM STG_BANCO.stg_sucursales
    WHERE id_sucursal IS NOT NULL
),
suc_dedup AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY codigo_sucursal ORDER BY id_sucursal DESC) AS rn
    FROM suc_clean
)
INSERT INTO DW_BANCO.DIM_SUCURSAL (
    CODIGO_SUCURSAL, NOMBRE_SUCURSAL, CIUDAD, PROVINCIA, REGION,
    FECHA_INICIO_VIGENCIA, FECHA_FIN_VIGENCIA, REGISTRO_ACTUAL
)
SELECT
    codigo_sucursal,
    COALESCE(nombre_sucursal, 'SIN_NOMBRE'),
    COALESCE(ciudad, 'DESCONOCIDA'),
    provincia,
    region,
    DATE '1900-01-01',  -- default por falta de columna en el origen
    NULL,
    CASE
        WHEN activa_raw = '1' THEN TRUE
        WHEN activa_raw <> '1' THEN FALSE
        ELSE TRUE
    END
FROM suc_dedup
WHERE rn = 1
ON CONFLICT (CODIGO_SUCURSAL) DO UPDATE SET
    NOMBRE_SUCURSAL = EXCLUDED.NOMBRE_SUCURSAL,
    CIUDAD          = EXCLUDED.CIUDAD,
    PROVINCIA       = EXCLUDED.PROVINCIA,
    REGION          = EXCLUDED.REGION,
    REGISTRO_ACTUAL = EXCLUDED.REGISTRO_ACTUAL;