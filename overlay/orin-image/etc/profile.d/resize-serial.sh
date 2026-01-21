if [ "$(tty)" = /dev/ttyS0 -o "$(tty)" = /dev/ttymxc0 ]; then
  /usr/bin/resize > /dev/null
fi
