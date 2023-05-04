#!/usr/bin/python3

#### Captcha HTTP Server

#### Libraries
import sys
import time
import random
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
# Random Character Choice Dataset
charChoices = "987654321ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
# Session Record (Stores challenge answer, cookie info, timestamp, etc)
sessionRecord = {}

#### Handling HTTP Requests
# Define a custom class that uses BaseHTTPRequestHandler
class myServer(BaseHTTPRequestHandler):
# Overriding methods from the default ones in BaseHTTPRequestHandler.
  try:
    def do_GET(self):
      if self.path == '/new_image': # When to gen images
        challenge = newImage(self)
        self.wfile.write(challenge)
      elif self.path == '/new_sound': # When to gen sounds
        challenge = newSound(self)
        self.wfile.write(challenge)
      elif self.path == '/debug': # Test page
        genericResponse(self,"This is a test page.")
      else:
        self.send_error(404)
  except Exception as error:
    print("Internal Server Error! Check using verbose mode!")
    vprint(error)

#### Generate Image Challenge
def newImage(self):
  # Clear Old Items from Session Record
  clrOldSessions()
  # 24-Character Random Cookie
  randCookie = ''.join(random.choice(charChoices) for i in range(24))
  # Format Cookie String for Browser
  fmtCookie = 'captchaid='+randCookie
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
    vprint(f"SESSIONS                    ANSWERS    TIMESTAMP")
    for key, values in sessionRecord.items():
      vprint(f"{key}\t{values}")
  return CaptchaImage(randAnswer)

#### Generate Sound Challenge (piggyback off existing img answer)
def newSound(self):
  self.send_response(200)
  #self.send_header("Content-type", "audio/wav")
  self.send_header("Content-type", "text/html")
  self.end_headers()
  # We need to check the cookies to send same random string as audio
  return bytes("Not Implemented!", "utf-8")

#### Generic HTTP Response
def genericResponse(self,msg):
  self.send_response(200)
  self.send_header("Content-type", "text/html")
  self.end_headers()
  self.wfile.write(bytes(msg, "utf-8"))

#### Remove expired sessions from sessionRecord
def clrOldSessions():
  currentTime = int(time.time())
  oldSessions = []
  for key, value in sessionRecord.items():
    if currentTime - value[1] > 75:
      oldSessions.append(key)
  for key in oldSessions:
    del sessionRecord[key]

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
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print("Server stopped.")

def showHelp():
  print(f"Usage: {sys.argv[0]} [OPTIONS]")
  print(f"\t-h : Show Help")
  print(f"\t-v : Enable Verbose Mode")
  exit(0)

def vprint(*args, **kwargs):
  if verboseMode == True:
    print("[VERBOSE] -- ", end = '')
    print(*args, **kwargs)

#### Run as Standalone App or Module
if __name__ == '__main__':
  # Standalone Mode
  main()

#https://stackoverflow.com/questions/26286203/custom-print-function-that-wraps-print
#https://pynative.com/python-global-variables/
#https://www.freecodecamp.org/news/python-print-exception-how-to-try-except-print-an-error/
#https://pythonbasics.org/webserver/
#https://www.educative.io/answers/how-to-generate-a-random-string-in-python
# https://www.programiz.com/python-programming/dictionary
# https://www.w3schools.com/python/python_lists.asp
