#!/usr/bin/python3

#### Captcha Sound Generator
# Based heavily on capimg.py

#### Libraries
import os
import sys
import random
import subprocess

#### Globals
# Somewhat Meaningless Version Info
appVer = "0.1"
appTitle = "Captcha Sound Generator"
# Modes
verboseMode = False
# Random Character Choice Dataset (Notice there is no zero)
charChoices = "987654321ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"

#### Start Here
def main():
  print(f"{appTitle} Version {appVer}")
  # Defaults that really need to be overridden
  capString = None
  outFile = "temp.wav"
  fileFmt = 0
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
          elif sys.argv[i][1] == 'm': # Convert to mp3
            fileFmt = 1
          elif sys.argv[i][1] == 's': # Get string for captcha
            i = i + 1
            capString = sys.argv[i]
          elif sys.argv[i][1] == 'f': # Get file name
            i = i + 1
            outFile = sys.argv[i]
          elif sys.argv[i][1] == 't': # Test arg prints string
            i = i + 1
            print(sys.argv[i])
        i = i + 1
    except Exception as error:
      print(f"Error parsing arguments! Pass \'-h\' for help.\nExiting.")
      vprint(error)
  else:
    showHelp()
  if capString is not None:
    vprint(f"You want to use the string: {capString}")
    vprint(f"You want to save to: {outFile}")
    capSound = CaptchaSound(capString, fileFmt)
    newFile = open(outFile, "wb")
    newFile.write(capSound)
    newFile.close()
  else:
    print('File Error')

#### Help Page
def showHelp():
  print(f"Usage: {sys.argv[0]} [-m (Enable MP3)] -s <YOURSTRING> -f <OUTPUTFILE>")
  exit(0)

#### Verbose Mode Printing
def vprint(*args, **kwargs):
  if verboseMode == True:
    print("[VERBOSE] -- ", end = '')
    print(*args, **kwargs)

#### Generate a Sound Clip Reading Text
def CaptchaSound(capString, fileFmt):
  # Generate Random Temp File Name
  tempFileName = ''.join(random.choice(charChoices) for i in range(7))
  tempFile = '/tmp/'+tempFileName+'.wav'
  subprocess.run(["espeak-ng", "-w", tempFile, capString], check=True)
  if fileFmt == 1: # Convert to mp3 as needed for iOS compatibility
    subprocess.run(["ffmpeg", "-i", tempFile, '/tmp/'+tempFileName+'.mp3'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.remove(tempFile)
    tempFile = '/tmp/'+tempFileName+'.mp3'
  sndFile = open(tempFile, "rb")
  sndBin = sndFile.read()
  os.remove(tempFile)
  return sndBin

#### Run as Standalone App or Module
if __name__ == '__main__':
  # Standalone Mode
  main()

#### Resources and References
#https://www.digitalocean.com/community/tutorials/how-to-use-subprocess-to-run-external-programs-in-python-3
#https://www.w3schools.com/python/python_file_remove.asp
#https://stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess
