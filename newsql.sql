SET search_path to summative,public;


DROP TABLE IF EXISTS exam;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS entry;
DROP TABLE IF EXISTS cancel;
DROP FUNCTION IF EXISTS student_withdraw(integer);
DROP FUNCTION IF EXISTS show_table_entry(CHAR(4));
DROP FUNCTION IF EXISTS show_table_entry();
DROP FUNCTION IF EXISTS examination_timetable(INTEGER);

CREATE TABLE exam (
   excode CHAR(4) NOT NULL PRIMARY KEY,
   extitle VARCHAR(200) NOT NULL UNIQUE,  -- rule 6
   exlocation VARCHAR(200) NOT NULL,
   exdate DATE NOT NULL CHECK(exdate > CURRENT_DATE  -- rule 1 must be for the coming year TODO maybe add 1 year to current date so the exam has to be for next year?
   				 AND exdate > '2025-11-1'),  -- rule 8 the first exam is after 2025
   extime TIME NOT NULL CHECK('18:00' >= extime  AND extime >= '09:00')  -- rule 9
);


CREATE TABLE student(
	sno serial NOT NULL PRIMARY KEY,
	sname VARCHAR(200) NOT NULL,
	semail VARCHAR(200) NOT NULL --CHECK (semail) -- TODO write a function to validate emails
);

CREATE TABLE entry( -- serial 
	eno serial NOT NULL PRIMARY KEY,
	excode CHAR(4) NOT NULL,
	sno integer NOT NULL,
	egrade DECIMAL(5,2) DEFAULT NULL,  -- TODO write a function that when this student attents an exam they get given a number grade 0-100
	CONSTRAINT entry_CK1 UNIQUE (eno),
    CONSTRAINT entry_CK2 UNIQUE (excode, sno)
);
CREATE TABLE IF NOT EXISTS cancel (
	eno integer NOT NULL,
	excode CHAR(4) NOT NULL,
	sno integer NOT NULL,
	cdate TIMESTAMP NOT NULL,
	cuser VARCHAR(200) NOT NULL,
	PRIMARY KEY (eno,sno) -- as multiple students from a with the same eno can cancel
	--CONSTRAINT cancel UNIQUE (eno),
);

-- --just placeholder stuff right now
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


CREATE OR REPLACE FUNCTION log_withdrawn_exam_extry()
RETURNS TRIGGER AS $$

BEGIN
    IF TG_OP = 'DELETE' THEN
		BEGIN
	        INSERT INTO cancel (eno, excode, sno, cdate, cuser)
    	    VALUES (OLD.eno, old.excode,old.sno, NOW(),'admin');  -- possible change out admin for differnt
		EXCEPTION
			WHEN unique_violation THEN
				RAISE NOTICE 'log_withdrawn_exam_extry, is throwing an error possibly pk already in db';
		END;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE PLPGSQL;

CREATE OR REPLACE TRIGGER log_withdrawn_exam_extry
AFTER DELETE ON entry
FOR EACH ROW
EXECUTE FUNCTION log_withdrawn_exam_extry();

INSERT INTO exam (excode,extitle,exlocation,exdate,extime) VALUES
('db01','just for testing1','here','2033-11-1','10:10'),
('db02','just for testing2','there','2034-10-1','11:11'),
('db03','just for testing3','where?','2035-10-5','15:15'),
('ma01','EXAMPLE TITLE','OLD LOcATION','2026-11-6','9:00'),
('ma02','DIFFERENT TITLE','NEW LOcATION','2026-11-7','9:00');

INSERT INTO student (sname,semail) VALUES
('timmy','timmy@gmail'),
('ahhhh','ahhhh@email'),
('coolName','coolName@email'),
('boringName','boringName@email'),
('iCantThinkOfAName','iCantThinkOfAName@email'),
('Name','Name@email'),
('benedict','benedicty@gmail'),
('jimmy','jimmy@email'),
('walterWhite','walterWhite@email'),
('RANDOMNAME','RANDOMNAME@email');

INSERT INTO entry(excode,sno) VALUES
('db01',1),
('db01',2),
('db01',3),
('db01',4),
('db01',5),
('db01',6),
('db01',12);

