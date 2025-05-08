SET search_path to summative,public;

-- INSERT INTO student(sno, sname, semail) VALUES
-- (600,'Liza, F.','ffl@myhome.com');
-- ---- SELECT * FROM student;

-- -- INSERT INTO student(sno, sname, semail) VALUES
-- -- (100,'Perez, B.','pb@myhome.com');
-- ---- SELECT * FROM student;

-- INSERT INTO exam(excode, extitle, exlocation, exdate, extime) VALUES
-- ('VB01','Visual Basic 1','Norwich','02-11-2025','09:00');
-- ---- SELECT * FROM exam;

-- -- INSERT INTO exam(excode, extitle, exlocation, exdate, extime) VALUES
-- -- ('VB03','Visual Basic 3','London','03-11-2025','19:00');
-- -- -- SELECT * FROM exam;

-- -- due to the trigger function log_withdrawn_exam_extry
-- -- i just need to delete/withdraw the student
-- SELECT student_withdraw(200);
-- SELECT * FROM entry;
-- SELECT * FROM cancel;
-- SELECT delete_exam('VB01');
-- SELECT * FROM exam;

-- SELECT delete_exam('PYTH');
-- SELECT * FROM exam;

-- INSERT INTO entry(eno, excode, sno) VALUES
-- (10,'VB02',400);
-- SELECT * FROM entry;

-- -- INSERT INTO entry(eno, excode, sno) VALUES
-- -- (11,'VB02',100);
-- -- SELECT * FROM entry;

-- INSERT INTO entry(eno, excode, sno) VALUES
-- (12,'VB02',500);
-- SELECT * FROM entry;

---------- task F

-- SELECT give_egrade(200,'XQ02',60);
-- SELECT * FROM show_table_entry_with_excode('XQ02');


-- UPDATE entry SET egrade = 60 WHERE entry.eno = 99;
-- SELECT * FROM entry;

--UPDATE entry SET egrade = 110 WHERE entry.eno = 9;
--SELECT * FROM entry;

-- SELECT * FROM show_table_entry_with_excode('SQL1');
-- SELECT * FROM show_table_entry_with_excode('SQL"');
-- SELECT * FROM show_table_entry_with_excode('XQ02');
-- SELECT * FROM show_table_entry_with_excode('PMAN');
-- SELECT * FROM show_table_entry_with_excode('PYTH');
-- SELECT * FROM exam;
-- SELECT * FROM show_table_entry_with_excode('VB02');
--SELECT * FROM show_table_entry();
SELECT * FROM examination_timetable(100);