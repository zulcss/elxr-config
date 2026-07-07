# Ultra-Minimal

Modular, bare-bones command-line-only image for resource-constrained edge devices.

## Components

Available component YAML files:

- **base.yaml**: Essential base system configuration
- **boot.yaml**: Essential boot components (systemd-boot, kernel, init)
- **cleanup.yaml**: Aggressive cleanup for minimal size
- **management.yaml**: Basic package management tools (apt, dpkg)
- **network.yaml**: Minimal networking (systemd-networkd only)
- **security.yaml**: Essential security components, minimal CA certificates
- **storage.yaml**: Core filesystems only (ext4, vfat)

### Boot Component

- Essential boot components only (systemd-boot, kernel, init)
- Stripped drivers (GPU, media, staging, wireless, USB, HID)
- Minimal firmware (Intel/AMD essentials only)

### Network Component

- Minimal networking (systemd-networkd only)
- Excludes wireless/bluetooth drivers and firmware

### Storage Component

- Core filesystems only (ext4, vfat)
- Excludes xfs/btrfs/nfs/smb/f2fs/fuse/overlayfs/squashfs/isofs

### Security Component

- Essential security components
- Minimal CA certificates (Mozilla only)
- Basic authentication (root user setup)

### Management Component

- Basic package management tools (apt, dpkg)
- Preserves customer extension capability
- Maintains dependency resolution

### Cleanup Component

- Aggressive size optimization
- Removes documentation, man pages, locales (except en*)
- Strips debug symbols from binaries and kernel modules
- Removes development headers and static libraries

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
cd elxr-config/elxr/bianca/cloud/ec2/minimal
./build.py --enable all --output image.yaml
```

This generates an image.yaml using modular component architecture for VM
deployment.
