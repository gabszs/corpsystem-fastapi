#!/bin/bash

MYSQL_ROOT_PASSWORD="app_password"  # Assuming you used this password in docker run

mysql -u root -p$MYSQL_ROOT_PASSWORD

# Grant SELECT privilege on the specified table
GRANT ALL PRIVILEGES ON test.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
