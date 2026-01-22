# shellcheck disable=SC2148

# The ShellCheck tip SC2148 recommends adding a target shell hint such
# as a shebang.
# SC2148 is disabled because this file is sourced by /etc/profile
# which is the system-wide .profile file for the Bourne shell (sh(1))
# and Bourne compatible shells (bash(1), ksh(1), ash(1), ...).

ttydev="$(tty)"
case "$ttydev" in
  /dev/ttyS0 | /dev/ttymxc0)
    if [ -x /usr/bin/resize ]; then
      # echo "Resizing terminal for $ttydev..."
      /usr/bin/resize > /dev/null 2>&1
    fi
    ;;
esac
