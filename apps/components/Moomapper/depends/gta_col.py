#belongs in apps/components/Moomapper/depends/gta_col.py -Version:1.6
# X-Seti-2026-08-01

import struct
from typing import List, Optional, BinaryIO

# vers: 1.6
class ColBox:
    __slots__ = ['min_coord', 'max_coord', 'material', 'piece']
    def __init__(self):
        self.min_coord: List[float] = [0.0, 0.0, 0.0]
        self.max_coord: List[float] = [0.0, 0.0, 0.0]
        self.material: int = 0
        self.piece: int = 0

# vers: 1.6
class ColFace:
    __slots__ = ['v1', 'v2', 'v3', 'material', 'piece']
    def __init__(self):
        self.v1: int = 0
        self.v2: int = 0
        self.v3: int = 0
        self.material: int = 0
        self.piece: int = 0

# vers: 1.6
class ColSphere:
    __slots__ = ['center', 'radius', 'material', 'piece']
    def __init__(self):
        self.center: List[float] = [0.0, 0.0, 0.0]
        self.radius: float = 0.0
        self.material: int = 0
        self.piece: int = 0

# vers: 1.6
class ColVertex:
    __slots__ = ['coord']
    def __init__(self):
        self.coord: List[float] = [0.0, 0.0, 0.0]

# vers: 1.6
class GTACol:
    def __init__(self, stream: Optional[BinaryIO] = None, name: str = "", in_start: int = 0, in_size: int = 0):
        self.name = name
        self.loaded = False
        self.in_use = False
        self.stream = stream
        self.f_start = in_start
        self.f_size = in_size
        
        self.model_name: str = ""
        self.spheres: List[ColSphere] = []
        self.boxes: List[ColBox] = []
        self.vertices: List[ColVertex] = []
        self.faces: List[ColFace] = []
        
        if stream and in_size > 0:
            self.load_from_stream()

    # vers: 1.6
    def load_from_file(self, filename: str):
        with open(filename, 'rb') as f:
            self.load_from_stream(f, 0, 0)

    # vers: 1.6
    def load_from_stream(self, stream: Optional[BinaryIO] = None, in_start: int = 0, in_size: int = 0):
        if stream:
            self.stream = stream
            self.f_start = in_start
            self.f_size = in_size
            
        if not self.stream:
            return
            
        self.loaded = True
        self.stream.seek(self.f_start)
        
        magic = self.stream.read(4).decode('ascii', errors='ignore')
        
        if magic == 'COLL':
            self._parse_coll()
        elif magic in ('COL2', 'COL3'):
            self._parse_col2()
        else:
            self.loaded = False

    # vers: 1.6
    def unload(self):
        self.loaded = False
        self.spheres.clear()
        self.boxes.clear()
        self.vertices.clear()
        self.faces.clear()

    # vers: 1.6
    def _parse_col2(self):
        self.stream.read(4) # skip size
        self.model_name = self.stream.read(64).split(b'\x00')[0].decode('ascii', errors='ignore').strip()
        
        sph_count = struct.unpack('<H', self.stream.read(2))[0]
        self.stream.read(2) # unknown
        self._read_spheres(sph_count)
        
        line_count = struct.unpack('<H', self.stream.read(2))[0]
        self.stream.read(2)
        self.stream.read(line_count * 24) 
        
        box_count = struct.unpack('<H', self.stream.read(2))[0]
        self.stream.read(2)
        self._read_boxes(box_count)
        
        vert_count = struct.unpack('<H', self.stream.read(2))[0]
        self.stream.read(2) 
        self._read_vertices(vert_count)
        
        face_count = struct.unpack('<H', self.stream.read(2))[0]
        self.stream.read(6) 
        self._read_faces(face_count)

    # vers: 1.6
    def _parse_coll(self):
        self.stream.read(4) # skip size
        self.model_name = self.stream.read(24).split(b'\x00')[0].decode('ascii', errors='ignore').strip()
        
        sph_count = struct.unpack('<H', self.stream.read(2))[0]
        self._read_spheres(sph_count)
        
        line_count = struct.unpack('<H', self.stream.read(2))[0]
        self.stream.read(line_count * 24)
        
        box_count = struct.unpack('<H', self.stream.read(2))[0]
        self._read_boxes(box_count)
        
        vert_count = struct.unpack('<H', self.stream.read(2))[0]
        self._read_vertices(vert_count)
        
        face_count = struct.unpack('<H', self.stream.read(2))[0]
        self._read_faces(face_count)

    # vers: 1.6
    def _read_boxes(self, count: int):
        for _ in range(count):
            box = ColBox()
            box.min_coord = list(struct.unpack('<3f', self.stream.read(12)))
            box.max_coord = list(struct.unpack('<3f', self.stream.read(12)))
            box.material, box.piece = struct.unpack('<BB', self.stream.read(2))
            self.stream.read(2) # padding
            self.boxes.append(box)

    # vers: 1.6
    def _read_faces(self, count: int):
        for _ in range(count):
            face = ColFace()
            face.v1, face.v2, face.v3 = struct.unpack('<HHH', self.stream.read(6))
            face.material, face.piece = struct.unpack('<BB', self.stream.read(2))
            self.faces.append(face)

    # vers: 1.6
    def _read_spheres(self, count: int):
        for _ in range(count):
            sph = ColSphere()
            sph.radius = struct.unpack('<f', self.stream.read(4))[0]
            sph.center = list(struct.unpack('<3f', self.stream.read(12)))
            sph.material, sph.piece = struct.unpack('<BB', self.stream.read(2))
            self.stream.read(2) # padding
            self.spheres.append(sph)

    # vers: 1.6
    def _read_vertices(self, count: int):
        for _ in range(count):
            vert = ColVertex()
            vert.coord = list(struct.unpack('<3f', self.stream.read(12)))
            self.vertices.append(vert)