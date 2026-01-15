#!/bin/bash
# This file is part of dracut.
# SPDX-License-Identifier: GPL-2.0-or-later

installkernel() {
    inst_multiple -o /lib/firmware/*
}
