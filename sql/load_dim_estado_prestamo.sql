-- ============================================================
-- DIM_ESTADO_PRESTAMO
-- Catálogo fijo según la consigna + un estado "DESCONOCIDO".
-- ============================================================
INSERT INTO DW_BANCO.DIM_ESTADO_PRESTAMO (CODIGO_ESTADO, DESCRIPCION) VALUES
    ('CHARGED_OFF',         'Préstamo castigado / pérdida'),
    ('CURRENT',             'Préstamo vigente'),
    ('DEFAULT',             'Incumplimiento / default'),
    ('FULLY_PAID',          'Préstamo pagado completamente'),
    ('IN_GRACE_PERIOD',     'En período de gracia'),
    ('ISSUED',              'Préstamo emitido'),
    ('LATE_16_30_DAYS',     'Atrasado 16-30 días'),
    ('LATE_31_120_DAYS',    'Atrasado 31-120 días'),
    ('DESCONOCIDO',         'Estado desconocido')
ON CONFLICT (CODIGO_ESTADO) DO NOTHING;