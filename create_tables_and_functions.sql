SET search_path to summative,public;

DROP TABLE IF EXISTS exam;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS entry;
-- DROP TABLE IF EXISTS cancel;
DROP FUNCTION IF EXISTS student_withdraw(integer);
DROP FUNCTION IF EXISTS show_table_entry_with_excode(CHAR(4));
DROP FUNCTION IF EXISTS show_table_entry();
DROP FUNCTION IF EXISTS examination_timetable(INTEGER);
DROP FUNCTION IF EXISTS check_student_entry();

CREATE TABLE exam (
   excode CHAR(4) NOT NULL PRIMARY KEY,
   extitle VARCHAR(200) NOT NULL UNIQUE,  -- rule 6
   exlocation VARCHAR(200) NOT NULL,
   exdate DATE NOT NULL CHECK(exdate > CURRENT_DATE  -- rule 1 must be for the coming year TODO maybe add 1 year to current date so the exam has to be for next year?
   				 AND exdate >= '2025-11-1' AND exdate < '2025-12-1'),  -- rule 8 the first exam is after 2025 in november
   extime TIME NOT NULL CHECK('18:00' >= extime  AND extime >= '09:00')  -- rule 9
);

CREATE TABLE student(
	sno INTEGER NOT NULL PRIMARY KEY,
	sname VARCHAR(200) NOT NULL,
	semail VARCHAR(200) NOT NULL --CHECK (semail) -- TODO write a function to validate emails
);

CREATE TABLE entry(
	eno INTEGER NOT NULL PRIMARY KEY,
	excode CHAR(4) NOT NULL,
	sno INTEGER NOT NULL,
	egrade DECIMAL(5,2) DEFAULT NULL CHECK(egrade >= 0 AND egrade <= 100),  -- DONE write a function that when this student attents an exam they get given a number grade 0-100
	CONSTRAINT entry_CK1 UNIQUE (eno),
    CONSTRAINT entry_CK2 UNIQUE (excode, sno)
);

CREATE TABLE IF NOT EXISTS cancel (
	eno integer NOT NULL,
	excode CHAR(4) NOT NULL,
	sno integer NOT NULL,
	cdate TIMESTAMP NOT NULL,
	cuser VARCHAR(200) NOT NULL,
	PRIMARY KEY (eno,cdate) -- as multiple students from a with the same eno can cancel
	--CONSTRAINT cancel UNIQUE (eno),
);



CREATE OR REPLACE FUNCTION log_withdrawn_exam_extry()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
		BEGIN
	        INSERT INTO cancel (eno, excode, sno, cdate, cuser)
    	    VALUES (OLD.eno, old.excode,old.sno, NOW(),'admin');  -- possibly change out admin for  something different
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
		RAISE NOTICE 'cannot delete exam: "%", as there are still entrys', exam_to_cancel;
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



-- FOR TASK F
CREATE OR REPLACE FUNCTION give_egrade(target_sno INTEGER, target_excode CHAR(4), mark INTEGER)
RETURNS VOID AS $$
BEGIN
	UPDATE entry SET egrade = mark WHERE sno = target_sno AND excode = target_excode;
END;
$$ LANGUAGE PLPGSQL;



-- -- FOR TASK G
CREATE OR REPLACE FUNCTION examination_timetable(given_sno INTEGER)
RETURNS TABLE (
				student_name VARCHAR(200),
				exam_location VARCHAR(200), 
				exam_code CHAR(4),
				exam_title VARCHAR(200),
				exam_day DATE,
				exam_time TIME) AS $$
BEGIN
	RETURN QUERY SELECT distinct on (exam.excode) student.sname, exam.exlocation, exam.excode, exam.extitle, exam.exdate, exam.extime FROM student,entry,exam WHERE student.sno = given_sno and entry.excode = exam.excode;
END;
$$ LANGUAGE PLPGSQL;



-- FOR TASK H
CREATE OR REPLACE FUNCTION show_table_entry()
RETURNS TABLE (
				examination_code CHAR(4),
				student_name VARCHAR(200), 
				egrade_value DECIMAL(5,2),
				egrade_text TEXT) AS $$
BEGIN
	RETURN QUERY SELECT entry.excode, student.sname,entry.egrade,
	CASE
		WHEN entry.egrade >= 70 THEN 'Distinction'
		WHEN entry.egrade < 70 and entry.egrade >= 50 THEN 'Pass' 
		WHEN entry.egrade < 50 THEN 'Fail'
		else 'Not taken'
	END AS egrade
	from entry,student WHERE student.sno = entry.sno ORDER BY examination_code,student_name;
END;
$$ LANGUAGE PLPGSQL;



-- -- FOR TASK I
CREATE OR REPLACE FUNCTION show_table_entry_with_excode(target_excode CHAR(4))
RETURNS TABLE (
				examination_code CHAR(4),
				student_name VARCHAR(200), 
				egrade_value DECIMAL(5,2),
				egrade_text TEXT) AS $$
BEGIN
	RETURN QUERY SELECT entry.excode, student.sname,entry.egrade,
	CASE
		WHEN entry.egrade >= 70 THEN 'Distinction'
		WHEN entry.egrade < 70 and entry.egrade >= 50 THEN 'Pass' 
		WHEN entry.egrade < 50 THEN 'Fail'
		else 'Not taken'
	END AS egrade
	from entry,student WHERE student.sno = entry.sno AND entry.excode = target_excode ORDER BY examination_code,student_name;
END;
$$ LANGUAGE PLPGSQL;



CREATE OR REPLACE FUNCTION check_student_entry()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN  -- this line isnt directly needed but its for clarity
		-- the "date_part('year', cdate) = date_part('year', CURRENT_DATE);" part checks for if the date in the db is in the current year
		IF EXISTS (SELECT 1 FROM cancel WHERE new.excode = excode AND new.sno = sno AND date_part('year', cdate) = date_part('year', CURRENT_DATE)) THEN
			RAISE NOTICE 'Wont add student sno:"%", as they have already attempted then withdrew from that class this year',new.sno;
			RETURN NULL;
		ELSE
			RETURN NEW;
		-- SELECT 1 FROM cancel WHERE OLD.eno = eno , old.excode = excode, old.sno = sno
  --       INSERT INTO cancel (eno, excode, sno, cdate, cuser)
--  	    VALUES (OLD.eno, old.excode,old.sno, NOW(),'admin');  -- possible change out admin for differnt
		END IF;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE PLPGSQL;

CREATE OR REPLACE TRIGGER check_student_entry
BEFORE INSERT ON entry
FOR EACH ROW
EXECUTE FUNCTION check_student_entry();