INSERT INTO entry(excode,sno) VALUES
('db02',10),
('db02',7),
('db02',5),
('db02',3),
('db02',1),
('db02',12);

INSERT INTO entry(excode,sno) VALUES
('ma01',10),
('ma01',8),
('ma01',6),
('ma01',4),
('ma01',2),
('ma01',12);

INSERT INTO entry(excode,sno) VALUES
('ma02',1),
('ma02',3),
('ma02',5),
('ma02',7),
('ma02',9),
('ma02',12);

-- -- for testing delete_exam
-- INSERT INTO entry (excode,sno) VALUES
-- ('db03',6);


CREATE OR REPLACE FUNCTION delete_exam(exam_to_cancel CHAR(4))
-- for task D
-- exams can only be deleted if there are no entries
RETURNS VOID AS $$
BEGIN
	IF NOT EXISTS (SELECT 1 FROM entry WHERE excode = exam_to_cancel) THEN
		 RAISE NOTICE 'no entrys found for exam: "%", will now delete',exam_to_cancel;
		 DELETE FROM exam WHERE excode = exam_to_cancel;
		 RAISE NOTICE 'deleted exam "%"', exam_to_cancel;
	ELSE
		RAISE NOTICE 'cannot delete exam "%", as there are still entrys', exam_to_cancel;
	END IF;
END;
$$ LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION student_withdraw(target_sno INTEGER, target_excode CHAR(4))
-- deletes all entrys in the table entry with the matching sno
RETURNS VOID AS $$
BEGIN
	-- checking if there is a student to deleted and will raise a correct notice
	IF EXISTS (SELECT 1 FROM entry WHERE excode = target_excode and sno = target_sno ) THEN
		RAISE NOTICE 'withdrawing entry in entry with sno "%" and excode "%"', target_sno,target_excode;
		DELETE FROM entry WHERE sno = target_sno AND excode = target_excode;	
		RAISE NOTICE 'withdrew sno "%" and excode "%"',target_sno,target_excode;
	ELSE
		RAISE NOTICE 'cannot withdraw student as with sno "%" and excode "%", as it does not exist', target_sno,target_excode;
	END IF;
END;
$$ LANGUAGE PLPGSQL;


-- TODO Figure out what the hell this function was ment todo
-- CREATE OR REPLACE FUNCTION insert_examination_entry(eno INTEGER, excode , sno)
-- -- deletes all entrys in the table entry with the matching sno
-- RETURNS VOID AS $$
-- BEGIN
-- 	DELETE FROM entry WHERE sno = target_sno;
-- END;
-- $$ LANGUAGE PLPGSQL;

-- FOR TASK F
CREATE OR REPLACE FUNCTION give_egrade(target_sno INTEGER, target_excode CHAR(4), mark INTEGER)
RETURNS VOID AS $$
BEGIN
	UPDATE entry SET egrade = mark WHERE sno = target_sno AND excode = target_excode;
END;
$$ LANGUAGE PLPGSQL;








-- -- FOR TASK G
-- CREATE OR REPLACE FUNCTION examination_timetable(given_sno INTEGER)
-- RETURNS TABLE (
-- 				student_name VARCHAR(200),
-- 				exam_location VARCHAR(200), 
-- 				exam_code CHAR(4),
-- 				exam_title VARCHAR(200),
-- 				exam_day DATE,
-- 				exam_time TIME) AS $$
-- BEGIN

-- 	RETURN QUERY SELECT distinct on (exam.excode) student.sname, exam.exlocation, exam.excode, exam.extitle, exam.exdate, exam.extime FROM student,entry,exam WHERE student.sno = given_sno and entry.excode = exam.excode;


-- --SELECT student.sname, exam. FROM student,exam WHERE student.sno = 5;

-- END;
-- $$ LANGUAGE PLPGSQL;


-- SELECT student.sname, exam.exlocation, exam.excode, exam.extitle, exam.exdate, exam.extime
-- 	FROM student, exam;

-- SELECT * FROM examination_timetable(12);

