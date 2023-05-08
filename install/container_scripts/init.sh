#!/bin/bash

#### Captcha Project
# init program for demo container

# Oneshot Services
/setup

# Background Services
services=(
  '/usr/sbin/nginx -g "daemon off;"'
  '/gitrepo/apps/captcha/capsvr.py'
)

pids=()

# Start services and record pids
function startup {
  echo "[ % ] - Starting Up!"
  for service in "${services[@]}"; do
    eval "$service &"
    pids+=( $! )
    echo "[ * ] - Started $service with PID $!"
  done
}

# Stop the pids you started
function shutdown {
  echo "[ % ] - Shutting Down!"
  for pid in "${pids[@]}"; do
    echo "[ * ] - Killing PID $pid"
    kill "$pid"
  done
  exit 0
}

# Run shutdown function when container stops or when receiving SIGINT (Ctrl+C)
trap shutdown SIGTERM SIGINT

startup

# Wait until signaled
wait
