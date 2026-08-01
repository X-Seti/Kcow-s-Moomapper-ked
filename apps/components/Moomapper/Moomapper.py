#belongs in apps/components/Moomapper/depends/gta_img.py -Version:1.6
# X-Seti-2026-08-01

import os
import struct
from typing import List, Dict, Any, Optional, BinaryIO

# vers: 1.6
class DirEntry:
    __slots__ = ['start_block', 'block_count', 'name', 'index', 'delete']
    
    def __init__(self):
        self.start_block: int = 0
        self.block_count: int = 0
        self.name: str = ""
        self.index: int = 0
        self.delete: bool = False

    @classmethod
    def from_bytes(cls, data: bytes, index: int) -> 'DirEntry':
        entry = cls()
        entry.start_block, entry.block_count, name_bytes = struct.unpack('<II24s', data)
        entry.name = name_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
        entry.index = index
        entry.delete = False
        return entry

    def to_bytes(self) -> bytes:
        name_bytes = self.name.encode('ascii')[:24].ljust(24, b'\x00')
        return struct.pack('<II24s', self.start_block, self.block_count, name_bytes)

# vers: 1.6
class GTA3Archive:
    def __init__(self, filename: str, create_new: bool = False, only_textures: bool = False):
        self.filename = filename
        self.entries: List[DirEntry] = []
        self.archive_list: Dict[str, int] = {}
        self.read_only = False
        self.archive_opened = False
        self.f_dir: Optional[BinaryIO] = None
        self.f_img: Optional[BinaryIO] = None
        self._open_files(filename, create_new, only_textures)

    def _open_files(self, filename: str, create_new: bool, only_textures: bool):
        mode = 'wb' if create_new else 'r+b'
        try:
            self.f_img = open(filename, mode)
            self.f_dir = open(os.path.splitext(filename)[0] + '.dir', mode)
        except IOError:
            self.read_only = True
            try:
                self.f_img = open(filename, 'rb')
                self.f_dir = open(os.path.splitext(filename)[0] + '.dir', 'rb')
            except IOError:
                self.archive_opened = False
                return

        self.archive_opened = True
        if not create_new:
            self.f_dir.seek(0, os.SEEK_END)
            dir_size = self.f_dir.tell()
            self.f_dir.seek(0)
            for i in range(dir_size // 32):
                data = self.f_dir.read(32)
                if len(data) == 32:
                    self.entries.append(DirEntry.from_bytes(data, i))
        self.create_list()

    def add(self, filename: str, stream: BinaryIO):
        pass  # Overridden in GTAImg

    def create_list(self):
        self.archive_list = {e.name.lower(): i for i, e in enumerate(self.entries) if not e.delete}

    def destroy_list(self):
        self.archive_list.clear()

    def do_remove(self):
        self.entries = [e for e in self.entries if not e.delete]
        self.f_dir.seek(0)
        self.f_dir.truncate()
        for i, entry in enumerate(self.entries):
            entry.index = i
            self.f_dir.write(entry.to_bytes())
        self.create_list()

    def entry_count(self) -> int:
        return len(self.entries) if self.archive_opened else 0

    def extract(self, index: int, stream: BinaryIO):
        entry = self.entries[index]
        self.f_img.seek(entry.start_block * 2048)
        if entry.block_count > 0:
            stream.write(self.f_img.read(entry.block_count * 2048))

    def get_entry(self, index: int) -> DirEntry:
        return self.entries[index]

    def mark_for_removal(self, index: int):
        self.entries[index].delete = True

    def rename(self, index: int, new_name: str):
        self.entries[index].name = new_name
        self.f_dir.seek(index * 32)
        self.f_dir.write(self.entries[index].to_bytes())
        self.create_list()

# vers: 1.6
class GTAImg(GTA3Archive):
    def __init__(self, filename: str = ""):
        super().__init__(filename, False, False)
        self.txd_list: Dict[str, int] = {}
        self.dff_list: Dict[str, int] = {}
        self.gtxd: List[Any] = []
        self.gdff: List[Any] = []
        self.kill_not_used = False

    def add(self, filename: str, stream: BinaryIO):
        pass  # To be implemented with TXD/DFF tracking

    def create_dff_list(self):
        self.dff_list = {obj.name.lower(): i for i, obj in enumerate(self.gdff)}

    def create_txd_list(self):
        self.txd_list = {obj.name.lower(): i for i, obj in enumerate(self.gtxd)}

    def destroy_dff_list(self):
        self.dff_list.clear()

    def destroy_not_used(self):
        for obj in self.gdff:
            if not getattr(obj, 'in_use', False):
                obj.unload()
        for i in range(1, len(self.gtxd)):
            if not getattr(self.gtxd[i], 'in_use', False):
                if not (len(self.gtxd[i].name) == 7 and self.gtxd[i].name.lower() == 'radar.txd'):
                    self.gtxd[i].unload()

    def destroy_txd_list(self):
        self.txd_list.clear()

    def dff_exists(self, in_name: str) -> bool:
        in_name = in_name.lower()
        return in_name in self.archive_list or f"{in_name}.dff" in self.archive_list

    def get_dff_num(self, in_name: str) -> int:
        in_name = in_name.lower()
        if in_name in self.dff_list:
            return self.dff_list[in_name]
        for i, obj in enumerate(self.gdff):
            if obj.name.lower() == in_name:
                return i
        return -1

    def get_entry_num(self, in_name: str) -> int:
        return self.archive_list.get(in_name.lower(), -1)

    def get_txd_num(self, in_name: str) -> int:
        in_name = in_name.lower()
        if in_name == 'generic' and len(self.gtxd) > 0:
            return 0
        if in_name in self.txd_list:
            return self.txd_list[in_name]
        for i, obj in enumerate(self.gtxd):
            if obj.name.lower() == in_name:
                return i
        return -1

    def gl_draw(self, in_name: str, in_txd: int):
        index = self.get_dff_num(in_name)
        if index != -1:
            if not getattr(self.gdff[index], 'loaded', False):
                self.gdff[index].load_from_stream()
            self.gdff[index].gl_draw(in_txd)
            self.gdff[index].in_use = True

    def set_not_used(self):
        self.kill_not_used = True
        for obj in self.gdff:
            obj.in_use = False
        for obj in self.gtxd:
            obj.in_use = False

    def txd_exists(self, in_name: str) -> bool:
        in_name = in_name.lower()
        if in_name == 'generic':
            return True
        if in_name.endswith('.txd'):
            in_name = in_name[:-4]
        return in_name in self.archive_list or f"{in_name}.txd" in self.archive_list