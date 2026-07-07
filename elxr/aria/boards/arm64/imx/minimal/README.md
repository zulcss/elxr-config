# Ultra-Minimal (ARM64 i.MX)

Modular, bare-bones command-line-only image for resource-constrained ARM64
i.MX edge devices.

## Components

Available component YAML files:

- **base.yaml**: Essential base system configuration for ARM64 i.MX
- **boot.yaml**: Essential boot components (systemd-boot, kernel, init) for ARM64
- **cleanup.yaml**: Aggressive cleanup for minimal size on ARM64
- **management.yaml**: Basic package management tools (apt, dpkg)
- **network.yaml**: Minimal networking (systemd-networkd only)
- **security.yaml**: Essential security components, minimal CA certificates
- **storage.yaml**: Core filesystems only (ext4, vfat)

### Base Component

- Essential base system for ARM64 i.MX boards
- Root user setup and hostname configuration
- Basic systemd services (networkd, getty)

### Boot Component

- Essential boot components only (systemd-boot, kernel, init)
- ARM64-specific kernel (linux-image-arm64)
- Stripped drivers (GPU, media, staging, wireless, USB, HID)
- ARM64 UEFI boot configuration (BOOTAA64.EFI)

### Network Component

- Minimal networking (systemd-networkd only)
- Excludes wireless/bluetooth drivers and firmware
- Basic network utilities (iproute2, iputils-ping)

### Storage Component

- Core filesystems only (ext4, vfat)
- Excludes xfs/btrfs/nfs/smb/f2fs/fuse/overlayfs/squashfs/isofs

### Security Component

- Essential security components
- Minimal CA certificates
- Basic authentication (root user setup)
- GPG support for package verification

### Management Component

- Basic package management tools (apt, dpkg)
- Preserves customer extension capability
- Maintains dependency resolution
- Essential utilities (bash, coreutils, util-linux)

### Cleanup Component

- Aggressive size optimization for ARM64
- Removes documentation, man pages, locales (except en*)
- Strips debug symbols from binaries and kernel modules
- Removes development headers and static libraries
- ARM64-specific cleanup (aarch64-linux-gnu paths)

## Usage

Generate image.yaml dynamically:

```bash
# Ultra-minimal (all components)
./build.py --enable all
# or
./build.py --enable base,boot,cleanup,management,network,security,storage

# With individual components
./build.py --enable base,boot,cleanup
./build.py --enable base,boot,cleanup,management

# Custom output directory
./build.py --enable base,boot,cleanup,management,security \
  --output-dir /tmp --output image.yaml
```

## Example

```bash
cd elxr-config/elxr/aria/boards/arm64/imx/minimal
./build.py --enable all --output image.yaml
```

This generates an image.yaml using modular component architecture for ARM64
i.MX board deployment.

## Architecture Differences

This ARM64 i.MX version differs from the VM version in:

- Uses `linux-image-arm64` instead of `linux-image-cloud-amd64`
- ARM64 UEFI boot configuration (`BOOTAA64.EFI`)
- ARM64-specific cleanup paths (`aarch64-linux-gnu`)
- i.MX board-specific partitioning (10MB start offset for EFI)
- Console configuration optimized for embedded ARM64 devices
