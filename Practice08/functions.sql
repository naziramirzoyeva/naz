CREATE OR REPLACE FUNCTION get_contacts_by_pattern(search_term TEXT)
RETURNS TABLE(name_out VARCHAR, phone_out VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    WHERE name ILIKE '%' || search_term || '%' 
       OR phone ILIKE '%' || search_term || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE(name_out VARCHAR, phone_out VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    ORDER BY name 
    LIMIT p_limit 
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;