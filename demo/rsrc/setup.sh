#!/bin/bash


#### Captcha Project
# Helper setup script for building demo container


#### Bash Settings
# Exit if any error
set -e


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
dbName="captchaDemo"
/usr/bin/mariadb -uroot -p${dbPassword} <<EOF
GRANT ALL PRIVILEGES ON ${dbName}.* TO 'root'@'localhost' IDENTIFIED BY '${dbPassword}';
FLUSH PRIVILEGES;

CREATE DATABASE ${dbName};
USE ${dbName};
CREATE TABLE surveyResults (
favoriteColor varchar(64),
favoriteSport varchar(64),
favoriteFruit varchar(64),
timeStamp datetime
);

CREATE TABLE accountDetails (
username varchar(64) NOT NULL,
passAlgo varchar(8),
passSalt varchar(48),
passHash varchar(255),
acctInfo text(1200),
timeStamp datetime
);
ALTER TABLE accountDetails ADD UNIQUE (username);

CREATE TABLE contactUs (
firstName varchar(255),
lastName varchar(255),
emailAddress varchar(255),
message text(1200),
timeStamp datetime
);

CREATE TABLE testTable (
field1 varchar(255),
field2 varchar(255),
field3 varchar(255),
field4 varchar(255),
timeStamp datetime
);
EOF

# Stop MariaDB daemon
kill $mdbPid
