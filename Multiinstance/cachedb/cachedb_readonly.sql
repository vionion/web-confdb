-- ------------------------------------------------------------------------------- --   
-- TABLES FOR SIMPLE DICTS VERSION 2 WITH TYPE -  MULTI INSTANCE READONLY BROWSER  --
-- ------------------------------------------------------------------------------- --

-- 
-- For all the items in the Path tree: paths, sequences and modules. 
--
CREATE TABLE patsMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);

-- 
-- For all the items in the EndPath tree: paths, sequences, modules and output modules. 
--
CREATE TABLE endpatsMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);

-- 
-- For all the items in the Module tab. 
--
CREATE TABLE allmodsMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);

-- 
-- For all the items in the Service tab. 
--
CREATE TABLE srvsMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);

-- 
-- For all the items in the Global Psets tab. 
--
CREATE TABLE gpsMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);

-- 
-- For all the items in the Summray View: Streams, Datasets, and Paths. 
--
CREATE TABLE sumMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);

-- 
-- For all the items in the Folder Explorer View: Folders and Configurations. 
--
CREATE TABLE folsMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);

-- 
-- For all the items in the Streams Tab: Streams, Datasets, and Event Content. 
--
CREATE TABLE strsMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);

-- 
-- For all the items in the Sequence tab: sequences and modules. 
--
CREATE TABLE seqsMapping (id SERIAL PRIMARY KEY, source INTEGER, dbid text, itemtype text);


-- Functions put and get


CREATE or REPLACE FUNCTION uniqueMapping_get(integer, integer, text, text) RETURNS text AS $$                              
DECLARE
    gid ALIAS FOR $1;
    src ALIAS FOR $2;
    tab ALIAS FOR $3;
    ity ALIAS FOR $4;
    _found integer;
    result text;
BEGIN
    EXECUTE format('SELECT 1 FROM %s WHERE %s.id = %L AND %s.source = %L AND %s.itemtype = %L', tab, tab, gid, tab, src, tab, ity);
    GET DIAGNOSTICS _found = ROW_COUNT;
    IF _found > 0 
    THEN EXECUTE format('SELECT %s.dbid FROM %s WHERE %s.id = %L AND %s.source = %L AND %s.itemtype = %L', tab, tab, tab, gid, tab, src, tab, ity)
    INTO result;
    RETURN result;
    ELSE
    RETURN -1;
    END IF;
END;
    
$$ LANGUAGE plpgsql;

CREATE or REPLACE FUNCTION uniqueMapping_put(text, integer, text, integer, text) RETURNS integer AS $$             
DECLARE
    src ALIAS FOR $2;
    srcid ALIAS FOR $1;
    tab ALIAS FOR $3;
    uniq ALIAS FOR $4;
    ity ALIAS FOR $5;
    _found integer;
    _found2 integer;
    result integer;
BEGIN
    EXECUTE format('SELECT 1 FROM %s WHERE %s.source = %L AND %s.dbid = %L AND %s.itemtype = %L', tab, tab, src, tab, srcid, tab, ity);
    GET DIAGNOSTICS _found = ROW_COUNT;
    IF _found > 0 AND uniq = 1 
    THEN EXECUTE format('SELECT %s.id FROM %s WHERE %s.source = %L AND %s.dbid = %L AND %s.itemtype = %L', tab, tab, tab, src, tab, srcid, tab, ity)
    INTO result;
    RETURN result;
    ELSE
        EXECUTE format('LOCK TABLE %s IN ACCESS EXCLUSIVE MODE',tab);
        EXECUTE format('SELECT 1 FROM %s WHERE %s.source = %L AND %s.dbid = %L AND %s.itemtype = %L',tab, tab, src, tab, srcid, tab, ity);
        GET DIAGNOSTICS _found2 = ROW_COUNT;
        IF _found2 > 0 AND uniq = 1 
        THEN EXECUTE format('SELECT %s.id FROM %s WHERE %s.source = %L AND %s.dbid = %L AND %s.itemtype = %L', tab, tab, tab, src, tab, srcid, tab, ity)
        INTO result;
        RETURN result;
        ELSE
        EXECUTE format('INSERT INTO %s VALUES (DEFAULT, %L, %L, %L) RETURNING id',tab, src, srcid, ity)
        INTO result;
        RETURN result;
        END IF;
    END IF;
END;
    
$$ LANGUAGE plpgsql;

