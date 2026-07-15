#!/usr/bin/env python3
"""Build script to dynamically generate image.yaml from subsystem modules."""

import argparse
import yaml
import sys
import os
from pathlib import Path

# Custom YAML dumper to prevent line wrapping
class NoWrapDumper(yaml.SafeDumper):
    def represent_str(self, data):
        if '\n' in data:
            return self.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return self.represent_scalar('tag:yaml.org,2002:str', data)

NoWrapDumper.add_representer(str, NoWrapDumper.represent_str)

SUBSYSTEMS = {
    'base': 'component/base.yaml',
    'boot': 'component/boot.yaml',
    'cleanup': 'component/cleanup.yaml',
    'management': 'component/management.yaml',
    'network': 'component/network.yaml',
    'security': 'component/security.yaml',
    'storage': 'component/storage.yaml'
}

BASE_TEMPLATE = {
    'name': 'elxr-minimal-imx',
    'description': 'i.MX minimal configuration.',
    'architecture': 'arm64',
    'version': '${oc.env:DEFAULT_ELXR_VERSION}',
    'schemaVersion': 1,
    'params': {
        'version': '${version}',
        'source': '${oc.env:CURRENT_DIR}/${name}-${version}-${architecture}.tar.gz',
        'disk': '${oc.env:CURRENT_DIR}/${name}-${version}-${architecture}.img'
    },
    'stages': {
        'install': [
            {
                'name': 'Creating minimal rootfs',
                'module': 'bootstrap.mmdebstrap',
                'options': {
                    'suite': 'aria',
                    'target': '${params.source}',
                    'architecture': '${architecture}',
                    'variant': 'minbase',
                    'setup_hooks': [
                        'sync-in overlay/ultra-minimal/ /',
                        'sync-in overlay/systemd-networkd/ /'
                    ],
                    'customize_hooks': [],
                    'packages': [],
                    'dpkgopt': [],
                    'mirrors': ['deb http://mirror.elxr.dev/elxr aria main non-free-firmware contrib']
                }
            },
            {
                'name': 'Create raw image ${params.disk}',
                'module': 'image.raw',
                'options': {'name': '${params.disk}', 'size': '1G'}
            },
            {
                'name': 'Partitioning ${params.disk}',
                'module': 'installer.disk.parted',
                'options': {
                    'slices': [
                        {'name': 'EFI', 'start': '10MB', 'end': '128MB', 'flags': ['boot', 'esp'], 'id': 'c12a7328-f81f-11d2-ba4b-00a0c93ec93b'},
                        {'name': 'ROOT', 'start': '128MB', 'end': '100%', 'flags': [], 'id': ''}
                    ]
                }
            },
            {
                'name': 'Formatting ${params.disk}',
                'module': 'installer.disk.fs',
                'options': {
                    'filesystems': [
                        {'name': 'EFI', 'label': 'EFI', 'fs': 'vfat', 'options': []},
                        {'name': 'ROOT', 'label': 'ROOT', 'fs': 'ext4', 'options': []}
                    ]
                }
            },
            {
                'name': 'Unpacking ${params.source}',
                'module': 'installer.unpack',
                'options': []
            },
            {
                'name': 'Installing bootloader on ${params.disk}',
                'module': 'installer.bootloader',
                'options': {'kernel_args': 'root=LABEL=ROOT rw console=tty0'}
            },
            {
                'name': 'Compress image ${params.disk}',
                'module': 'image.compress',
                'options': {'name': '${params.disk}', 'compression': 'zstd'}
            }
        ]
    }
}

def load_subsystem(filepath):
    """Load subsystem YAML file."""
    with open(filepath) as f:
        return yaml.safe_load(f)

def generate_image_yaml(enabled_subsystems, output_file):
    """Generate image.yaml from enabled subsystems."""
    config = BASE_TEMPLATE.copy()
    bootstrap_stage = config['stages']['install'][0]
    
    for subsys_name in enabled_subsystems:
        if subsys_name not in SUBSYSTEMS:
            print(f"Warning: Unknown subsystem '{subsys_name}', skipping")
            continue
        
        subsys_file = Path(__file__).parent / SUBSYSTEMS[subsys_name]
        if not subsys_file.exists():
            print(f"Error: Subsystem file {subsys_file} not found")
            sys.exit(1)
        
        subsys = load_subsystem(subsys_file)
        
        if subsys.get('packages'):
            bootstrap_stage['options']['packages'].extend(subsys['packages'])
        if subsys.get('customize_hooks'):
            bootstrap_stage['options']['customize_hooks'].extend(subsys['customize_hooks'])
        if subsys.get('dpkgopt'):
            bootstrap_stage['options']['dpkgopt'].extend(subsys['dpkgopt'])
    
    with open(output_file, 'w') as f:
        yaml.dump(config, f, Dumper=NoWrapDumper, default_flow_style=False, sort_keys=False, width=120, indent=2)
    
    print(f"Generated {output_file} with subsystems: {', '.join(enabled_subsystems)}")

def main():
    parser = argparse.ArgumentParser(description='Build minimal ARM64 i.MX image with modular subsystems')
    parser.add_argument('--enable', required=True,
                        help='Enable specific subsystems (space or comma-separated, or "all")')
    parser.add_argument('--output', default='image.yaml', help='Output file (default: image.yaml)')
    parser.add_argument('--output-dir', help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    # Parse comma-separated or space-separated subsystems
    if args.enable.lower() == 'all':
        enabled_subsystems = list(SUBSYSTEMS.keys())
    elif ',' in args.enable:
        enabled_subsystems = [s.strip() for s in args.enable.split(',') if s.strip()]
    else:
        enabled_subsystems = args.enable.split()
    
    # Validate subsystems
    invalid_subsystems = [s for s in enabled_subsystems if s not in SUBSYSTEMS]
    if invalid_subsystems:
        print(f"Error: Invalid subsystems: {', '.join(invalid_subsystems)}")
        print(f"Available subsystems: {', '.join(SUBSYSTEMS.keys())}")
        sys.exit(1)
    
    if not enabled_subsystems:
        print("Error: No subsystems enabled. Use --enable to specify subsystems.")
        print(f"Available subsystems: {', '.join(SUBSYSTEMS.keys())}")
        sys.exit(1)
    
    # Handle output path
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        output_path = os.path.join(args.output_dir, args.output)
    else:
        output_path = args.output
    
    generate_image_yaml(enabled_subsystems, output_path)

if __name__ == '__main__':
    main()
