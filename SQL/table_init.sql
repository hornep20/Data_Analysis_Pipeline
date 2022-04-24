DROP SCHEMA IF EXISTS finalproject CASCADE;
CREATE SCHEMA finalproject;
SET SEARCH_PATH TO finalproject;

-- Grant cohe_armc the necessary privileges (revoked in post_processing.sql).
GRANT pg_read_server_files TO cohe_armc;
GRANT ALL PRIVILEGES ON SCHEMA finalproject TO cohe_armc;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA finalproject TO cohe_armc;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA finalproject TO cohe_armc;
ALTER DEFAULT PRIVILEGES IN SCHEMA finalproject GRANT ALL PRIVILEGES ON TABLES TO cohe_armc;
ALTER DEFAULT PRIVILEGES IN SCHEMA finalproject GRANT ALL PRIVILEGES ON SEQUENCES TO cohe_armc;


---------------------------------------------------------------------------------------
-- Role
---------------------------------------------------------------------------------------
-- (2) Change role to cohe_armc.
SET ROLE cohe_armc;

CREATE OR REPLACE FUNCTION clean_county(counties TEXT) RETURNS TEXT as $$
DECLARE
    up TEXT := UPPER(counties);
    ret TEXT;
BEGIN
    ret :=
        CASE
            WHEN SUBSTR(counties, length(counties), length(counties)) = '_'
                THEN TRIM(SUBSTR(counties,1,length(counties)-1))
            ELSE
                TRIM(up)
        END;
    return ret;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clean_counties() RETURNS TRIGGER as $$
BEGIN
    SELECT finalproject.clean_county(NEW.counties) INTO NEW.counties;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

---------------------------------------------------------------------------------------
-- Create Tables.
---------------------------------------------------------------------------------------
-- Create the care_2016 table.
DROP TABLE IF EXISTS care_2016;
CREATE TABLE care_2016 (
    Counties    		TEXT,
    None_Care      		INT,
    First_Trimester 	INT,
    Second_Trimester	INT,
    Third_Trimester    	INT,
    Unknown_Care		INT,
	Total_Care			INT,
	Year				TEXT
);

CREATE TRIGGER clean_care_2016
    BEFORE INSERT
    ON care_2016
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the care_2017 table.
DROP TABLE IF EXISTS care_2017;
CREATE TABLE care_2017 (
    Counties    		TEXT,
    None_Care      		INT,
    First_Trimester 	INT,
    Second_Trimester	INT,
    Third_Trimester    	INT,
    Unknown_Care		INT,
	Total_Care			INT,
	Year				TEXT
);

CREATE TRIGGER clean_care_2017
    BEFORE INSERT
    ON care_2017
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the care_2018 table.
DROP TABLE IF EXISTS care_2018;
CREATE TABLE care_2018 (
    Counties    		TEXT,
    None_Care      		INT,
    First_Trimester 	INT,
    Second_Trimester	INT,
    Third_Trimester    	INT,
    Unknown_Care		INT,
	Total_Care			INT,
	Year				TEXT
);

CREATE TRIGGER clean_care_2018
    BEFORE INSERT
    ON care_2018
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the care_2019 table.
DROP TABLE IF EXISTS care_2019;
CREATE TABLE care_2019 (
    Counties    		TEXT,
    None_Care      		INT,
    First_Trimester 	INT,
    Second_Trimester	INT,
    Third_Trimester    	INT,
    Unknown_Care		INT,
	Total_Care			INT,
	Year				TEXT
);

CREATE TRIGGER clean_care_2019
    BEFORE INSERT
    ON care_2019
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the care_total table.
--DROP TABLE IF EXISTS care_total;
--CREATE TABLE care_total (
--    Counties            TEXT,
--    None_Care           INT,
--    First_Trimester     INT,
--    Second_Trimester    INT,
--    Third_Trimester     INT,
 --   Unknown_Care        INT,
--    Total_Care          INT,
--    Year                TEXT
--);

--CREATE TRIGGER clean_care_total
--    BEFORE INSERT
--    ON care_total
--    FOR EACH ROW
--    EXECUTE PROCEDURE clean_counties();


-- Create the gender_2016 table.
DROP TABLE IF EXISTS gender_2016;
CREATE TABLE gender_2016 (
    Counties    		TEXT,
    male      			INT,
    female 				INT,
    unknown_gender		INT,
    total_gender    	INT,
	Year				TEXT
);

