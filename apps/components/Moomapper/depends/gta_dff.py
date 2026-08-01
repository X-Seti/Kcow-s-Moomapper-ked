#belongs in apps/components/Moomapper/depends/gta_dff.py -Version:1.6
# X-Seti-2026-08-01

import struct
from typing import List, Dict, Any, Optional, BinaryIO

# vers: 1.6
RW_DATA = 1
RW_STRING = 2
RW_EXTENSION = 3
RW_TEXTURE = 6
RW_MATERIAL = 7
RW_MATERIAL_LIST = 8
RW_FRAME_LIST = 14
RW_GEOMETRY = 15
RW_CLUMP = 16
RW_ATOMIC = 20
RW_GEOMETRY_LIST = 26
RW_FRAME = 39056126
RW_MATERIAL_SPLIT = 1294

RW_OBJECT_VERTEX_UV = 4
RW_OBJECT_VERTEX_COLOR = 8
RW_OBJECT_VERTEX_NORMAL = 16

# vers: 1.6
class DFFFace:
    __slots__ = ['v2', 'v1', 'extra', 'v3']
    def __init__(self):
        self.v2: int = 0
        self.v1: int = 0
        self.extra: int = 0
        self.v3: int = 0

# vers: 1.6
class DFFFrame:
    __slots__ = ['name', 'matrix', 'coord', 'parent', 'other1', 'other2']
    def __init__(self):
        self.name: str = ""
        self.matrix: List[float] = [0.0] * 12
        self.coord: List[float] = [0.0, 0.0, 0.0]
        self.parent: int = 0
        self.other1: int = 0
        self.other2: int = 0

# vers: 1.6
class DFFHeader:
    __slots__ = ['start', 'back', 'tag', 'size', 'data1', 'data2']
    def __init__(self):
        self.start: int = 0
        self.back: int = 0
        self.tag: int = 0
        self.size: int = 0
        self.data1: int = 0
        self.data2: int = 0

# vers: 1.6
class DFFDataGeometryHeader:
    __slots__ = ['flags1', 'flags2', 'triangle_count', 'vertex_count', 'other_count']
    def __init__(self):
        self.flags1: int = 0
        self.flags2: int = 0
        self.triangle_count: int = 0
        self.vertex_count: int = 0
        self.other_count: int = 0

# vers: 1.6
class DFFLightHeaderGeometry:
    __slots__ = ['ambient', 'diffuse', 'specular']
    def __init__(self):
        self.ambient: float = 0.0
        self.diffuse: float = 0.0
        self.specular: float = 0.0

# vers: 1.6
class DFFExtraGeometry:
    __slots__ = ['u1', 'u2', 'u3', 'u4', 'other1', 'other2']
    def __init__(self):
        self.u1: float = 0.0
        self.u2: float = 0.0
        self.u3: float = 0.0
        self.u4: float = 0.0
        self.other1: int = 0
        self.other2: int = 0

# vers: 1.6
class DFFDataGeometry:
    __slots__ = ['header', 'light_header', 'color', 'uv', 'face', 'extra', 'vertex', 'normal']
    def __init__(self):
        self.header = DFFDataGeometryHeader()
        self.light_header = DFFLightHeaderGeometry()
        self.color: List[bytes] = []
        self.uv: List[List[float]] = []
        self.face: List[DFFFace] = []
        self.extra = DFFExtraGeometry()
        self.vertex: List[List[float]] = []
        self.normal: List[List[float]] = []

# vers: 1.6
class DFFDataMaterialList:
    __slots__ = ['material_count', 'other']
    def __init__(self):
        self.material_count: int = 0
        self.other: int = 0

# vers: 1.6
class DFFDataMaterial:
    __slots__ = ['other1', 'color', 'other3', 'texture_count', 'other5', 'other6', 'other7']
    def __init__(self):
        self.other1: int = 0
        self.color: bytes = b'\x00\x00\x00\x00\x00'
        self.other3: int = 0
        self.texture_count: int = 0
        self.other5: float = 1.0
        self.other6: float = 0.0
        self.other7: float = 1.0

# vers: 1.6
class DFFTexture:
    __slots__ = ['name', 'alpha', 'got_name']
    def __init__(self):
        self.name: str = ""
        self.alpha: str = ""
        self.got_name: bool = False

