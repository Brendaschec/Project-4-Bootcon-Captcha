#!/usr/bin/python3

#### Captcha HTTP Server

#### Libraries
import sys
from capimg import CaptchaImage


#### Globals
# Somewhat Meaningless Version Info
appVer = "0.1"
appTitle = "Captcha Server"
# Modes
verboseMode = False
# Network Settings
hostName = "localhost"
portNum = 8080


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
  print("Placeholder")

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