-- SELECT * FROM exam;
-- SELECT * FROM student;
-- SELECT student.sname, exam.exlocation, exam.excode, exam.extitle, exam.exdate, exam.extime FROM student,entry,exam WHERE student.sno = 2 and entry.excode = exam.excode;
--SELECT student.sname, exam.exlocation, exam.excode, exam.extitle, exam.exdate, exam.extime FROM student,entry,exam WHERE student.sno = 1 and entry.excode = exam.excode;
-- SELECT * FROM exam WHERE excode = (SELECT entry.excode FROM student,entry where student.sno = entry.sno);
--SELECT * FROM entry;


-- SELECT student.sname, exam.exlocation, exam.excode, exam.extitle, exam.exdate, exam.extime FROM student,entry,exam WHERE student.sno = 1 AND student.sno = entry.sno AND entry.excode = exam.excode; 


-- FOR TASK H
-- CREATE OR REPLACE FUNCTION show_table_entry()
-- RETURNS TABLE (
-- 				examination_code CHAR(4),
-- 				student_name VARCHAR(200), 
-- 				egrade_value DECIMAL(5,2),
-- 				egrade_text TEXT) AS $$
-- BEGIN
-- 	RETURN QUERY SELECT entry.excode, student.sname,entry.egrade,
-- 	CASE
-- 		WHEN entry.egrade >= 70 THEN 'Distinction'
-- 		WHEN entry.egrade < 70 and entry.egrade >= 50 THEN 'Pass' 
-- 		WHEN entry.egrade < 50 THEN 'Fail'
-- 		else 'Not taken'
-- 	END AS egrade
-- 	from entry,student WHERE student.sno = entry.sno ORDER BY examination_code,student_name;
-- END;
-- $$ LANGUAGE PLPGSQL;

-- -- FOR TASK I
-- CREATE OR REPLACE FUNCTION show_table_entry_with_excode(target_excode CHAR(4))
-- RETURNS TABLE (
-- 				examination_code CHAR(4),
-- 				student_name VARCHAR(200), 
-- 				egrade_value DECIMAL(5,2),
-- 				egrade_text TEXT) AS $$
-- BEGIN
-- 	RETURN QUERY SELECT entry.excode, student.sname,entry.egrade,
-- 	CASE
-- 		WHEN entry.egrade >= 70 THEN 'Distinction'
-- 		WHEN entry.egrade < 70 and entry.egrade >= 50 THEN 'Pass' 
-- 		WHEN entry.egrade < 50 THEN 'Fail'
-- 		else 'Not taken'
-- 	END AS egrade
-- 	from entry,student WHERE student.sno = entry.sno AND entry.excode = target_excode ORDER BY examination_code,student_name;
-- END;
-- $$ LANGUAGE PLPGSQL;

-- -- testing for task C
--SELECT student_withdraw(1,'db01');
--SELECT student_withdraw(4,'db01');


-- SELECT * FROM examination_timtable(5);

-- -- testing for task F,  kinda H + I
-- SELECT give_egrade(1,'db01',30);
-- SELECT give_egrade(2,'db01',40);
-- SELECT give_egrade(3,'db01',50);
-- SELECT give_egrade(4,'db01',60);
-- SELECT give_egrade(5,'db01',70);
-- SELECT give_egrade(6,'db01',80);

-- SELECT give_egrade(10,'ma01',77);
-- SELECT give_egrade(8,'ma01',66);
-- SELECT give_egrade(6,'ma01',55);
-- SELECT give_egrade(4,'ma01',44);
-- SELECT give_egrade(2,'ma01',100);

-- SELECT give_egrade(1,'ma02',33);
-- SELECT give_egrade(3,'ma02',55);
-- SELECT give_egrade(5,'ma02',66);
-- SELECT give_egrade(7,'ma02',77);
-- SELECT give_egrade(9,'ma02',88);

-- -- testing for task H and I
-- -- SELECT * FROM show_table_entry();
-- SELECT * FROM show_table_entry_with_excode('db01');
-- SELECT * FROM show_table_entry_with_excode('db02');
-- SELECT * FROM show_table_entry_with_excode('ma01');
-- SELECT * FROM show_table_entry_with_excode('ma02');

SELECT * FROM student;