#!/usr/bin/python3

#### Captcha HTTP Server

#### Libraries
import sys
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
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("This is a test page.", "utf-8"))
      else:
        self.send_error(404)
  except Exception as error:
    print("Internal Server Error! Check using verbose mode!")
    vprint(error)

#### Generate Image Challenge
def newImage(self):
  # We need to gen and store a random cookie and challenge answer
  self.send_response(200)
  self.send_header("Content-type", "image/png")
  self.end_headers()
  return CaptchaImage("Hello World")

#### Generate Sound Challenge (piggyback off existing img answer)
def newSound(self):
  self.send_response(200)
  #self.send_header("Content-type", "audio/wav")
  self.send_header("Content-type", "text/html")
  self.end_headers()
  # We need to check the cookies to send same random string as audio
  return bytes("Not Implemented!", "utf-8")

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
          elif sys.argv[i][1] == 'h': # Show Help Page
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