CREATE TRIGGER clean_gender_2016
    BEFORE INSERT
    ON gender_2016
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the gender_2017 table.
DROP TABLE IF EXISTS gender_2017;
CREATE TABLE gender_2017 (
    Counties    		TEXT,
    male      			INT,
    female 				INT,
    unknown_gender		INT,
    total_gender    	INT,
	Year				TEXT
);

CREATE TRIGGER clean_gender_2017
    BEFORE INSERT
    ON gender_2017
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the gender_2018 table.
DROP TABLE IF EXISTS gender_2018;
CREATE TABLE gender_2018 (
    Counties    		TEXT,
    male      			INT,
    female 				INT,
    unknown_gender		INT,
    total_gender    	INT,
	Year				TEXT
);

CREATE TRIGGER clean_gender_2018
    BEFORE INSERT
    ON gender_2018
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the gender_2019 table.
DROP TABLE IF EXISTS gender_2019;
CREATE TABLE gender_2019 (
    Counties    		TEXT,
    male      			INT,
    female 				INT,
    unknown_gender		INT,
    total_gender    	INT,
	Year				TEXT
);

CREATE TRIGGER clean_gender_2019
    BEFORE INSERT
    ON gender_2019
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the gender_total table.
--DROP TABLE IF EXISTS gender_total;
--CREATE TABLE gender_total (
--    Counties            TEXT,
--    male                INT,
--    female              INT,
--    unknown_gender      INT,
--    total_gender        INT,
--    Year                TEXT
--);

--CREATE TRIGGER clean_gender_total
--    BEFORE INSERT
--    ON gender_total
 --   FOR EACH ROW
--    EXECUTE PROCEDURE clean_counties();


-- Create the plural_2016 table.
DROP TABLE IF EXISTS plural_2016;
CREATE TABLE plural_2016 (
    Counties    		TEXT,
    singleton      		INT,
    twins 				INT,
    other_multiples		INT,
    unknown_plural    	INT,
    total_plural        INT,
	Year				TEXT
);

CREATE TRIGGER clean_plural_2016
    BEFORE INSERT
    ON plural_2016
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the plural_2017 table.
DROP TABLE IF EXISTS plural_2017;
CREATE TABLE plural_2017 (
    Counties    		TEXT,
    singleton      		INT,
    twins 				INT,
    other_multiples		INT,
    unknown_plural    	INT,
    total_plural        INT,
	Year				TEXT
);

CREATE TRIGGER clean_plural_2017
    BEFORE INSERT
    ON plural_2017
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the plural_2018 table.
DROP TABLE IF EXISTS plural_2018;
CREATE TABLE plural_2018 (
    Counties    		TEXT,
    singleton      		INT,
    twins 				INT,
    other_multiples		INT,
    unknown_plural    	INT,
    total_plural        INT,
	Year				TEXT
);

CREATE TRIGGER clean_plural_2018
    BEFORE INSERT
    ON plural_2018
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the plural_2019 table.
DROP TABLE IF EXISTS plural_2019;
CREATE TABLE plural_2019 (
    Counties    		TEXT,
    singleton      		INT,
    twins 				INT,
    other_multiples		INT,
    unknown_plural    	INT,
    total_plural        INT,
	Year				TEXT
);

CREATE TRIGGER clean_plural_2019
    BEFORE INSERT
    ON plural_2019
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the plural_total table.
--DROP TABLE IF EXISTS plural_total;
--CREATE TABLE plural_total (
--    Counties            TEXT,
--    singleton           INT,
--    twins               INT,
--    other_multiples     INT,
--    unknown_plural      INT,
--    total_plural        INT,
--    Year                TEXT
--);

--CREATE TRIGGER clean_plural_total
--    BEFORE INSERT
--    ON plural_total
--    FOR EACH ROW
--    EXECUTE PROCEDURE clean_counties();

-- Create the race_2016 table.
DROP TABLE IF EXISTS race_2016;
CREATE TABLE race_2016 (
    Counties					   	TEXT,
    White_Non_Hispanic      		INT,
    African_American_Non_Hispanic	INT,
    Other_Non_Hispanic				INT,
    Hispanic    					INT,
	Total_Race						INT,
	Year							TEXT
);

CREATE TRIGGER clean_race_2016
    BEFORE INSERT
    ON race_2016
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the race_2017 table.
DROP TABLE IF EXISTS race_2017;
CREATE TABLE race_2017 (
    Counties					   	TEXT,
    White_Non_Hispanic      		INT,
    African_American_Non_Hispanic	INT,
    Other_Non_Hispanic				INT,
    Hispanic    					INT,
	Total_Race						INT,
	Year							TEXT
);

