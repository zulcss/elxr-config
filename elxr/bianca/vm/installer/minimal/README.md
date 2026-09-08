# Ultra-Minimal Subsystem Installer

Modular ultra-minimal installer configuration for AMD64 systems using
component-based architecture.

## Overview

This directory contains a modular build system that generates installer
configurations from individual subsystem components. Each component defines
specific packages, customization hooks, and dpkg options that are combined to
create the final installer tarball.

## Components

| Component | Description |
|-----------|-------------|
| `base` | Essential base system configuration |
| `boot` | Boot components (systemd-boot, init system) |
| `cleanup` | System cleanup and optimization |
| `management` | System management tools |
| `network` | Network configuration |
| `security` | Security configuration |
| `storage` | Storage drivers and utilities |

## Usage

Generate installer configuration with all subsystems:

```bash
python3 build.py --enable all
# or
python3 build.py --enable "base,boot,cleanup,management,network,security,storage"
```

Generate with specific subsystems only:

```bash
python3 build.py --enable "base,boot,network,storage"
```

Custom output file:

```bash
python3 build.py --enable "base,boot" --output custom.yaml
```

List available subsystems:

```bash
python3 build.py --list
```

## Output

The build script generates a complete installer configuration that:

- Creates an ultra-minimal rootfs tarball
- Includes only essential packages and drivers
- Applies aggressive cleanup and optimization
- Excludes non-essential kernel modules and firmware
- Results in a minimal installer suitable for edge devices

## Architecture

- **Modular Design**: Each subsystem is independently defined
- **Hook Ordering**: Security hooks → Regular hooks → Cleanup hooks
- **Package Aggregation**: All component packages are merged
- **dpkg Optimization**: Path exclusions are combined from all components
