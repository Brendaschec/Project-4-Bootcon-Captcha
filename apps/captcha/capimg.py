#!/usr/bin/python3

#### Captcha Image Generator

#### Libraries
import sys

#### Globals
appver = "0.1"
apptitle = "Captcha Image Generator"

#### Start Here
def main():
  print(f"{apptitle} Version {appver}")
  # Did the user pass valid arguments?
  # Let's *try* to parse them!
  numArgs = len(sys.argv)
  if numArgs != 1 and (numArgs - 1) % 2 == 0:
    arg = 1
    capString = None
    outFile = None
    while arg < numArgs:
      # There is no match case until Python 3.10. Sorry!
      if sys.argv[arg] == "-s": # Get string for captcha
        arg = arg + 1
        capString = sys.argv[arg]
      elif sys.argv[arg] == "-f": # Get file name
        arg = arg + 1
        outFile = sys.argv[arg]
      elif sys.argv[arg] == "-t": # Test arg parser
        arg = arg + 1
        print("Test Pass!")
      arg = arg + 1
    print(f"You want to use the string: {capString}")
    print(f"You want to save to: {outFile}")
  else:
    showHelp()

def showHelp():
  print(f"Usage: {sys.argv[0]} -s <YOURSTRING> -f <OUTPUTFILE>")

def CaptchaImage(capString="ERROR"):
  print("NOT IMPLEMENTED")
  return finalimage

#### Run as Standalone App or Module
if __name__ == '__main__':
  # Standalone Mode
  main()
