#!/usr/bin/env python3
"""Build script to dynamically generate lbase.yaml from subsystem modules."""

import argparse
import yaml
import sys
import os
from pathlib import Path

# Custom YAML dumper to prevent line wrapping
class NoWrapDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

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
    'name': 'elxr-minimal-installer-amd64',
    'description': 'AMD64 minimal installer configuration.',
    'architecture': 'amd64',
    'version': '${oc.env:DEFAULT_ELXR_VERSION}',
    'schemaVersion': 1,
    'params': {
        'version': '${version}',
        'source': '${oc.env:CURRENT_DIR}/elxr-minimal-installer-${version}-${architecture}.tar.gz'
    },
    'stages': {
        'install': [
            {
                'name': 'Create minimal rootfs tarball',
                'module': 'bootstrap.mmdebstrap',
                'options': {
                    'suite': 'aria',
                    'target': '${params.source}',
                    'architecture': '${architecture}',
                    'variant': 'minbase',
                    'setup_hooks': ['sync-in overlay/minimal/ /'],
                    'customize_hooks': [],
                    'packages': [],
                    'dpkgopt': [],
                    'mirrors': ['deb http://mirror.elxr.dev/elxr aria main non-free-firmware contrib']
                }
            }
        ]
    }
}

def load_subsystem(filepath):
    """Load subsystem YAML file."""
    with open(filepath) as f:
        return yaml.safe_load(f)

def generate_lbase_yaml(enabled_subsystems, output_file):
    """Generate lbase.yaml from enabled subsystems."""
    config = BASE_TEMPLATE.copy()
    bootstrap_stage = config['stages']['install'][0]
    
    # Track hooks by priority: security first, cleanup last
    security_hooks = []
    regular_hooks = []
    cleanup_hooks = []
    
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
            if subsys_name == 'security':
                security_hooks.extend(subsys['customize_hooks'])
            elif subsys_name == 'cleanup':
                cleanup_hooks.extend(subsys['customize_hooks'])
            else:
                regular_hooks.extend(subsys['customize_hooks'])
        if subsys.get('dpkgopt'):
            bootstrap_stage['options']['dpkgopt'].extend(subsys['dpkgopt'])
    
    # Order: security (apt-key) -> regular -> cleanup (strip binaries)
    bootstrap_stage['options']['customize_hooks'].extend(security_hooks)
    bootstrap_stage['options']['customize_hooks'].extend(regular_hooks)
    bootstrap_stage['options']['customize_hooks'].extend(cleanup_hooks)
    
    # Add final depmod command at the end
    bootstrap_stage['options']['customize_hooks'].append('depmod -a -b $1 $(ls $1/lib/modules/) 2>/dev/null || true')
    
    with open(output_file, 'w') as f:
        f.write('---\n')
        yaml.dump(config, f, Dumper=NoWrapDumper, default_flow_style=False, sort_keys=False, width=float('inf'))
    
    print(f"Generated {output_file} with subsystems: {', '.join(enabled_subsystems)}")

def main():
    parser = argparse.ArgumentParser(description='Build minimal installer with modular subsystems')
    parser.add_argument('--enable',
                        help='Enable specific subsystems (space or comma-separated, or "all")')
    parser.add_argument('--output', default='base.yaml', help='Output file (default: base.yaml)')
    parser.add_argument('--output-dir', help='Output directory (default: current directory)')
    parser.add_argument('--list', action='store_true', help='List available subsystems')
    
    args = parser.parse_args()
    
    # Handle list command
    if args.list:
        print("Available subsystems:")
        for name, path in SUBSYSTEMS.items():
            subsys_file = Path(__file__).parent / path
            if subsys_file.exists():
                subsys = load_subsystem(subsys_file)
                print(f"  {name:12} - {subsys.get('description', 'No description')}")
        return
    
    # Determine enabled subsystems
    if args.enable:
        # Handle 'all' keyword
        if args.enable.lower() == 'all':
            enabled_subsystems = list(SUBSYSTEMS.keys())
        else:
            # Parse comma-separated or space-separated subsystems
            if ',' in args.enable:
                enabled_subsystems = [s.strip() for s in args.enable.split(',') if s.strip()]
            else:
                enabled_subsystems = args.enable.split()
    else:
        print("Error: Must specify --enable or --list")
        print(f"Available subsystems: {', '.join(SUBSYSTEMS.keys())}")
        sys.exit(1)
    
    # Validate subsystems
    invalid_subsystems = [s for s in enabled_subsystems if s not in SUBSYSTEMS]
    if invalid_subsystems:
        print(f"Error: Invalid subsystems: {', '.join(invalid_subsystems)}")
        print(f"Available subsystems: {', '.join(SUBSYSTEMS.keys())}")
        sys.exit(1)
    
    if not enabled_subsystems:
        print("Error: No subsystems enabled. Use --enable or --list")
        print(f"Available subsystems: {', '.join(SUBSYSTEMS.keys())}")
        sys.exit(1)
    
    # Handle output path
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        output_path = os.path.join(args.output_dir, args.output)
    else:
        output_path = args.output
    
    generate_lbase_yaml(enabled_subsystems, output_path)

if __name__ == '__main__':
    main()
