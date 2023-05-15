#### Base Image
FROM docker.io/almalinux/9-minimal


#### Update Repo + Packages
RUN microdnf update -y


#### Enable CRB
RUN microdnf install -y 'dnf-command(config-manager)'
RUN dnf-3 config-manager --set-enabled crb


#### Install EPEL Repo
RUN microdnf install -y epel-release


#### Install core packages
RUN microdnf install -y python3 python3-pip ImageMagick-devel espeak-ng ffmpeg-free mariadb mariadb-server mariadb-devel nginx php liberation-fonts procps-ng vim
RUN microdnf clean all
RUN pip install Wand


#### Copy/Create needed files/directories
COPY init.sh /init
COPY core /captcha


#### NGINX Arrangements
RUN rm -r /usr/share/nginx/html/*
COPY nxdefs.conf /etc/nginx/default.d/


#### PHP Arrangements
RUN mkdir -p /run/php-fpm


#### MariaDB Arrangements
RUN /usr/bin/mariadb-install-db --user=root --datadir=/var/lib/mysql


#### Expose Ports for Web App
EXPOSE 80 


#### Entrypoint
CMD /init
