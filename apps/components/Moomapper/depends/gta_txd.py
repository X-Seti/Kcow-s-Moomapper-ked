#belongs in apps/components/Moomapper/depends/gta_txd.py -Version:1.6
# X-Seti-2026-08-01

import struct
from typing import List, Dict, Optional, BinaryIO

# OpenGL constants (preserved from original)
GL_TEXTURE_2D = 0x0DE1
GL_RGBA4 = 0x8056
GL_COMPRESSED_RGB_S3TC_DXT1_EXT = 0x83F0
GL_COMPRESSED_RGBA_S3TC_DXT1_EXT = 0x83F1
GL_COMPRESSED_RGBA_S3TC_DXT3_EXT = 0x83F2
GL_COMPRESSED_RGBA_S3TC_DXT5_EXT = 0x83F3
GL_TEXTURE_ENV = 0x2200
GL_TEXTURE_ENV_MODE = 0x2200
GL_MODULATE = 0x2100
GL_TEXTURE_MAG_FILTER = 0x2800
GL_TEXTURE_MIN_FILTER = 0x2801
GL_LINEAR = 0x2601
GL_RGBA = 0x1908
GL_UNSIGNED_BYTE = 0x1401

# vers: 1.6
class Texture:
    __slots__ = [
        'name', 'alpha_name', 'width', 'height', 'alpha', 
        'mipmaps', 'other', 'compression', 'depth', 'data_size', 'data', 'palette'
    ]
    def __init__(self):
        self.name: str = ""
        self.alpha_name: str = ""
        self.width: int = 0
        self.height: int = 0
        self.alpha: int = 0
        self.mipmaps: int = 0
        self.other: int = 0
        self.compression: int = 0
        self.depth: int = 0
        self.data_size: int = 0
        self.data: bytes = b""
        self.palette: bytes = b""

# vers: 1.6
class GTATxd:
    def __init__(self, stream: Optional[BinaryIO] = None, name: str = "", in_start: int = 0, in_size: int = 0):
        self.name = name
        self.loaded = False
        self.in_use = False
        self.stream = stream
        self.f_start = in_start
        self.f_size = in_size
        
        self.image: List[Texture] = []
        self.image_texture: List[int] = []
        self.image_count: int = 0
        self.image_name_list: Dict[str, int] = {}
        self.image_alpha_list: Dict[str, int] = {}
        
        if stream and in_size > 0:
            self.load_from_stream()

    # vers: 1.6
    def _make_8_fake_32(self, tex: Texture):
        newbuf = bytearray(tex.width * tex.height * 4)
        pal = tex.palette[:1024]
        
        for i in range(tex.data_size):
            b = tex.data[i]
            pal_offset = b * 4
            newbuf[i*4 : i*4+4] = pal[pal_offset : pal_offset+4]
            
        tex.data_size = tex.width * tex.height * 4
        tex.data = bytes(newbuf)

    # vers: 1.6
    def _parse_file(self, f_data: bytes):
        if not f_data:
            return

        f_file_pos = 24
        data_type = struct.unpack_from('<H', f_data, f_file_pos + 4)[0]
        
        if data_type == 21:
            self.image_count = struct.unpack_from('<H', f_data, f_file_pos)[0]
        else:
            self.image_count = 0
            
        self.image = [Texture() for _ in range(self.image_count)]
        self.image_texture = [0] * self.image_count
        self.image_name_list.clear()
        self.image_alpha_list.clear()

        f_file_pos += 4

        if self.image_count > 0:
            if struct.unpack_from('<I', f_data, f_file_pos + 24)[0] == 3298128:
                self.image_count = 0
                self.image = []
                self.image_texture = []
            else:
                for i in range(self.image_count):
                    f_file_pos += 12
                    file_ver = struct.unpack_from('<I', f_data, f_file_pos + 12)[0]
                    f_file_pos += 20

                    name_bytes = f_data[f_file_pos:f_file_pos+32]
                    self.image[i].name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
                    f_file_pos += 32
                    self.image_name_list[self.image[i].name.lower()] = i

                    alpha_bytes = f_data[f_file_pos:f_file_pos+32]
                    self.image[i].alpha_name = alpha_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
                    f_file_pos += 32 + 4
                    self.image_alpha_list[self.image[i].alpha_name.lower()] = i

                    self.image[i].alpha = struct.unpack_from('<I', f_data, f_file_pos)[0]
                    self.image[i].width = struct.unpack_from('<H', f_data, f_file_pos + 4)[0]
                    self.image[i].height = struct.unpack_from('<H', f_data, f_file_pos + 6)[0]
                    self.image[i].depth = struct.unpack_from('<B', f_data, f_file_pos + 8)[0]
                    self.image[i].mipmaps = struct.unpack_from('<B', f_data, f_file_pos + 9)[0]
                    self.image[i].other = struct.unpack_from('<B', f_data, f_file_pos + 10)[0]
                    self.image[i].compression = struct.unpack_from('<B', f_data, f_file_pos + 11)[0]
                    f_file_pos += 12

                    for j in range(self.image[i].mipmaps):
                        if self.image[i].depth == 8:
                            self.image[i].palette = f_data[f_file_pos:f_file_pos+1024]
                            f_file_pos += 1024

                        self.image[i].data_size = struct.unpack_from('<I', f_data, f_file_pos)[0]
                        f_file_pos += 4

                        self.image[i].data = f_data[f_file_pos:f_file_pos+self.image[i].data_size]
                        f_file_pos += self.image[i].data_size

                        w = self.image[i].width // (1 << j)
                        h = self.image[i].height // (1 << j)
                        if w == 0: w = 1
                        if h == 0: h = 1

                        if self.image[i].alpha == 827611204:
                            pass # glCompressedTexImage2DARB placeholder
                        elif self.image[i].alpha == 861165636:
                            pass # glCompressedTexImage2DARB placeholder
                        else:
                            if self.image[i].depth == 8:
                                self._make_8_fake_32(self.image[i])
                            elif self.image[i].depth == 16:
                                pass # Compression handling placeholder
                            elif self.image[i].depth == 32:
                                if file_ver == 9:
                                    self.image[i].alpha = self.image[i].compression # San Andreas problems
                                self.image[i].data = self._swap_rgba(self.image[i].data, w * h)

                    if i < self.image_count - 1:
                        if struct.unpack_from('<H', f_data, f_file_pos)[0] != 3:
                            if struct.unpack_from('<H', f_data, f_file_pos + 2)[0] == 3:
                                f_file_pos += 2
                            elif struct.unpack_from('<H', f_data, f_file_pos - 2)[0] == 3:
                                f_file_pos -= 2
                    f_file_pos += 12

    # vers: 1.6
    def _swap_rgba(self, data: bytes, size: int) -> bytes:
        data_list = bytearray(data)
        for i in range(0, size * 4, 4):
            data_list[i], data_list[i+2] = data_list[i+2], data_list[i]
        return bytes(data_list)

    # vers: 1.6
    def load_from_stream(self):
        self.loaded = True
        self.stream.seek(self.f_start)
        f_data = self.stream.read(self.f_size)
        self._parse_file(f_data)

    # vers: 1.6
    def unload(self):
        self.loaded = False
        self.image_count = 0
        self.image = []
        self.image_texture = []
        self.image_name_list.clear()
        self.image_alpha_list.clear()