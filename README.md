## UPenn Cybersecurity Bootcamp Project 4

### Overview:

**Topic**: Web Development - CAPTCHA Challenge Authentication

**Title**: Robot Until Proven Human: Implementing CAPTCHA

**End Goal**: Implement a server-side, visual and audio based, CAPTCHA system for web applications to deter bot activity.

**List of Technologies to reach the Goal:**
 - Linux VM
 - Docker/Podman
 - NGINX
 - Python
 - MariaDB
 - PHP
 - HTML and CSS
 - JavaScript
 - ImageMagick
 - espeak (espeak-ng)
 - ffmpeg (ffmpeg-free)
 - cURL
 - Web Browser
 - Git
 - Geany/VSCode/Codium/Vim IDE

**The goal will be reached in the following way:**
The Linux VM hosts a Container running the NGINX HTTP server to serve static HTML/CSS/JS content for the frontend of the app. PHP scripts using the cURL library proxy certain requests between the Python backend for handling CAPTCHAs. The backend generates visual and auditory CAPTCHA challenges for GET requests and validates user input for POST requests. ImageMagick and espeak are the libraries and utilities used to generate the challenges. Cookies are used to track a user's CAPTCHA session and the associated answer to the challenge (in RAM). MariaDB stores supplementary data for demonstrating a hypothetical survey web application that uses CAPTCHA verification. The cURL utility and Firefox are used for testing/debugging, while GitHub manages version control.

### Running the Proof of Concept

You will need: Linux system with Docker (Podman works too with some adjustments)
```
$ git clone "https://github.com/Brendaschec/Project-4-Bootcon-Captcha"
$ cd Project-4-Bootcon-Captcha/
$ sudo docker build . -t captchademo1
```
Wait a few minutes for the container image to build

Now you can start a temporary instance of the container
```
$ sudo docker run -it --rm -v $PWD/demo/site:/usr/share/nginx/html -p 4080:80 captchademo1
```
*Note that this command will remove the container when it is stopped. Adjust for persistence if you desire.*

Visit the link in a web browser to access the local web application:
```
http://localhost:4080/
```

You can stop the container by sending a Ctrl+C signal to the Docker terminal.
