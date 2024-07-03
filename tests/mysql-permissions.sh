#!/bin/bash
# docker exec -it corpsystem_test /bin/bash
MYSQL_ROOT_PASSWORD="app_password"  # Assuming you used this password in docker run

mysql -u root -p$MYSQL_ROOT_PASSWORD

# Grant SELECT privilege on the specified table
GRANT ALL PRIVILEGES ON test.* TO 'app_user'@'%';
echo "PRIVELEGES GRANTED"

# Flush privileges for immediate effect
FLUSH PRIVILEGES;
echo "PRIVELEGES FLUSHED"

echo "Granted SELECT privilege to user '$TARGET_USER' on table '$TABLE_NAME' in database '$DATABASE_NAME'"


# # Grant SELECT privilege on the specified table
# GRANT ALL PRIVILEGES ON test.* TO 'app_user'@'%';
# FLUSH PRIVILEGES;
# EOF

