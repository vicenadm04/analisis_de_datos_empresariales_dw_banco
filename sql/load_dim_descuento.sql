-- ============================================================
-- DIM_DESCUENTO
-- No hay datos de descuentos en los CSV. Se carga una fila
-- placeholder para que la tabla BRIDGE_PRESTAMO_DESCUENTO
-- conserve integridad referencial si en el futuro se llena.
-- ============================================================
INSERT INTO DW_BANCO.DIM_DESCUENTO
    (CODIGO_DESCUENTO, DESCRIPCION, TIPO_DESCUENTO, PORCENTAJE_DESCUENTO)
VALUES
    ('NO_APLICA', 'Sin descuento aplicado', 'NINGUNO', 0)
ON CONFLICT (CODIGO_DESCUENTO) DO NOTHING;