#!/bin/sh


set -eu

if [ "${MMDEBSTRAP_VERBOSITY:-1}" -ge 3 ]; then
	set -x
fi

rootdir="$1"
mkdir -p $rootdir/usr/share/helm
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \
       	-o $rootdir/usr/share/helm/install.sh
chmod +x $rootdir/usr/share/helm/install.sh
