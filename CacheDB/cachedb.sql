-- ------------------------------------------------------------------------------- --   
-- TABLES FOR SIMPLE DICTS VERSION 2 WITH TYPE -  MULTI INSTANCE READONLY BROWSER  --
-- ------------------------------------------------------------------------------- --

-- 
-- For all the items in the Path tree: paths, sequences and modules. 
--
CREATE TABLE patsMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);

-- 
-- For all the items in the EndPath tree: paths, sequences, modules and output modules. 
--
CREATE TABLE endpatsMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);

-- 
-- For all the items in the Module tab. 
--
CREATE TABLE allmodsMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);

-- 
-- For all the items in the Service tab. 
--
CREATE TABLE srvsMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);

-- 
-- For all the items in the Global Psets tab. 
--
CREATE TABLE gpsMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);

-- 
-- For all the items in the Summray View: Streams, Datasets, and Paths. 
--
CREATE TABLE sumMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);

-- 
-- For all the items in the Folder Explorer View: Folders and Configurations. 
--
CREATE TABLE folsMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);

-- 
-- For all the items in the Streams Tab: Streams, Datasets, and Event Content. 
--
CREATE TABLE strsMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);

-- 
-- For all the items in the Sequence tab: sequences and modules. 
--
CREATE TABLE seqsMapping (id SERIAL PRIMARY KEY, dbid INTEGER, itemtype text);


-- Functions put and get


CREATE or REPLACE FUNCTION uniqueMapping_get(integer, text, text) RETURNS text AS $$
DECLARE
    gid ALIAS FOR $1;
    tab ALIAS FOR $2;
    ity ALIAS FOR $3;
    _found integer;
    result integer;
BEGIN
    EXECUTE format('SELECT 1 FROM %s WHERE %s.id = %L AND %s.itemtype = %L', tab, tab, gid, tab, ity);
    GET DIAGNOSTICS _found = ROW_COUNT;
    IF _found > 0 
    THEN EXECUTE format('SELECT %s.dbid FROM %s WHERE %s.id = %L AND %s.itemtype = %L', tab, tab, tab, gid, tab, ity)
    INTO result;
    RETURN result;
    ELSE
    RETURN -1;
    END IF;
END;
    
$$ LANGUAGE plpgsql;

CREATE or REPLACE FUNCTION uniqueMapping_put(integer, text, integer, text) RETURNS integer AS $$
DECLARE
    srcid ALIAS FOR $1;
    tab ALIAS FOR $2;
    uniq ALIAS FOR $3;
    ity ALIAS FOR $4;
    _found integer;
    _found2 integer;
    result integer;
BEGIN
    EXECUTE format('SELECT 1 FROM %s WHERE %s.dbid = %L AND %s.itemtype = %L', tab, tab, srcid, tab, ity);
    GET DIAGNOSTICS _found = ROW_COUNT;
    IF _found > 0 AND uniq = 1 
    THEN EXECUTE format('SELECT %s.id FROM %s WHERE %s.dbid = %L AND %s.itemtype = %L', tab, tab, tab, srcid, tab, ity)
    INTO result;
    RETURN result;
    ELSE
        EXECUTE format('LOCK TABLE %s IN ACCESS EXCLUSIVE MODE',tab);
        EXECUTE format('SELECT 1 FROM %s WHERE %s.dbid = %L AND %s.itemtype = %L',tab, tab, srcid, tab, ity);
        GET DIAGNOSTICS _found2 = ROW_COUNT;
        IF _found2 > 0 AND uniq = 1 
        THEN EXECUTE format('SELECT %s.id FROM %s WHERE %s.dbid = %L AND %s.itemtype = %L', tab, tab, tab, srcid, tab, ity)
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
-- For all the params, caching whole object as json.
--
CREATE TABLE params_cache (id SERIAL PRIMARY KEY, data JSON, version_id BIGINT, changed BOOLEAN);

CREATE TABLE endpaths_cache (version_id SERIAL PRIMARY KEY, data JSON);

CREATE TABLE path_items_cache (path_item_id SERIAL PRIMARY KEY, data JSON);

CREATE TABLE path_items_hierarchy (parent_id BIGINT, child_id BIGINT, child_order INTEGER , PRIMARY KEY (parent_id, child_id));

CREATE TABLE modules_names_cache (version_id SERIAL PRIMARY KEY, names text[]);
--
-- For mapping external (oracle) and internal entities' ids
--
CREATE TABLE ext2int_id_mapping (internal_id SERIAL PRIMARY KEY, external_id BIGINT, itemtype text, source INTEGER);

CREATE TABLE event_statements_cache (statement_id BIGINT, statement_rank BIGINT, data JSON, PRIMARY KEY (statement_id, statement_rank));

CREATE TABLE stream_event_hierarchy (stream_id BIGINT, event_id BIGINT, ver_id BIGINT,  PRIMARY KEY (stream_id, event_id, ver_id));

CREATE TABLE event_configs_names_cache (event_id BIGINT, name text, ver_id BIGINT,  PRIMARY KEY (event_id, ver_id));

CREATE TABLE paths_cache (path_id BIGINT, name text, is_endpath INTEGER, data JSON, version_id BIGINT, PRIMARY KEY (path_id, version_id));

CREATE TABLE paths2datasets_relation (dataset_id BIGINT, path_ids BIGINT[], ver_id BIGINT, PRIMARY KEY (dataset_id, ver_id));

CREATE TABLE service_messages (id SERIAL PRIMARY KEY, due_date BIGINT, message text);

CREATE or REPLACE FUNCTION getClientMappings(BIGINT, text, text) RETURNS text[] AS $$
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
