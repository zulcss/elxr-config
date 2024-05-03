#!/bin/sh

# k3s installer script expects dbus to running which does not happen in
# mmdebstrap so download the install script and execute it later.

set -eu

if [ "${MMDEBSTRAP_VERBOSITY:-1}" -ge 3 ]; then
	set -x
fi

rootdir="$1"
INSTALL_K3S_VERSION=v1.29.3+k3s1
mkdir -p $rootdir/usr/share/rancher
curl https://raw.githubusercontent.com/rancher/k3s/$INSTALL_K3S_VERSION/install.sh \
       	-o $rootdir/usr/share/rancher/install.sh
chmod +x $rootdir/usr/share/rancher/install.sh
