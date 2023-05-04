#!/usr/bin/python3

#### Captcha HTTP Server

#### Libraries
import sys
from capimg import CaptchaImage

#### Globals
# Somewhat Meaningless Version Info
appVer = "0.1"
appTitle = "Captcha Server"
# Network Settings
hostName = "localhost"
portNum = 8080
# Sample Data for Random Choice
charChoices = "987654321ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"

#### Run as Standalone App or Module
if __name__ == '__main__':
  # Standalone Mode
  main()
print(f"{appTitle} Version {appVer}")
