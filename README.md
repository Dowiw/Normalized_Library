# UE_library
A query container for a normalized library database.
- Take a look at 1_final_db.png for a 3NF format of the database.

This project will:
- Build its own library database using the python file builder.
- Have a query python file to house relevant python queries.

# Requirements
- This runs on python3.
- Ensure that you have a database already created with your psql user.
- Ensure that this database is named properly as the initial_database_name.

# Notes
Remember, you must first log in to your postgres user.

Like:
```
sudo -i -u postgres
```

To check if pgAdmin is installed properly use:
```
dpkg -l | grep pgadmin4
```

In case you forget your postgres password:
```
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'enter_password';
\q
```

To install VS Code:
```
sudo snap install code --classic
```

To execute a certain part of the python script in VSCode, use shift + enter.