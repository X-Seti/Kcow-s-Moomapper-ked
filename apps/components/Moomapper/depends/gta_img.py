#belongs in apps/components/Moomapper/depends/gta_img.py -Version:1.6
# X-Seti-2026-08-01

import os
import struct
from typing import List, Dict, Optional, BinaryIO

# vers: 1.6
def _find_companion(file_path: str, extension: str) -> Optional[str]:
    """Find companion file with given extension (case-insensitive)"""
    base_path = os.path.splitext(file_path)[0]
    
    # Try lowercase extension first
    lower_path = base_path + extension
    if os.path.exists(lower_path):
        return lower_path
    
    # Try uppercase extension
    upper_path = base_path + extension.upper()
    if os.path.exists(upper_path):
        return upper_path
    
    return None

# vers: 1.6
class DirEntry:
    __slots__ = ['start_block', 'block_count', 'name', 'index', 'delete']
    
    def __init__(self):
        self.start_block: int = 0
        self.block_count: int = 0
        self.name: str = ""
        self.index: int = 0
        self.delete: bool = False

    # vers: 1.6
    @classmethod
    def from_bytes(cls, data: bytes, index: int) -> 'DirEntry':
        entry = cls()
        entry.start_block, entry.block_count, name_bytes = struct.unpack('<II24s', data)
        entry.name = name_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
        entry.index = index
        entry.delete = False
        return entry

    # vers: 1.6
    def to_bytes(self) -> bytes:
        name_bytes = self.name.encode('ascii')[:24].ljust(24, b'\x00')
        return struct.pack('<II24s', self.start_block, self.block_count, name_bytes)

# vers: 1.6
class GTA3Archive:
    def __init__(self, filename: str, create_new: bool = False):
        self.filename = filename
        self.entries: List[DirEntry] = []
        self.archive_list: Dict[str, int] = {}
        self.read_only = False
        self.archive_opened = False
        self.f_dir: Optional[BinaryIO] = None
        self.f_img: Optional[BinaryIO] = None
        self._open_files(filename, create_new)

    # vers: 1.6
    def _open_files(self, filename: str, create_new: bool):
        # Check if this is a dual-file format (GTA III/VC) or single-file (SA)
        dir_filename = _find_companion(filename, '.dir')
        has_dir_file = dir_filename is not None
        
        try:
            if create_new:
                self.f_img = open(filename, 'wb')
                if has_dir_file or True:  # Always create .dir for GTA III/VC format
                    dir_path = os.path.splitext(filename)[0] + '.dir'
                    self.f_dir = open(dir_path, 'wb')
            else:
                # Try to open IMG file
                self.f_img = open(filename, 'r+b')
                
                # Try to open DIR file if it exists
                if has_dir_file:
                    self.f_dir = open(dir_filename, 'r+b')
                else:
                    # Single file format (San Andreas) - no .dir file
                    self.f_dir = None
                
        except IOError as e:
            print(f"Error opening files: {e}")
            self.read_only = True
            try:
                self.f_img = open(filename, 'rb')
                if has_dir_file:
                    self.f_dir = open(dir_filename, 'rb')
                else:
                    self.f_dir = None
            except IOError:
                self.archive_opened = False
                return

        self.archive_opened = True
        
        if not create_new:
            if self.f_dir:
                # Read from .dir file (GTA III/VC format)
                self.f_dir.seek(0, os.SEEK_END)
                dir_size = self.f_dir.tell()
                self.f_dir.seek(0)
                
                entry_count = dir_size // 32
                for i in range(entry_count):
                    data = self.f_dir.read(32)
                    if len(data) == 32:
                        self.entries.append(DirEntry.from_bytes(data, i))
            else:
                # Read from IMG file header (San Andreas format)
                self._read_sa_directory()
        
        self.create_list()

    # vers: 1.6
    def _read_sa_directory(self):
        """Read directory entries from San Andreas IMG format (VER2)"""
        if not self.f_img:
            return
            
        self.f_img.seek(0)
        header = self.f_img.read(8)
        if len(header) < 8:
            return
        
        # Check for SA IMG header (VER2)
        if header[:4] == b'VER2':
            # Read entry count
            entry_count = struct.unpack('<I', header[4:8])[0]
            
            # Read entries
            for i in range(entry_count):
                data = self.f_img.read(32)
                if len(data) == 32:
                    self.entries.append(DirEntry.from_bytes(data, i))
        else:
            # Not a valid SA IMG file
            print(f"Error: Invalid IMG header in {self.filename}")

    # vers: 1.6
    def create_list(self):
        self.archive_list = {e.name.lower(): i for i, e in enumerate(self.entries) if not e.delete}

    # vers: 1.6
    def destroy_list(self):
        self.archive_list.clear()

    # vers: 1.6
    def do_remove(self):
        self.entries = [e for e in self.entries if not e.delete]
        if self.f_dir:
            self.f_dir.seek(0)
            self.f_dir.truncate()
            for i, entry in enumerate(self.entries):
                entry.index = i
                self.f_dir.write(entry.to_bytes())
        self.create_list()

    # vers: 1.6
    def entry_count(self) -> int:
        return len(self.entries) if self.archive_opened else 0

    # vers: 1.6
    def extract(self, index: int, stream: BinaryIO):
        if index < 0 or index >= len(self.entries):
            return
        entry = self.entries[index]
        if self.f_img:
            self.f_img.seek(entry.start_block * 2048)
            if entry.block_count > 0:
                stream.write(self.f_img.read(entry.block_count * 2048))

    # vers: 1.6
    def get_entry(self, index: int) -> DirEntry:
        return self.entries[index]

    # vers: 1.6
    def mark_for_removal(self, index: int):
        self.entries[index].delete = True

    # vers: 1.6
    def rename(self, index: int, new_name: str):
        self.entries[index].name = new_name
        if self.f_dir:
            self.f_dir.seek(index * 32)
            self.f_dir.write(self.entries[index].to_bytes())
        self.create_list()

