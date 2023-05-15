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
RUN microdnf install -y python3 python3-pip ImageMagick-devel espeak-ng ffmpeg-free mariadb mariadb-server mariadb-devel nginx php php-mysqlnd liberation-fonts procps-ng vim
RUN microdnf clean all
RUN pip install Wand


#### Copy needed files and directories
COPY demo/rsrc/setup.sh /setup
COPY demo/rsrc/init.sh /init
COPY core /captcha


#### Execute setup script
RUN /setup


#### Expose Ports for Web App
EXPOSE 80 


#### Entrypoint
CMD /init
