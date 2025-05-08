SET search_path to summative,public;

DELETE FROM entry;

DELETE FROM student;

DELETE FROM exam;

DELETE FROM cancel;

INSERT INTO exam VALUES 
    ('VB02', 'Visual Basic 2', 'London', '2025-11-02', '18:00'),
    ('SQL1', 'SQL 1', 'Norwich', '2025-11-01', '11:00'),
    ('SQL2', 'SQL 2', 'Norwich', '2025-11-02', '11:00'),
    ('XQ02', 'Xquery 2', 'Norwich', '2025-11-03', '11:00'),
    ('PMAN', 'Project Management', 'London', '2025-11-04', '11:00'),
    ('PYTH', 'Python programming', 'London', '2025-11-04', '11:00');


INSERT INTO student VALUES
    (100, 'Lewing, Y.', 'ly@myhome.com'),
    (200, 'Brown, B.', 'bb@myhome.com'),
    (300, 'Green, C.', 'cg@myhome.com'),
    (400, 'White, D.', 'dw@myhome.com'),
    (500, 'Young, E.', 'ey@myhome.com');

INSERT INTO entry(eno, excode, sno)
    VALUES (1, 'VB02', 100);   
INSERT INTO entry(eno, excode, sno)
    VALUES (2, 'XQ02', 100);
INSERT INTO entry(eno, excode, sno)
    VALUES (3, 'PMAN', 100);
INSERT INTO entry(eno, excode, sno)
    VALUES (4, 'SQL1', 200);
INSERT INTO entry(eno, excode, sno)
    VALUES (5, 'VB02', 200);
INSERT INTO entry(eno, excode, sno)
    VALUES (6, 'XQ02', 200);
INSERT INTO entry(eno, excode, sno)
    VALUES (7, 'PMAN', 200);
INSERT INTO entry(eno, excode, sno)
    VALUES (8, 'PYTH', 300);
INSERT INTO entry(eno, excode, sno)
    VALUES (9, 'SQL2', 500);	

SELECT 'Students', count(*) FROM student
UNION 
SELECT 'Exams', count(*) FROM exam
UNION 
SELECT 'Entries', count(*)FROM entry
UNION 
SELECT 'Cancelled', count(*)FROM cancel;

-- This should show you 9 entries, 6 exams, 5 students and 0 cancelled.


UPDATE entry SET

    egrade = 50

    WHERE eno = 1;

UPDATE entry SET

    egrade = 55

    WHERE eno = 2;

UPDATE entry SET

    egrade = 45

    WHERE eno = 3;

UPDATE entry SET

    egrade = 50

    WHERE eno = 4;

UPDATE entry SET

    egrade = 90

    WHERE eno = 5;

UPDATE entry SET

    egrade = 20

    WHERE eno = 6;



SELECT * FROM entry order by eno;

-- This should show entries 1-6 with egrades and entries 7 TO 9 with null values.