# vers: 1.6
class GTAImg(GTA3Archive):
    def __init__(self, filename: str = ""):
        super().__init__(filename, False)
        self.txd_list: Dict[str, int] = {}
        self.dff_list: Dict[str, int] = {}

    # vers: 1.6
    def create_dff_list(self):
        self.dff_list = {e.name.lower(): i for i, e in enumerate(self.entries) 
                        if e.name.lower().endswith('.dff') and not e.delete}

    # vers: 1.6
    def create_txd_list(self):
        self.txd_list = {e.name.lower(): i for i, e in enumerate(self.entries) 
                        if e.name.lower().endswith('.txd') and not e.delete}

    # vers: 1.6
    def destroy_dff_list(self):
        self.dff_list.clear()

    # vers: 1.6
    def destroy_txd_list(self):
        self.txd_list.clear()

    # vers: 1.6
    def dff_exists(self, in_name: str) -> bool:
        in_name = in_name.lower()
        if in_name.endswith('.dff'):
            in_name = in_name[:-4]
        return f"{in_name}.dff".lower() in self.archive_list

    # vers: 1.6
    def get_dff_num(self, in_name: str) -> int:
        in_name = in_name.lower()
        if in_name.endswith('.dff'):
            in_name = in_name[:-4]
        return self.archive_list.get(f"{in_name}.dff", -1)

    # vers: 1.6
    def get_entry_num(self, in_name: str) -> int:
        return self.archive_list.get(in_name.lower(), -1)

    # vers: 1.6
    def get_txd_num(self, in_name: str) -> int:
        in_name = in_name.lower()
        if in_name == 'generic':
            return 0
        if in_name.endswith('.txd'):
            in_name = in_name[:-4]
        return self.archive_list.get(f"{in_name}.txd", -1)

    # vers: 1.6
    def txd_exists(self, in_name: str) -> bool:
        in_name = in_name.lower()
        if in_name == 'generic':
            return True
        if in_name.endswith('.txd'):
            in_name = in_name[:-4]
        return f"{in_name}.txd" in self.archive_list