#!/bin/bash


#### Use Script Directory
cd $(dirname "${0}")


#### Configuration
imageName="captchademo_v3"
coreDir="../../core"


#### Check if Podman or Docker is installed
if which podman >/dev/null 2>&1; then
  BUILD_COMMAND="podman"
elif which docker >/dev/null 2>&1; then
  BUILD_COMMAND="docker"
else
  echo "Neither Docker nor Podman is installed. Exiting."
  exit 1
fi


#### Temporarily copy core directory to build directory
cp -r "$coreDir" .


#### Run image build
$BUILD_COMMAND build . -t "$imageName"


#### Remove temporary files
rm -rf ./core


