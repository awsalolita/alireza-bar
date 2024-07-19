
* Connect to db
```
sqlplus 'admin@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracle.c7c2o0kgmpvz.us-east-1.rds.amazonaws.com)(PORT=1521))(CONNECT_DATA=(SID=oracle1)))'
```

* better visuals
```
set colsep '|'
set linesize 167
set pagesize 30
set pagesize 1000
```
* show databases
```
SELECT NAME FROM v$database;
```

* Show tables
```
SELECT table_name FROM user_tables; 
or
select object_name from user_objects where object_type='TABLE';
```
```
select * from table;
```
```
describe table;
```
```
CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);
```
* insert values
```
insert into persons (personid , lastname , firstname , address , city ) values ( '1' , 'pourchali' , 'ali' , 'janat' , 'tehran');
```

