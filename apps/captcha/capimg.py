#!/usr/bin/python3

#### Captcha Image Generator

#### Libraries
import sys
import random
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

#### Generate an Image with Distorted Text
def CaptchaImage(capString):
  # Define a Blank PNG Image
  imgWidth = 320
  imgHeight = 82
  imgCanvas = Image(width=imgWidth, height=imgHeight, background=Color('WHITE'))
  imgCanvas.format = 'png'
  
  # Define a Drawing Object for Painting Colored Text
  drawTool = Drawing()
  drawTool.fill_color = Color(random.choice(['RED','ORANGE','GREEN','BLUE','BLACK']));
  drawTool.font = 'Liberation-Serif'
  drawTool.font_size = 48
  
  # Paint the Text
  drawTool.text(40, 60, capString)
  drawTool(imgCanvas);
  
  # Distort the Image with Transformation
  rndSwirl1 = random.randint(26, 37)
  imgCanvas.swirl(degree=rndSwirl1)
  
  # Define a Drawing Object for Painting Lines
  drawTool = Drawing()
  
  # Draw Some Random Lines on the Image
  lines = 10
  while lines > 0:
    drawTool.fill_color = Color(random.choice(['RED','MAGENTA','ORANGE','GREEN','BLUE','BROWN']));
    drawTool.line((random.randint(2, imgWidth - 100),random.randint(2, imgHeight - 60)), (random.randint(100, imgWidth - 10),random.randint(40, imgHeight - 10)))
    lines = lines - 1
  drawTool(imgCanvas);
  
  return imgCanvas.make_blob();

#### Run as Standalone App or Module
if __name__ == '__main__':
  # Standalone Mode
  main()


#### Resources and References
# https://docs.python.org/3/library/random.html
# https://www.geeksforgeeks.org/python-write-bytes-to-file/
# https://www.digitalocean.com/community/tutorials/python-command-line-arguments
