-- ------------------------------------------------------------------------------- --   
-- TABLES FOR SIMPLE DICTS VERSION 2 WITH TYPE -  MULTI INSTANCE READONLY BROWSER  --
-- ------------------------------------------------------------------------------- --

-- 
-- For all the items in the Path tree: paths, sequences and modules. 
--
CREATE TABLE patsMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);

-- 
-- For all the items in the EndPath tree: paths, sequences, modules and output modules. 
--
CREATE TABLE endpatsMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);

-- 
-- For all the items in the Module tab. 
--
CREATE TABLE allmodsMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);

-- 
-- For all the items in the Service tab. 
--
CREATE TABLE srvsMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);

-- 
-- For all the items in the Global Psets tab. 
--
CREATE TABLE gpsMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);

-- 
-- For all the items in the Summray View: Streams, Datasets, and Paths. 
--
CREATE TABLE sumMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);

-- 
-- For all the items in the Folder Explorer View: Folders and Configurations. 
--
CREATE TABLE folsMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);

-- 
-- For all the items in the Streams Tab: Streams, Datasets, and Event Content. 
--
CREATE TABLE strsMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);

-- 
-- For all the items in the Sequence tab: sequences and modules. 
--
CREATE TABLE seqsMapping (id SERIAL PRIMARY KEY, dbid text, itemtype text);


-- Functions put and get


CREATE or REPLACE FUNCTION uniqueMapping_get(integer, text, text) RETURNS text AS $$
DECLARE
    gid ALIAS FOR $1;
    tab ALIAS FOR $2;
    ity ALIAS FOR $3;
    _found integer;
    result text;
BEGIN
    EXECUTE format('SELECT 1 FROM %s WHERE %s.id = %L AND %s.itemtype = %L', tab, tab, gid, tab, tab, ity);
    GET DIAGNOSTICS _found = ROW_COUNT;
    IF _found > 0 
    THEN EXECUTE format('SELECT %s.dbid FROM %s WHERE %s.id = %L AND %s.itemtype = %L', tab, tab, tab, gid, tab, tab, ity)
    INTO result;
    RETURN result;
    ELSE
    RETURN -1;
    END IF;
END;
    
$$ LANGUAGE plpgsql;

CREATE or REPLACE FUNCTION uniqueMapping_put(text, text, integer, text) RETURNS integer AS $$
DECLARE
    srcid ALIAS FOR $1;
    tab ALIAS FOR $2;
    uniq ALIAS FOR $3;
    ity ALIAS FOR $4;
    _found integer;
    _found2 integer;
    result integer;
BEGIN
    EXECUTE format('SELECT 1 FROM %s WHERE %s.dbid = %L AND %s.itemtype = %L', tab, tab, tab, srcid, tab, ity);
    GET DIAGNOSTICS _found = ROW_COUNT;
    IF _found > 0 AND uniq = 1 
    THEN EXECUTE format('SELECT %s.id FROM %s WHERE %s.dbid = %L AND %s.itemtype = %L', tab, tab, tab, tab, srcid, tab, ity)
    INTO result;
    RETURN result;
    ELSE
        EXECUTE format('LOCK TABLE %s IN ACCESS EXCLUSIVE MODE',tab);
        EXECUTE format('SELECT 1 FROM %s WHERE %s.dbid = %L AND %s.itemtype = %L',tab, tab, tab, srcid, tab, ity);
        GET DIAGNOSTICS _found2 = ROW_COUNT;
        IF _found2 > 0 AND uniq = 1 
        THEN EXECUTE format('SELECT %s.id FROM %s WHERE %s.dbid = %L AND %s.itemtype = %L', tab, tab, tab, tab, srcid, tab, ity)
        INTO result;
        RETURN result;
        ELSE
        EXECUTE format('INSERT INTO %s VALUES (DEFAULT, %L, %L) RETURNING id',tab, srcid, ity)
        INTO result;
        RETURN result;
        END IF;
    END IF;
END;
    
$$ LANGUAGE plpgsql;


--
-- For all the modules, caching whole object as json.
--
CREATE TABLE modules_cache (id SERIAL PRIMARY KEY, module_id INTEGER, data JSON);

--
-- For mapping external (oracle) and internal entities' ids
--
CREATE TABLE ext2int_id_mapping (internal_id SERIAL PRIMARY KEY, external_id INTEGER, itemtype text, source INTEGER);


CREATE or REPLACE FUNCTION getClientMappings(integer, text, text) RETURNS text[] AS $$
DECLARE
    external_id ALIAS FOR $1;
    tabl ALIAS FOR $2;
    item_type ALIAS FOR $3;
    result text[];
    i INT;
    rec record;
BEGIN
    i := 0;
    FOR rec IN EXECUTE format('SELECT id FROM %s WHERE dbid = %L AND itemtype = %L', tabl, external_id, item_type) LOOP
        result[i] := rec.id;
        i := i+1;
    END LOOP;
    RETURN result;
END;

$$ LANGUAGE plpgsql;
