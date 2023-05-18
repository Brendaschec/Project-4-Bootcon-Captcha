#!/bin/bash


#### Captcha Project
# init program for demo container


#### Oneshot Services
# < none >


#### Background Services
services=(
  '/usr/bin/mariadbd-safe --user=root --bind-address=127.0.0.1 --init-file=/etc/mariadb-init'
  '/usr/sbin/php-fpm --nodaemonize'
  '/usr/sbin/nginx -g "daemon off;"'
  '/captcha/server.py -v'
)


#### PID List
pids=()


#### Start Services and Record PIDs
function startup {
  echo "[ % ] - Starting Up!"
  for service in "${services[@]}"; do
    eval "$service &"
    pids+=( $! )
    echo "[ * ] - Started $service with PID $!"
  done
}


#### Stop the Recorded PIDs
function shutdown {
  echo "[ % ] - Shutting Down!"
  for pid in "${pids[@]}"; do
    echo "[ * ] - Killing PID $pid"
    kill "$pid"
  done
  exit 0
}


#### Signal Handling
# Run shutdown function when container stops or SIGINT (Ctrl+C)
trap shutdown SIGTERM SIGINT


#### Get Going!
startup


#### Wait Until Signaled
wait