# vers: 1.6
class DFFMaterial:
    __slots__ = ['data', 'texture']
    def __init__(self):
        self.data = DFFDataMaterial()
        self.texture = DFFTexture()

# vers: 1.6
class DFFHeaderMaterialSplit:
    __slots__ = ['data', 'split_count', 'face_count']
    def __init__(self):
        self.data: int = 0
        self.split_count: int = 0
        self.face_count: int = 0

# vers: 1.6
class DFFSplit:
    __slots__ = ['face_index', 'material_index', 'index', 'normal']
    def __init__(self):
        self.face_index: int = 0
        self.material_index: int = 0
        self.index: List[int] = []
        self.normal: List[List[float]] = []

# vers: 1.6
class DFFMaterialSplit:
    __slots__ = ['header', 'split']
    def __init__(self):
        self.header = DFFHeaderMaterialSplit()
        self.split: List[DFFSplit] = []

# vers: 1.6
class DFFMaterialList:
    __slots__ = ['data', 'material', 'material_count']
    def __init__(self):
        self.data = DFFDataMaterialList()
        self.material: List[DFFMaterial] = []
        self.material_count: int = 0

# vers: 1.6
class DFFGeometry:
    __slots__ = ['data', 'material_list', 'material_split']
    def __init__(self):
        self.data = DFFDataGeometry()
        self.material_list = DFFMaterialList()
        self.material_split = DFFMaterialSplit()

# vers: 1.6
class DFFFrameList:
    __slots__ = ['frame_count', 'frame', 'frame_up_to']
    def __init__(self):
        self.frame_count: int = 0
        self.frame: List[DFFFrame] = []
        self.frame_up_to: int = 0

# vers: 1.6
class DFFGeometryList:
    __slots__ = ['geometry_count', 'geometry']
    def __init__(self):
        self.geometry_count: int = 0
        self.geometry: List[DFFGeometry] = []

# vers: 1.6
class DFFAtomic:
    __slots__ = ['frame_num', 'geometry_num', 'other1', 'other2']
    def __init__(self):
        self.frame_num: int = 0
        self.geometry_num: int = 0
        self.other1: int = 0
        self.other2: int = 0

# vers: 1.6
class DFFClump:
    __slots__ = ['object_count', 'frame_list', 'geometry_list', 'atomic', 'atomic_count']
    def __init__(self):
        self.object_count: int = 0
        self.frame_list = DFFFrameList()
        self.geometry_list = DFFGeometryList()
        self.atomic: List[DFFAtomic] = []
        self.atomic_count: int = 0

