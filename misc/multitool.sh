#!/bin/bash

# Work relative to script dir -> repo dir
cd $(dirname ${0})
cd ../

function upcontent {
  sudo rsync -vr ./demo/* /usr/share/nginx/html/
}

echo "What do you want to do? (Enter a number)"
echo "1 - Update static web content"
echo ""

read optnumber

case ${optnumber} in
  1)
    upcontent
    ;;
  *)
    echo "Invalid Option. Quitting..."; exit 2
    ;;
esac


