#!/bin/bash
echo "APPLYING PRIVILAGES"
MYSQL_ROOT_PASSWORD="app_password"  # Assuming you used this password in docker run

mysql -u root -p$MYSQL_ROOT_PASSWORD
#mysql -h 127.0.0.1 --port 8888 -u root -ppassword -e 'CREATE DATABASE IF NOT EXISTS test;'
# Grant SELECT privilege on the specified table
GRANT ALL PRIVILEGES ON test.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
