#!/usr/bin/env python3
#belongs in Kcow-s-Moomapper-ked/installer.py -Version:1.6
# X-Seti-2026-08-01

import os
import sys
import shutil
import argparse

# vers: 1.6
def check_dependencies():
    try:
        import PyQt5
        import OpenGL
        return True
    except ImportError:
        print("Missing dependencies. Please run: pip install PyQt5 PyOpenGL")
        return False

# vers: 1.6
def create_init_files(base_path):
    """Create necessary __init__.py files for Python packages"""
    init_dirs = [
        'apps',
        'apps/components',
        'apps/components/Moomapper',
        'apps/components/Moomapper/depends'
    ]
    
    for dir_path in init_dirs:
        full_path = os.path.join(base_path, dir_path)
        init_file = os.path.join(full_path, '__init__.py')
        if os.path.exists(full_path) and not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Python package init\n")
            print(f"Created {init_file}")

# vers: 1.6
def copy_directory_safe(src, dst, ignore_dirs=None):
    """Safely copy directory contents without deleting existing files"""
    if ignore_dirs is None:
        ignore_dirs = []
    
    if not os.path.exists(src):
        print(f"Warning: Source directory not found: {src}")
        return
        
    for item in os.listdir(src):
        if item in ignore_dirs:
            continue
            
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isdir(src_path):
            if os.path.exists(dst_path):
                copy_directory_safe(src_path, dst_path, ignore_dirs)
            else:
                shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
    
    print(f"Merged {src} into {dst}")

# vers: 1.6
def install_img_factory(target_path):
    if not os.path.exists(target_path):
        print(f"Error: IMG Factory path not found: {target_path}")
        return
        
    apps_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps')
    apps_dst = os.path.join(target_path, 'apps')
    
    if not os.path.exists(apps_src):
        print("Error: Source 'apps' directory not found.")
        return
    
    os.makedirs(apps_dst, exist_ok=True)
        
    print("Installing into IMG Factory 1.6 (ignoring utils and themes)...")
    copy_directory_safe(apps_src, apps_dst, ignore_dirs=['utils', 'themes'])
    create_init_files(target_path)
    print("Installation complete. Existing files preserved.")

# vers: 1.6
def install_standalone(target_path):
    os.makedirs(target_path, exist_ok=True)
    src_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Installing standalone to {target_path}...")
    
    for item in ['apps', 'depends', 'source']:
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(target_path, item)
        if os.path.exists(src_path):
            copy_directory_safe(src_path, dst_path)
    
    for item in ['run.py', 'README.md', 'ChangeLog']:
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(target_path, item)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
    
    create_init_files(target_path)
    print("Standalone installation complete.")

# vers: 1.6
def main():
    if not check_dependencies():
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="Moo Mapper Installer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--imgfactory', type=str, help='Path to IMG Factory 1.6 root directory')
    group.add_argument('--standalone', type=str, help='Path for standalone installation')
    
    args = parser.parse_args()
    
    if args.imgfactory:
        install_img_factory(args.imgfactory)
    elif args.standalone:
        install_standalone(args.standalone)

if __name__ == "__main__":
    main()