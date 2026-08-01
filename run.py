#!/usr/bin/env python3
#belongs in Kcow-s-Moomapper-ked/run.py -Version:1.6
# X-Seti-2026-08-01

import os
import sys
import traceback

# vers: 1.6
def main():
    try:
        setup_paths()
        from apps.components.Moomapper.Moomapper import main as run_app
        run_app()
    except Exception as e:
        print(f"Failed to start Moomapper: {e}")
        traceback.print_exc()
        sys.exit(1)

# vers: 1.6
def setup_paths():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

if __name__ == "__main__":
    main()