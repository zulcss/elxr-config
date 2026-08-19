# shellcheck disable=SC2148

# The ShellCheck tip SC2148 recommends adding a target shell hint such
# as a shebang.
# SC2148 is disabled because this file is sourced by /etc/profile
# which is the system-wide .profile file for the Bourne shell (sh(1))
# and Bourne compatible shells (bash(1), ksh(1), ash(1), ...).

if [ "$(tty)" = /dev/ttyS0 ] || [ "$(tty)" = /dev/ttymxc0 ]; then
  /usr/bin/resize > /dev/null
fi
