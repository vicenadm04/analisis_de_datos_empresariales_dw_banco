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