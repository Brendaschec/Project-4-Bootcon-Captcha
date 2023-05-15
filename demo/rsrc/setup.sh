#!/bin/bash


#### Captcha Project
# Helper setup script for building demo container


#### NGINX Arrangements
# Clear Document Root
rm -r /usr/share/nginx/html/*

# Add custom configuration file
tee -a /etc/nginx/default.d/nxdefs.conf > /dev/null <<EOF
location /apps/direct {
  proxy_pass http://127.0.0.1:8080/;
}
EOF


#### PHP Arrangements
# Make room for php-fpm www.sock
mkdir -p /run/php-fpm


# MariaDB Arrangements (Insecure!)
# Install DB
/usr/bin/mariadb-install-db --user=root --datadir=/var/lib/mysql

# Add MariaDB Initial Config File
dbPassword="testpass100"
tee -a /etc/mariadb-init > /dev/null <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED BY '${dbPassword}';
EOF

# Start MariaDB daemon 
/usr/bin/mariadbd-safe --user=root --bind-address=127.0.0.1 --init-file=/etc/mariadb-init &

# Store the PID so we can stop it later
mdbPid=$!

# Wait a little for it to start properly (ugh!)
sleep 5

# Run some Management and SQL Queries
dbName="survey"
tableName="results"
/usr/bin/mariadb -uroot -p${dbPassword} <<EOF
GRANT ALL PRIVILEGES ON ${dbName}.* TO 'root'@'localhost' IDENTIFIED BY '${dbPassword}';
FLUSH PRIVILEGES;
CREATE DATABASE ${dbName};
USE ${dbName};
CREATE TABLE ${tableName} (color varchar(24), fruit varchar(24));
EOF

# Stop MariaDB daemon
kill $mdbPid
