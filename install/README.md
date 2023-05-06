## Installation Steps

### Step 1:
Install the required packages:

**Fedora/RHEL9 Distros with EPEL:**

`yum install ImageMagick ImageMagick-devel espeak-ng python3-pip mariadb mariadb-server mariadb-devel nginx ffmpeg-free`

**Debian/Ubuntu Distros:**

`apt install <FIXME>`

### Step 2:
**Configure SELinux to allow NGINX reverse proxy connection.**

*If you don't use SELinux or are running in a container, skip this.*

`sudo setsebool -P httpd_can_network_connect 1`

### Step 3:
**UNFINISHED. UNDER CONSTRUCTION!**

### Step 4:
