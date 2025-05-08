SET search_path to summative,public;

INSERT INTO exam(excode, extitle, exlocation, exdate, extime) VALUES
('db01','just for testing1','here','2025-11-1','10:10'),
('db02','just for testing2','there','2025-11-1','11:11'),
('db03','just for testing3','where?','2025-11-5','15:15'),
('ma01','EXAMPLE TITLE','OLD LOcATION','2025-11-6','9:00'),
('ma02','DIFFERENT TITLE','NEW LOcATION','2025-11-7','9:00');
--('er01','boundary test1','0 0 0','2024-11-7','9:00'),  -- ERROR:  new row for relation "exam" violates check constraint "exam_exdate_check"
--('er02','boundary test2','0 0 0','2026-11-7','9:00');  -- ERROR:  new row for relation "exam" violates check constraint "exam_exdate_check"

INSERT INTO student(sno, sname, semail) VALUES
(1,'timmy','timmy@gmail'),
(2,'ahhhh','ahhhh@email'),
(3,'coolName','coolName@email'),
(4,'boringName','boringName@email'),
(5,'iCantThinkOfAName','iCantThinkOfAName@email'),
(6,'Name','Name@email'),
(7,'benedict','benedicty@gmail'),
(8,'jimmy','jimmy@email'),
(9,'walterWhite','walterWhite@email'),
(10,'RANDOMNAME','RANDOMNAME@email'),
(11,'billy mitchel','"best"gamer@gmail'),
(12,'todd togers','worstgamer@gmail');

INSERT INTO entry(eno, excode, sno) VALUES
(1,'db01',1),
(2,'db01',2),
(3,'db01',3),
(4,'db01',4),
(5,'db01',5),
(6,'db01',6),
(7,'db01',12);

INSERT INTO entry(eno, excode, sno) VALUES
(8,'db02',10),
(9,'db02',7),
(10,'db02',5),
(11,'db02',3),
(12,'db02',1),
(13,'db02',12);

INSERT INTO entry(eno, excode, sno) VALUES
(14,'ma01',10),
(15,'ma01',8),
(16,'ma01',6),
(17,'ma01',4),
(18,'ma01',2),
(19,'ma01',12);

INSERT INTO entry(eno, excode, sno) VALUES
(20,'ma02',1),
(21,'ma02',3),
(22,'ma02',5),
(23,'ma02',7),
(24,'ma02',9),
(25,'ma02',12);

INSERT INTO entry(eno, excode, sno) VALUES
(26,'er01',11),
(27,'er02',11);




-- -- testing for task F,  kinda H + I
SELECT give_egrade(1,'db01',30);
SELECT give_egrade(2,'db01',40);
SELECT give_egrade(3,'db01',50);
SELECT give_egrade(4,'db01',60);
SELECT give_egrade(5,'db01',70);
SELECT give_egrade(6,'db01',80);

SELECT give_egrade(10,'ma01',77);
SELECT give_egrade(8,'ma01',66);
SELECT give_egrade(6,'ma01',55);
SELECT give_egrade(4,'ma01',44);
SELECT give_egrade(2,'ma01',100);

SELECT give_egrade(1,'ma02',33);
SELECT give_egrade(3,'ma02',55);
SELECT give_egrade(5,'ma02',66);
SELECT give_egrade(7,'ma02',77);
SELECT give_egrade(9,'ma02',88);


SELECT student_withdraw(11);
INSERT INTO entry(eno, excode, sno) VALUES
(26,'er01',11);


--this is what the logs should look like;
-- NOTICE:  Wont add entry as another entry this student "5" is taking has an exam on the same day. for course "db02"
-- NOTICE:  Wont add entry as another entry this student "3" is taking has an exam on the same day. for course "db02"
-- NOTICE:  Wont add entry as another entry this student "1" is taking has an exam on the same day. for course "db02"
-- NOTICE:  Wont add entry as another entry this student "12" is taking has an exam on the same day. for course "db02"
-- NOTICE:  withdrawing entry in entry with sno "11"
-- NOTICE:  adding sno "11" to cancel table
-- NOTICE:  adding sno "11" to cancel table
-- NOTICE:  withdrew sno "11"
-- NOTICE:  Wont add student sno:"11", as they have already attempted then withdrew from that class this year
-- INSERT 0 0