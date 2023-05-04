#!/usr/bin/python3

#### Captcha HTTP Server

#### Libraries
import re
import sys
import time
import random
import threading
from capimg import CaptchaImage
from capsnd import CaptchaSound
from http.server import BaseHTTPRequestHandler, HTTPServer

#### Globals
# Somewhat Meaningless Version Info
appVer = "0.1"
appTitle = "Captcha Server"
# Modes
verboseMode = False
# Network Settings
hostName = "localhost"
portNum = 8080
# Random Character Choice Dataset (Notice there is no zero)
charChoices = "987654321ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
# Session Record (Stores challenge answer, cookie info, timestamp, etc)
sessionRecord = {}

#### Handling HTTP Requests
# Define a custom class that uses BaseHTTPRequestHandler
class myServer(BaseHTTPRequestHandler):
# Overriding methods from the default ones in BaseHTTPRequestHandler.
  try:
    def do_GET(self):
      if self.path == '/new_image': # gen images
        challenge = newImage(self)
        self.wfile.write(challenge)
      elif re.match(r'^/new_sound/(\d+)$', self.path): # gen sounds
        # Why the regex? - We need to match random digits in the URL
        # Why again?? - Firefox caches the sound file too agressively!
        # And...? - This workaround forces it to fetch a new URL.
        # Heres a new problem. Chrome users can spam the server by
        #   clicking the link many times. We need to alteast hide it!
        challenge = newSound(self)
        self.wfile.write(challenge)
      elif self.path == '/debug': # Test page
        genericHTTPResponse(self,"This is a test page.")
      else:
        self.send_error(404)
    def do_POST(self):
      if self.path == '/validate':
        response = valResponse(self)
        self.end_headers()
        self.wfile.write(bytes(response,"utf-8"))
  except Exception as error:
    print("Internal Server Error! Check using verbose mode!")
    vprint(error)

#### Generate Image Challenge
def newImage(self):
  # 24-Character Random Cookie
  randCookie = ''.join(random.choice(charChoices) for i in range(24))
  # Format Cookie String for Browser
  fmtCookie = 'captchaID='+randCookie
  self.send_response(200)
  # HTTP Headers
  self.send_header("Content-type", "image/png")
  self.send_header('Set-Cookie', fmtCookie)
  self.end_headers()
  # Generate Random 7-Character Challenge Answer
  randAnswer = ''.join(random.choice(charChoices) for i in range(7))
  # Maintain the record of the CaptchaID, Answer, and Timestamp
  currentTime = int(time.time())
  sessionRecord[randCookie] = [randAnswer,currentTime]
  # Show Session Table For Debugging
  if verboseMode == True:
    vprint(f"SESSIONS                     ANSWERS   TIMESTAMP")
    for key, values in sessionRecord.items():
      vprint(f"{key}\t{values}")
  return CaptchaImage(randAnswer)

#### Generate Sound Challenge (piggyback off existing img answer)
def newSound(self):
  self.send_response(200)
  self.send_header("Content-type", "audio/wav")
  self.end_headers()
  # We need to check the cookies to send same random string as audio
  if 'Cookie' in self.headers and 'captchaID=' in self.headers['Cookie']:
    # This is almost a copy of what was in valResponse
    captchaID = self.headers['Cookie'].partition('captchaID=')[2]
    if '; ' in self.headers['Cookie']:
      captchaID = captchaID.split('; ')[0]
    vprint(f"Client captchaID: {captchaID}")
    challengeAnswer = '...'.join(sessionRecord[captchaID][0])
    return CaptchaSound(challengeAnswer)
  else:
    return CaptchaSound("Improper Headers and/or Cookies!")
  

