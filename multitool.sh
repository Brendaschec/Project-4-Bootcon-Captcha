#!/bin/bash

cd $(dirname ${0})

function upcontent {
  sudo rsync -vr ./html/* /usr/share/nginx/html/
}

echo "What do you want to do? (Enter a number)"
echo "1 - Update static web content"
echo ""

read -n1 optnumber
echo -e "\n"

case ${optnumber} in
  1)
    upcontent
    ;;
  *)
    echo "Invalid Option. Quitting..."; exit 2
    ;;
esac


