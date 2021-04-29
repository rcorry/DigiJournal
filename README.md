# Digi-Journal

## Resource

**Log**

Attributes:

* heading (string)
* rating (integer)
* entry (string)
* date (string)
* place (string)

**Users**

Attributes:

* f_name (string)
* l_name (string)
* email (string)
* password (string)

## Schema

```sql
CREATE TABLE logs(
id INTEGER PRIMARY KEY,
heading TEXT,
date TEXT,
entry TEXT,
rating INTEGER,
place TEXT);
CREATE TABLE users(
id INTEGER PRIMARY KEY,
f_name TEXT,
l_name TEXT,
email TEXT,
password TEXT);
```

## REST Endpoints

Name                    | Method | Path
------------------------|--------|------------------
Retrieve log collection | GET    | /logs
Retrieve log member     | GET    | /logs/*\<id\>*
Create session member   | POST   | /sessions
Create log member       | POST   | /logs
Create user member      | POST   | /users
Update log member       | PUT    | /logs/*\<id\>*
Delete log member       | DELETE | /logs/*\<id\>*


## Password Hashing Method
* bcrypt