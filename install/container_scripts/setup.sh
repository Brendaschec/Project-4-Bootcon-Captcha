#!/bin/bash

#### Captcha Project
# Container Setup/Reset Script

# Update gitrepo if it exists
test -d "/gitrepo/.git" && cd /gitrepo && git pull

# Pull the latest testing branch if gitrepo does not exist
test -d "/gitrepo/.git" || git clone --branch testing https://github.com/Brendaschec/captcha.git /gitrepo

# Sync the web content
rsync -vr /gitrepo/demo/* /usr/share/nginx/html/

# Sync nginx config
rsync -vr /gitrepo/conf/nginx/* /etc/nginx/default.d/