#### Validate Client Response
def valResponse(self):
  self.send_response(200)
  self.send_header("Content-type", "text/html")
  # Kinda make sure client is honest about content length header
  try:
    contentLength = int(self.headers['Content-Length'])
  except:
    contentLength = None
  if self.headers['Content-Length'] is not None \
  and 'Cookie' in self.headers \
  and 'captchaID=' in self.headers['Cookie']:
    # This is messy but we really just care about the captchaID cookie
    captchaID = self.headers['Cookie'].partition('captchaID=')[2]
    if '; ' in self.headers['Cookie']:
      captchaID = captchaID.split('; ')[0]
    vprint(f"Client cookies: {self.headers['Cookie']}")
    vprint(f"Client captchaID: {captchaID}")
    postBody = self.rfile.read(contentLength).decode() # Is this good?
    vprint(f"POSTed Message Body: {postBody}") # What if client lies???
    if 'captchaAnswer=' in postBody:
      # We only expect an answer and nothing else
      userAnswer = postBody.partition('captchaAnswer=')[2]
      vprint(f"Client userAnswer: {userAnswer}")
    else:
      return "Bad POST Body!\n"
    if captchaID in sessionRecord:
      if userAnswer == sessionRecord[captchaID][0]: # Is answer right?
        return "Correct!\n"
      else:
        return "Wrong!\n"
    else:
      return "Invalid Session!\n"
  else:
    return "Improper Headers and/or Cookies!\n"
  

#### Generic HTTP Response
def genericHTTPResponse(self,msg):
  self.send_response(200)
  self.send_header("Content-type", "text/html")
  self.end_headers()
  self.wfile.write(bytes(msg, "utf-8"))

#### Generic HTTP Error
def genericHTTPError(self,msg):
  self.send_response(403)
  self.send_header("Content-type", "text/html")
  self.end_headers()
  self.wfile.write(bytes(msg, "utf-8"))

#### Clear Expired Sessions from sessionRecord
def clrOldSessions():
  currentTime = int(time.time())
  oldSessions = []
  for key, value in sessionRecord.items():
    if currentTime - value[1] > 75:
      oldSessions.append(key)
  for key in oldSessions:
    del sessionRecord[key]

#### Periodically run clrOldSessions() with threading
def sessionHouseKeeping(interval):
  # Used copyprogramming.com for help with this
  # Create a timer object
  timer = threading.Timer(interval, sessionHouseKeeping, args=[interval])
  # Set the timer as a daemon thread we can exit without waiting for it
  timer.daemon = True
  timer.start()
  # Clear Old Items from Session Record
  clrOldSessions()

#### Start Here
def main():
  print(f"{appTitle} Version {appVer}")
  # Try to parse arguments
  numArgs = len(sys.argv)
  if numArgs != 1:
    try:
      i = 1
      while i < numArgs:
        if sys.argv[i][0] == '-':
          if sys.argv[i][1] == 'v': # Enable verbose mode
            global verboseMode
            verboseMode = True
          elif sys.argv[i][1] == 'h': # Show Help Page and Quit
            showHelp()
          elif sys.argv[i][1] == 't': # Test arg prints string
            i = i + 1
            vprint(sys.argv[i])
        i = i + 1
    except Exception as error:
      print(f"Error parsing arguments! Pass \'-h\' for help.\nExiting.")
      vprint(error)
  httpd = HTTPServer((hostName, portNum), myServer)
  print(f"Server started and listening on port {portNum}")
  sessionHouseKeeping(20) # Clean up old sessionRecords every 20 seconds
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print("Server stopped.")

#### Help Page
def showHelp():
  print(f"Usage: {sys.argv[0]} [OPTIONS]")
  print(f"\t-h : Show Help")
  print(f"\t-v : Enable Verbose Mode")
  exit(0)

#### Verbose Mode Printing
def vprint(*args, **kwargs):
  if verboseMode == True:
    print("[VERBOSE] -- ", end = '')
    print(*args, **kwargs)

#### Run as Standalone App or Module
if __name__ == '__main__':
  # Standalone Mode
  main()


#### Resources and References
#https://stackoverflow.com/questions/26286203/custom-print-function-that-wraps-print
#https://pynative.com/python-global-variables/
#https://www.freecodecamp.org/news/python-print-exception-how-to-try-except-print-an-error/
#https://pythonbasics.org/webserver/
#https://www.educative.io/answers/how-to-generate-a-random-string-in-python
#https://www.programiz.com/python-programming/dictionary
#https://www.w3schools.com/python/python_lists.asp
#https://copyprogramming.com/howto/how-to-run-a-function-every-30-seconds-in-python-best-methods-and-code-examples
#https://stackoverflow.com/questions/12572362/how-to-get-a-string-after-a-specific-substring
