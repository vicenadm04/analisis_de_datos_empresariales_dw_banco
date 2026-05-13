-- ============================================================
-- Helpers SQL: función para parsear fechas en múltiples formatos
-- (issue_d viene a veces como 'YYYY-MM-DD' y a veces como 'Mon-YYYY').
-- Se define IMMUTABLE para permitir uso en índices/expresiones.
-- ============================================================
CREATE OR REPLACE FUNCTION DW_BANCO.fn_parse_date_flex(p_text TEXT)
RETURNS DATE
LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE
    v_clean TEXT;
    v_result DATE;
BEGIN
    IF p_text IS NULL THEN
        RETURN NULL;
    END IF;
    v_clean := btrim(p_text);
    IF v_clean = '' OR upper(v_clean) IN ('NULL', 'N/A', 'NA', 'NONE') THEN
        RETURN NULL;
    END IF;

    -- ISO date
    BEGIN
        RETURN v_clean::DATE;
    EXCEPTION WHEN OTHERS THEN
        -- continuar
    END;

    -- Formato 'Mon-YYYY' (ej: 'May-2020')
    BEGIN
        RETURN to_date('01-' || v_clean, 'DD-Mon-YYYY');
    EXCEPTION WHEN OTHERS THEN
        -- continuar
    END;

    -- Formato 'MM/DD/YYYY'
    BEGIN
        RETURN to_date(v_clean, 'MM/DD/YYYY');
    EXCEPTION WHEN OTHERS THEN
        -- continuar
    END;

    RETURN NULL;
END;
$$;

-- Convierte un texto a numérico, removiendo símbolos comunes
-- ('%', '$', espacios y comas). Devuelve NULL si no se puede.
CREATE OR REPLACE FUNCTION DW_BANCO.fn_parse_numeric(p_text TEXT)
RETURNS NUMERIC
LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE
    v_clean TEXT;
BEGIN
    IF p_text IS NULL THEN
        RETURN NULL;
    END IF;
    v_clean := btrim(p_text);
    IF v_clean = '' OR upper(v_clean) IN ('NULL', 'N/A', 'NA', 'NONE') THEN
        RETURN NULL;
    END IF;
    v_clean := replace(replace(replace(v_clean, '%', ''), '$', ''), ',', '');
    v_clean := btrim(v_clean);
    BEGIN
        RETURN v_clean::NUMERIC;
    EXCEPTION WHEN OTHERS THEN
        RETURN NULL;
    END;
END;
$$;

-- Normaliza valores "vacíos" textuales a NULL real.
CREATE OR REPLACE FUNCTION DW_BANCO.fn_clean_text(p_text TEXT)
RETURNS TEXT
LANGUAGE sql IMMUTABLE AS $$
    SELECT CASE
        WHEN p_text IS NULL THEN NULL
        WHEN btrim(p_text) = '' THEN NULL
        WHEN upper(btrim(p_text)) IN ('NULL','N/A','NA','NONE','-') THEN NULL
        ELSE btrim(p_text)
    END;
$$;