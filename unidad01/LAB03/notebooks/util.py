from pathlib import Path
import sys
import os

def get_dir_path(dir):
    """Get the path for givel directory"""
    parent_dir = Path().resolve().parent
    dir_path = os.path.join(parent_dir, dir)
    return dir_path

def add_dir_path_to_sys_path(dir_path):
    """Add a directory path to sys.path"""
    print(f"Adding: {dir_path} to sys.path")
    if not dir_path in sys.path:
        sys.path.append(dir_path)

def make_dir_modules_importable():
    """
    - Make dir available into sys.append. This make possible to import from other directories
    - uv makes this atomatically.
    """
    src_dir_path = get_dir_path("src")

    add_dir_path_to_sys_path(src_dir_path)