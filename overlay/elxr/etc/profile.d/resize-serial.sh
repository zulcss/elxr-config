ttydev="$(tty)"
case "$ttydev" in
  /dev/ttyS0 | /dev/ttymxc0)
    if [ -x /usr/bin/resize ]; then
      # echo "Resizing terminal for $ttydev..."
      /usr/bin/resize > /dev/null 2>&1
    fi
    ;;
esac
