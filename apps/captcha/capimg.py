#!/usr/bin/python3

#### Captcha Image Generator

#### Libraries
import sys
from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing

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
    capImage = CaptchaImage(capString)
    newFile = open(outFile, "wb")
    newFile.write(capImage)
    newFile.close()
  else:
    showHelp()

def showHelp():
  print(f"Usage: {sys.argv[0]} -s <YOURSTRING> -f <OUTPUTFILE>")

def CaptchaImage(capString):
  # Define a Blank PNG Image
  imgCanvas = Image(width=320, height=82, background=Color('WHITE'))
  imgCanvas.format = 'png'
  
  # Define a Drawing Object for Painting Colored Text
  drawTool = Drawing()
  drawTool.fill_color = Color("#1D0067");
  drawTool.font = 'Liberation-Serif'
  drawTool.font_size = 48
  drawTool.text(40, 60, capString)
  drawTool(imgCanvas);
  
  return imgCanvas.make_blob();

#### Run as Standalone App or Module
if __name__ == '__main__':
  # Standalone Mode
  main()