# vers: 1.6
class GTADffLoader:
    def __init__(self):
        self.clump: List[DFFClump] = []

    # vers: 1.6
    def reset_clump(self):
        self.clump = []

    # vers: 1.6
    def load_from_stream(self, stream: BinaryIO, in_start: int = 0, in_size: int = 0):
        self.reset_clump()
        main_header = DFFHeader()
        main_header.start = in_start + 16
        main_header.tag = 0
        main_header.size = in_size if in_size > 0 else self._get_stream_size(stream)
        main_header.data1 = 0
        main_header.data2 = 0
        main_header.back = in_start
        
        if in_start > 0:
            stream.seek(in_start)
            
        self._parse_headers(stream, main_header, 0, 16)

    # vers: 1.6
    def load_from_file(self, filename: str):
        with open(filename, 'rb') as f:
            self.load_from_stream(f)

    # vers: 1.6
    def _get_stream_size(self, stream: BinaryIO) -> int:
        current_pos = stream.tell()
        stream.seek(0, 2)
        size = stream.tell()
        stream.seek(current_pos)
        return size

    # vers: 1.6
    def _get_next_header(self, stream: BinaryIO) -> Optional[DFFHeader]:
        start = stream.tell()
        data = stream.read(12)
        if len(data) < 12:
            return None
        tag, size, data1, data2 = struct.unpack('<IIHH', data)
        header = DFFHeader()
        header.start = start
        header.tag = tag
        header.size = size
        header.data1 = data1
        header.data2 = data2
        header.back = stream.tell()
        return header

    # vers: 1.6
    def _parse_headers(self, stream: BinaryIO, parse_header: DFFHeader, level: int, parent: int):
        more_data = True
        while more_data:
            in_header = self._get_next_header(stream)
            if not in_header:
                break

            if in_header.tag == RW_CLUMP:
                self.clump.append(DFFClump())

            if in_header.tag == RW_ATOMIC:
                self.clump[-1].atomic_count += 1
                self.clump[-1].atomic.append(DFFAtomic())
            elif in_header.tag == RW_GEOMETRY:
                self.clump[-1].geometry_list.geometry_count += 1
                self.clump[-1].geometry_list.geometry.append(DFFGeometry())
            elif in_header.tag == RW_MATERIAL:
                geom = self.clump[-1].geometry_list.geometry[-1]
                geom.material_list.material_count += 1
                geom.material_list.material.append(DFFMaterial())

            if in_header.tag in (RW_TEXTURE, RW_MATERIAL_LIST, RW_MATERIAL, RW_CLUMP, 
                                 RW_FRAME_LIST, RW_GEOMETRY_LIST, RW_GEOMETRY, RW_ATOMIC):
                self._parse_headers(stream, in_header, level + 1, in_header.tag)
            elif in_header.tag == RW_MATERIAL_SPLIT:
                self._parse_material_split(stream, in_header, parent)
            elif in_header.tag == RW_DATA:
                self._parse_data(stream, in_header, parent)
            elif in_header.tag == RW_EXTENSION and in_header.size > 0:
                self._parse_headers(stream, in_header, level + 1, parent)
            elif in_header.tag in (RW_FRAME, RW_STRING):
                self._parse_string(stream, in_header, level + 1, parent)

            stream.seek(in_header.back + in_header.size)

            if stream.tell() >= (parse_header.back + parse_header.size) or in_header.tag == 0:
                more_data = False

    # vers: 1.6
    def _parse_data(self, stream: BinaryIO, parse_header: DFFHeader, parent: int):
        if parent == RW_CLUMP:
            self.clump[-1].object_count = struct.unpack('<I', stream.read(4))[0]
        elif parent == RW_MATERIAL_LIST:
            data = self.clump[-1].geometry_list.geometry[-1].material_list.data
            data.material_count, data.other = struct.unpack('<II', stream.read(8))
        elif parent == RW_MATERIAL:
            mat = self.clump[-1].geometry_list.geometry[-1].material_list.material[-1]
            mat.texture.got_name = False
            mat.data.other1, r, g, b, a, mat.data.other3, mat.data.texture_count, \
            mat.data.other5, mat.data.other6, mat.data.other7 = struct.unpack('<I5BIf3f', stream.read(32))
            mat.data.color = bytes([r, g, b, a, 0])
        elif parent == RW_GEOMETRY_LIST:
            self.clump[-1].geometry_list.geometry_count = struct.unpack('<I', stream.read(4))[0]
        elif parent == RW_ATOMIC:
            atomic = self.clump[-1].atomic[-1]
            atomic.frame_num, atomic.geometry_num, atomic.other1, atomic.other2 = struct.unpack('<IIII', stream.read(16))
        elif parent == RW_FRAME_LIST:
            frame_list = self.clump[-1].frame_list
            frame_list.frame_count = struct.unpack('<I', stream.read(4))[0]
            frame_list.frame = []
            frame_list.frame_up_to = 0
            for _ in range(frame_list.frame_count):
                frame = DFFFrame()
                frame.matrix = list(struct.unpack('<12f', stream.read(48)))
                frame.coord = list(struct.unpack('<3f', stream.read(12)))
                frame.parent, frame.other1, frame.other2 = struct.unpack('<iHH', stream.read(8))
                frame_list.frame.append(frame)
        elif parent == RW_GEOMETRY:
            geom = self.clump[-1].geometry_list.geometry[-1].data
            geom.header.flags1, geom.header.flags2, geom.header.triangle_count, \
            geom.header.vertex_count, geom.header.other_count = struct.unpack('<HHIII', stream.read(16))
            
            if parse_header.data2 != 4099:
                geom.light_header.ambient, geom.light_header.diffuse, geom.light_header.specular = struct.unpack('<3f', stream.read(12))
            
            if (geom.header.flags1 & RW_OBJECT_VERTEX_COLOR) == RW_OBJECT_VERTEX_COLOR:
                geom.color = [stream.read(4) for _ in range(geom.header.vertex_count)]
            
            if (geom.header.flags1 & RW_OBJECT_VERTEX_UV) == RW_OBJECT_VERTEX_UV:
                geom.uv = [list(struct.unpack('<2f', stream.read(8))) for _ in range(geom.header.vertex_count)]
            
            geom.face = []
            for _ in range(geom.header.triangle_count):
                f = DFFFace()
                f.v2, f.v1, f.extra, f.v3 = struct.unpack('<HHHH', stream.read(8))
                geom.face.append(f)
            
            geom.extra.u1, geom.extra.u2, geom.extra.u3, geom.extra.u4, \
            geom.extra.other1, geom.extra.other2 = struct.unpack('<4fII', stream.read(24))
            
            geom.vertex = [list(struct.unpack('<3f', stream.read(12))) for _ in range(geom.header.vertex_count)]
            
            if (geom.header.flags1 & RW_OBJECT_VERTEX_NORMAL) == RW_OBJECT_VERTEX_NORMAL:
                geom.normal = [list(struct.unpack('<3f', stream.read(12))) for _ in range(geom.header.vertex_count)]
            elif geom.header.vertex_count > 0 and (geom.header.triangle_count % 3 == 0):
                geom.normal = [self._calc_face_normal(geom.vertex[f.v1], geom.vertex[f.v2], geom.vertex[f.v3]) for f in geom.face]

    # vers: 1.6
    def _parse_material_split(self, stream: BinaryIO, parse_header: DFFHeader, parent: int):
        geom = self.clump[-1].geometry_list.geometry[-1]
        header = geom.material_split.header
        header.data, header.split_count, header.face_count = struct.unpack('<III', stream.read(12))
        
        geom.material_split.split = []
        for _ in range(header.split_count):
            split = DFFSplit()
            split.face_index, split.material_index = struct.unpack('<II', stream.read(8))
            split.index = list(struct.unpack(f'<{split.face_index}I', stream.read(4 * split.face_index)))
            geom.material_split.split.append(split)

    # vers: 1.6
    def _parse_string(self, stream: BinaryIO, parse_header: DFFHeader, level: int, parent: int):
        buf = stream.read(parse_header.size).decode('ascii', errors='ignore').strip('\x00').strip()
        if parent == RW_TEXTURE:
            tex = self.clump[-1].geometry_list.geometry[-1].material_list.material[-1].texture
            if tex.got_name:
                tex.alpha = buf
            else:
                tex.name = buf
            tex.got_name = True
        elif parent == RW_FRAME_LIST:
            self.clump[-1].frame_list.frame[self.clump[-1].frame_list.frame_up_to].name = buf
            self.clump[-1].frame_list.frame_up_to += 1

    # vers: 1.6
    def _calc_face_normal(self, p1: List[float], p2: List[float], p3: List[float]) -> List[float]:
        a = [p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]]
        b = [p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]]
        nx = a[1]*b[2] - a[2]*b[1]
        ny = a[2]*b[0] - a[0]*b[2]
        nz = a[0]*b[1] - a[1]*b[0]
        
        length = (nx*nx + ny*ny + nz*nz) ** 0.5
        if length == 0:
            length = 1.0
        return [nx/length, ny/length, nz/length]

# vers: 1.6
class GTADff(GTADffLoader):
    def __init__(self, stream: Optional[BinaryIO] = None, name: str = "", in_start: int = 0, in_size: int = 0):
        super().__init__()
        self.name = name
        self.loaded = False
        self.in_use = False
        self.stream = stream
        self.f_start = in_start
        self.f_size = in_size
        
        if stream and not False: # Placeholder for GTA_MODEL_LOAD_DEMAND
            self.load_from_stream()

    # vers: 1.6
    def load_from_stream(self):
        self.loaded = True
        super().load_from_stream(self.stream, self.f_start, self.f_size)

    # vers: 1.6
    def unload(self):
        self.loaded = False
        self.reset_clump()