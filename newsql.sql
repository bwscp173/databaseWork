SET search_path to summative,public;


DROP TABLE IF EXISTS exam;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS entry;
DROP TABLE IF EXISTS cancel;

CREATE TABLE exam (
   excode CHAR(4) NOT NULL PRIMARY KEY,
   extitle VARCHAR(200) NOT NULL UNIQUE,  -- rule 6
   exlocation VARCHAR(200) NOT NULL,
   exdate DATE NOT NULL CHECK(exdate > CURRENT_DATE  -- rule 1 must be for the coming year TODO maybe add 1 year to current date so the exam has to be for next year?
   				 AND exdate > "November 2025"),  -- rule 8 the first exam is after 2025
   extime TIME NOT NULL CHECK('18:00' < extime  AND extime > '09:00')  -- rule 9
);


CREATE TABLE student(
	sno integer NOT NULL PRIMARY KEY,
	sname VARCHAR(200) NOT NULL,
	semail VARCHAR(200) NOT NULL CHECK (semail) -- TODO write a function to validate emails
);

CREATE TABLE entry(
	eno integer NOT NULL UNIQUE PRIMARY KEY,
	excode CHAR(4) NOT NULL,
	sno integer NOT NULL,
	egrade DECIMAL(5,2) DEFAULT NULL  -- TODO write a function that when this student attents an exam they get given a number grade 0-100
		
);
CREATE TABLE cancel (
	eno integer NOT NULL PRIMARY KEY,
	excode CHAR(4) NOT NULL,
	sno integer NOT NULL,
	cdate TIMESTAMP NOT NULL,
	cuser VARCHAR(200) NOT NULL
);

-- just placeholder stuff right now
-- CREATE OR REPLACE FUNCTION log_cancelled()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     IF TG_OP = 'INSERT' THEN
--         INSERT INTO Order_Log (product_id, action, timestamp)
--         VALUES (NEW.product_id, 'INSERT', NOW());
--     ELSIF TG_OP = 'UPDATE' THEN
--         INSERT INTO Order_Log (product_id, action, timestamp)
--         VALUES (NEW.product_id, 'UPDATE', NOW());
--     ELSIF TG_OP = 'DELETE' THEN
--         INSERT INTO Order_Log (product_id, action, timestamp)
--         VALUES (OLD.product_id, 'DELETE', NOW());
--     END IF;
--     RETURN NULL;
-- END;
-- $$ LANGUAGE PLPGSQL;

-- CREATE OR REPLACE TRIGGER trigger_log_cancelled
-- AFTER INSERT OR UPDATE OR DELETE ON Products
-- FOR EACH ROW
-- EXECUTE FUNCTION log_cancelled();

