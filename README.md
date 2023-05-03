## UPenn Cybersecurity Bootcamp Project 4

#### Overview:

**Topic**: Web Development - CAPTCHA Challenge Authentication

**Title**: Robot Until Proven Human: Implementing CAPTCHA

**End Goal**: Implement a server-side, visual and audio based, CAPTCHA system for web applications to deter bot activity.

**List of Technologies to reach the Goal:**
 - Fedora/Ubuntu Linux VM
 - NGINX
 - Python
 - MariaDB
 - HTML and CSS
 - JavaScript
 - ImageMagick
 - espeak
 - cURL
 - Web Browser
 - Git/GitHub

**The goal will be reached in the following way:**
The Linux VM hosts the NGINX HTTP server to serve static HTML/CSS/JS content for the frontend of the app and the proxy forwards certain requests to a Python backend for handling CAPTCHAs. The backend generates visual and auditory CAPTCHA challenges for GET requests and validates user input for POST requests. ImageMagick and espeak are the libraries and utilities used to generate the challenges. Cookies are used to track a user's CAPTCHA session and the associated answer to the challenge (in RAM). MariaDB will store longer term session cookie information, post-challenge. cURL and Firefox are used for testing/debugging, while GitHub manages version control.


#### To Do:

