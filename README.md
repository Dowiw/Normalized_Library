# UE_library
A query container for a normalized library database.

This library will be made from the ground up.
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
