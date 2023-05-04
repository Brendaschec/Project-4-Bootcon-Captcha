#!/usr/bin/python3

#### Captcha Image Generator

#### Libraries
import sys
import random
from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing

#### Globals
# Somewhat Meaningless Version Info
appVer = "0.1"
appTitle = "Captcha Image Generator"
# Modes
verboseMode = False

#### Start Here
def main():
  print(f"{appTitle} Version {appVer}")
  # Defaults that really need to be overridden
  capString = None
  outFile = "temp.png"
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
    capImage = CaptchaImage(capString)
    newFile = open(outFile, "wb")
    newFile.write(capImage)
    newFile.close()
  else:
    print('File Error')

def showHelp():
  print(f"Usage: {sys.argv[0]} -s <YOURSTRING> -f <OUTPUTFILE>")
  exit(0)
  
def vprint(*args, **kwargs):
  if verboseMode == True:
    print("[VERBOSE] -- ", end = '')
    print(*args, **kwargs)

#### Generate an Image with Distorted Text
def CaptchaImage(capString):
  # Define a Blank PNG Image
  imgWidth = 320
  imgHeight = 82
  imgCanvas = Image(width=imgWidth, height=imgHeight, background=Color('WHITE'))
  imgCanvas.format = 'png'
  
  # Define a Drawing Object for Painting Colored Text
  drawTool = Drawing()
  drawTool.fill_color = Color(random.choice(['RED','GREEN','BLUE','BLACK']));
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
  lines = 15
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
#https://stackoverflow.com/questions/26286203/custom-print-function-that-wraps-print
#https://pynative.com/python-global-variables/
#https://www.freecodecamp.org/news/python-print-exception-how-to-try-except-print-an-error/
#https://docs.python.org/3/library/random.html
#https://www.geeksforgeeks.org/python-write-bytes-to-file/
#https://www.digitalocean.com/community/tutorials/python-command-line-arguments
