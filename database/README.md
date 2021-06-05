~/trainingWorkspace/flask_ultimate_orelly/database:(13m|git@l-3-databse)
1147 ± sqlite3 data.db
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> create table users (id integer primary key autoincrement, name text, location text);
sqlite> .tables
users
sqlite> select * from users;
sqlite> insert into users (name, location) values ("FooBoy", "Devonshire");
sqlite> select * from users;
1|FooBoy|Devonshire
sqlite> insert into users (name, location) values ("GafGull", "Cornwarlshire");
sqlite> select * from users;
1|FooBoy|Devonshire
2|GafGull|Cornwarlshire
sqlite>.exit 

