#!/usr/bin/env python3
#belongs in Kcow-s-Moomapper-ked/test_imports.py -Version:1.6
# X-Seti-2026-08-01

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    import PyQt5
    print("✓ PyQt5 found")
except ImportError as e:
    print(f"✗ PyQt5 missing: {e}")

try:
    import OpenGL
    print("✓ PyOpenGL found")
except ImportError as e:
    print(f"✗ PyOpenGL missing: {e}")

try:
    from apps.components.Moomapper.depends.gta_img import GTAImg
    print("✓ gta_img.py loads")
except Exception as e:
    print(f"✗ gta_img.py failed: {e}")

try:
    from apps.components.Moomapper.Moomapper import MoomapperWindow
    print("✓ Moomapper.py loads")
except Exception as e:
    print(f"✗ Moomapper.py failed: {e}")
    import traceback
    traceback.print_exc()

print("\nIf all tests pass, try: python3 run.py")