CREATE TRIGGER clean_race_2017
    BEFORE INSERT
    ON race_2017
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the race_2018 table.
DROP TABLE IF EXISTS race_2018;
CREATE TABLE race_2018 (
    Counties					   	TEXT,
    White_Non_Hispanic      		INT,
    African_American_Non_Hispanic	INT,
    Other_Non_Hispanic				INT,
    Hispanic    					INT,
	Total_Race						INT,
	Year							TEXT
);

CREATE TRIGGER clean_race_2018
    BEFORE INSERT
    ON race_2018
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the race_2019 table.
DROP TABLE IF EXISTS race_2019;
CREATE TABLE race_2019 (
    Counties					   	TEXT,
    White_Non_Hispanic      		INT,
    African_American_Non_Hispanic	INT,
    Other_Non_Hispanic				INT,
    Hispanic    					INT,
	Total_Race						INT,
	Year							TEXT
);

CREATE TRIGGER clean_race_2019
    BEFORE INSERT
    ON race_2019
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the race_total table.
--DROP TABLE IF EXISTS race_total;
--CREATE TABLE race_total (
--    Counties                        TEXT,
--    White_Non_Hispanic              INT,
--    African_American_Non_Hispanic   INT,
--    Other_Non_Hispanic              INT,
--    Hispanic                        INT,
--    Total_Race                      INT,
--    Year                            TEXT
--);

--CREATE TRIGGER clean_race_total
--    BEFORE INSERT
--    ON race_total
--    FOR EACH ROW
--    EXECUTE PROCEDURE clean_counties();

-- Create the weight_2016 table.
DROP TABLE IF EXISTS weight_2016;
CREATE TABLE weight_2016 (
    Counties		TEXT,
    gms_0_499     	INT,
    gms_500_1499	INT,
    gms_1500_2499	INT,
    gms_2500_8165   INT,
	Unknown_weight	INT,
	Total_weight	INT,
	Year			TEXT
);
CREATE TRIGGER clean_weight_2016
    BEFORE INSERT
    ON weight_2016
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the weight_2017 table.
DROP TABLE IF EXISTS weight_2017;
CREATE TABLE weight_2017 (
    Counties		TEXT,
    gms_0_499     	INT,
    gms_500_1499	INT,
    gms_1500_2499	INT,
    gms_2500_8165   INT,
	Unknown_weight	INT,
	Total_weight	INT,
	Year			TEXT
);

CREATE TRIGGER clean_weight_2017
    BEFORE INSERT
    ON weight_2017
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the weight_2018 table.
DROP TABLE IF EXISTS weight_2018;
CREATE TABLE weight_2018 (
    Counties		TEXT,
    gms_0_499     	INT,
    gms_500_1499	INT,
    gms_1500_2499	INT,
    gms_2500_8165   INT,
	Unknown_weight	INT,
	Total_weight	INT,
	Year			TEXT
);

CREATE TRIGGER clean_weight_2018
    BEFORE INSERT
    ON weight_2018
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the weight_2019 table.
DROP TABLE IF EXISTS weight_2019;
CREATE TABLE weight_2019 (
    Counties		TEXT,
    gms_0_499     	INT,
    gms_500_1499	INT,
    gms_1500_2499	INT,
    gms_2500_8165   INT,
	Unknown_weight	INT,
	Total_weight	INT,
	Year			TEXT
);

CREATE TRIGGER clean_weight_2019
    BEFORE INSERT
    ON weight_2019
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();

-- Create the census table.
DROP TABLE IF EXISTS census;
CREATE TABLE census (
    Counties                TEXT,
    Per_Capital_Income      INT,
    Median_Houshold_Income  INT,
    Population              INT
);

CREATE TRIGGER clean_census
    BEFORE INSERT
    ON census
    FOR EACH ROW
    EXECUTE PROCEDURE clean_counties();



    -- Create the weight_total table.
--DROP TABLE IF EXISTS weight_total;
--CREATE TABLE weight_total (
--    Counties        TEXT,
--    gms_0_499       INT,
--    gms_500_1499    INT,
--    gms_1500_2499   INT,
--    gms_2500_8165   INT,
--    Unknown_weight  INT,
--    Total_weight    INT,
--    Year            TEXT
--);
--CREATE TRIGGER clean_weight_total
--    BEFORE INSERT
--    ON weight_total
--    FOR EACH ROW
--    EXECUTE PROCEDURE clean_counties();




