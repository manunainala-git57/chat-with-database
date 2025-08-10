create database student ;

use student;

CREATE TABLE student (
    Id INT PRIMARY KEY,
    Name VARCHAR(30),
    Class VARCHAR(10),
    Section VARCHAR(10),
    Marks INT
);


INSERT INTO student values(1, 'Karthik', '10th', 'A', 96);
INSERT INTO student values(2, 'Sai', '10th', 'B', 87);
INSERT INTO student values(3, 'Raju', '10th', 'A', 91);
INSERT INTO student values(4, 'Venkatesh', '10th', 'A', 84);
INSERT INTO student values(5, 'Suresh', '10th', 'B', 79);


SELECT * FROM student;