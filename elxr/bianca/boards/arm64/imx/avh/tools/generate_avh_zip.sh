#!/bin/bash
#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# This script is used to the new zip file of AVH from the original image file.
# Refer to:
# https://developer.arm.com/documentation/107660/0200/Custom-Firmware/Firmware/Understanding-Firmware-on-AVH
# Boot Arguments:
# console=ttymxc1,115200 earlycon= root=/dev/mmcblk2p3 initcall_blacklist=pca953x_init
#
# Usage:
#   ./generate_avh_zip.sh <image_file>
#
# Arguments:
#   <image_file>: the original image file.
set -x

if [ -z "$1" ]; then
   echo "please input image file!"
   exit 1
fi

image=$1

temp_dir=$(mktemp -d)
cd "$temp_dir" || exit 1
cp "$image" nand

off2=$(parted "$image" -s unit b print | awk 'NR==9  {print substr($2, 1, length($2)-1)}')
off3=$(parted "$image" -s unit b print | awk 'NR==10 {print substr($2, 1, length($2)-1)}')
mkdir mnt

mount -o loop,offset="$off2" "$image" mnt
cp mnt/vmlinuz-* kernel
cp mnt/initrd.img-* ramdisk.img
umount mnt

mount -o loop,offset="$off3" "$image" mnt
cp mnt/usr/lib/modules/*/dtb/imx8mp-evk.dtb devicetree
umount mnt

cat << EOF > Info.plist

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" http://www.apple.com/DTDs/PropertyList-1.0.dtd>
<plist version="1.0">
<dict>
    <key>Type</key>
    <string>iot</string>
    <key>UniqueIdentifier</key>
    <string>elxr imx8mp OS</string>
    <key>DeviceIdentifier</key>
    <string>imx8mp-evk</string>
    <key>Version</key>
    <string>1.0.0</string>
    <key>Build</key>
    <string>Edge</string>
</dict>
</plist>

EOF

zfile=${image/.img/.zip}
zip -r "$zfile" Info.plist nand devicetree kernel ramdisk.img
cd - || exit 1; rm -rf "$temp_dir"

