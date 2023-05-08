FROM docker.io/almalinux/9-minimal

# Update Repo + Pkgs
RUN microdnf update -y

# Install CRB
RUN microdnf install -y 'dnf-command(config-manager)'
RUN dnf-3 config-manager --set-enabled crb

# Install EPEL Repo
RUN microdnf install -y epel-release

# Install core packages
RUN microdnf install -y python3 python3-pip ImageMagick-devel espeak-ng ffmpeg-free mariadb-server mariadb-devel nginx git rsync liberation-fonts
RUN pip install Wand

# Copy needed files
COPY container_scripts/init.sh /init
COPY container_scripts/setup.sh /setup

# Entrypoint
CMD /init
