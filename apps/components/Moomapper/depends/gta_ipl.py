#belongs in apps/components/Moomapper/depends/gta_ipl.py -Version:1.6
# X-Seti-2026-08-01

import os
from typing import List, Dict, Optional

# vers: 1.6
class IPLInstance:
    __slots__ = ['id', 'model_name', 'interior', 'position', 'quaternion', 'lod']
    def __init__(self):
        self.id: int = 0
        self.model_name: str = ""
        self.interior: int = 0
        self.position: List[float] = [0.0, 0.0, 0.0]
        self.quaternion: List[float] = [0.0, 0.0, 0.0, 1.0]
        self.lod: int = -1

# vers: 1.6
class IPLCullZone:
    __slots__ = ['center', 'unknown1', 'unknown2', 'unknown3', 'flags']
    def __init__(self):
        self.center: List[float] = [0.0, 0.0, 0.0]
        self.unknown1: float = 0.0
        self.unknown2: float = 0.0
        self.unknown3: float = 0.0
        self.flags: int = 0

# vers: 1.6
class IPLZone:
    __slots__ = ['name', 'gxt_name', 'x1', 'y1', 'x2', 'y2']
    def __init__(self):
        self.name: str = ""
        self.gxt_name: str = ""
        self.x1: float = 0.0
        self.y1: float = 0.0
        self.x2: float = 0.0
        self.y2: float = 0.0

# vers: 1.6
class IPLGarage:
    __slots__ = ['position', 'size', 'type']
    def __init__(self):
        self.position: List[float] = [0.0, 0.0, 0.0]
        self.size: List[float] = [0.0, 0.0, 0.0]
        self.type: int = 0

# vers: 1.6
class IPLEntrance:
    __slots__ = ['entrance_pos', 'exit_pos', 'enter_angle', 'interior_id', 'flags', 'name', 'sky_color', 'time_on', 'time_off']
    def __init__(self):
        self.entrance_pos: List[float] = [0.0, 0.0, 0.0]
        self.exit_pos: List[float] = [0.0, 0.0, 0.0]
        self.enter_angle: float = 0.0
        self.interior_id: int = 0
        self.flags: int = 0
        self.name: str = ""
        self.sky_color: int = 0
        self.time_on: int = 0
        self.time_off: int = 0

# vers: 1.6
class IPLPickup:
    __slots__ = ['id', 'position', 'weapon_type']
    def __init__(self):
        self.id: int = 0
        self.position: List[float] = [0.0, 0.0, 0.0]
        self.weapon_type: int = 0

# vers: 1.6
class IPLJump:
    __slots__ = ['start', 'end', 'camera', 'reward']
    def __init__(self):
        self.start: List[float] = [0.0, 0.0, 0.0]
        self.end: List[float] = [0.0, 0.0, 0.0]
        self.camera: List[float] = [0.0, 0.0, 0.0]
        self.reward: int = 0

# vers: 1.6
class GTAIPL:
    def __init__(self, filename: str = ""):
        self.filename = filename
        self.loaded = False
        
        self.instances: List[IPLInstance] = []
        self.cull_zones: List[IPLCullZone] = []
        self.zones: List[IPLZone] = []
        self.garages: List[IPLGarage] = []
        self.entrances: List[IPLEntrance] = []
        self.pickups: List[IPLPickup] = []
        self.jumps: List[IPLJump] = []
        
        self.instance_list: Dict[str, List[int]] = {}
        
        if filename and os.path.exists(filename):
            self.load_from_file(filename)

    # vers: 1.6
    def load_from_file(self, filename: str):
        self.filename = filename
        self.loaded = True
        
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        self._parse_lines(lines)

    # vers: 1.6
    def unload(self):
        self.loaded = False
        self.instances.clear()
        self.cull_zones.clear()
        self.zones.clear()
        self.garages.clear()
        self.entrances.clear()
        self.pickups.clear()
        self.jumps.clear()
        self.instance_list.clear()

    # vers: 1.6
    def _parse_lines(self, lines: List[str]):
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('end'):
                current_section = ""
                continue
            
            if line.startswith('inst'):
                current_section = 'inst'
                continue
            elif line.startswith('cull'):
                current_section = 'cull'
                continue
            elif line.startswith('zone'):
                current_section = 'zone'
                continue
            elif line.startswith('grge'):
                current_section = 'grge'
                continue
            elif line.startswith('enex'):
                current_section = 'enex'
                continue
            elif line.startswith('pick'):
                current_section = 'pick'
                continue
            elif line.startswith('jump'):
                current_section = 'jump'
                continue
            
            if current_section == 'inst':
                self._parse_instance(line)
            elif current_section == 'cull':
                self._parse_cull_zone(line)
            elif current_section == 'zone':
                self._parse_zone(line)
            elif current_section == 'grge':
                self._parse_garage(line)
            elif current_section == 'enex':
                self._parse_entrance(line)
            elif current_section == 'pick':
                self._parse_pickup(line)
            elif current_section == 'jump':
                self._parse_jump(line)

    # vers: 1.6
    def _parse_instance(self, line: str):
        parts = line.split(',')
        if len(parts) >= 10:
            inst = IPLInstance()
            inst.id = int(parts[0].strip())
            inst.model_name = parts[1].strip()
            inst.interior = int(parts[2].strip())
            inst.position = [float(parts[3].strip()), float(parts[4].strip()), float(parts[5].strip())]
            inst.quaternion = [float(parts[6].strip()), float(parts[7].strip()), float(parts[8].strip()), float(parts[9].strip())]
            if len(parts) > 10:
                inst.lod = int(parts[10].strip())
            self.instances.append(inst)
            
            if inst.model_name.lower() not in self.instance_list:
                self.instance_list[inst.model_name.lower()] = []
            self.instance_list[inst.model_name.lower()].append(len(self.instances) - 1)

    # vers: 1.6
    def _parse_cull_zone(self, line: str):
        parts = line.split(',')
        if len(parts) >= 6:
            zone = IPLCullZone()
            zone.center = [float(parts[0].strip()), float(parts[1].strip()), float(parts[2].strip())]
            zone.unknown1 = float(parts[3].strip())
            zone.unknown2 = float(parts[4].strip())
            zone.unknown3 = float(parts[5].strip())
            if len(parts) > 6:
                zone.flags = int(parts[6].strip())
            self.cull_zones.append(zone)

    # vers: 1.6
    def _parse_zone(self, line: str):
        parts = line.split(',')
        if len(parts) >= 6:
            zone = IPLZone()
            zone.name = parts[0].strip()
            zone.gxt_name = parts[1].strip()
            zone.x1 = float(parts[2].strip())
            zone.y1 = float(parts[3].strip())
            zone.x2 = float(parts[4].strip())
            zone.y2 = float(parts[5].strip())
            self.zones.append(zone)

    # vers: 1.6
    def _parse_garage(self, line: str):
        parts = line.split(',')
        if len(parts) >= 7:
            garage = IPLGarage()
            garage.position = [float(parts[0].strip()), float(parts[1].strip()), float(parts[2].strip())]
            garage.size = [float(parts[3].strip()), float(parts[4].strip()), float(parts[5].strip())]
            garage.type = int(parts[6].strip())
            self.garages.append(garage)

    # vers: 1.6
    def _parse_entrance(self, line: str):
        parts = line.split(',')
        if len(parts) >= 10:
            entrance = IPLEntrance()
            entrance.entrance_pos = [float(parts[0].strip()), float(parts[1].strip()), float(parts[2].strip())]
            entrance.enter_angle = float(parts[3].strip())
            entrance.interior_id = int(parts[4].strip())
            entrance.flags = int(parts[5].strip())
            entrance.name = parts[6].strip()
            entrance.sky_color = int(parts[7].strip())
            entrance.time_on = int(parts[8].strip())
            entrance.time_off = int(parts[9].strip())
            if len(parts) >= 13:
                entrance.exit_pos = [float(parts[10].strip()), float(parts[11].strip()), float(parts[12].strip())]
            self.entrances.append(entrance)

    # vers: 1.6
    def _parse_pickup(self, line: str):
        parts = line.split(',')
        if len(parts) >= 5:
            pickup = IPLPickup()
            pickup.id = int(parts[0].strip())
            pickup.position = [float(parts[1].strip()), float(parts[2].strip()), float(parts[3].strip())]
            pickup.weapon_type = int(parts[4].strip())
            self.pickups.append(pickup)

    # vers: 1.6
    def _parse_jump(self, line: str):
        parts = line.split(',')
        if len(parts) >= 10:
            jump = IPLJump()
            jump.start = [float(parts[0].strip()), float(parts[1].strip()), float(parts[2].strip())]
            jump.end = [float(parts[3].strip()), float(parts[4].strip()), float(parts[5].strip())]
            jump.camera = [float(parts[6].strip()), float(parts[7].strip()), float(parts[8].strip())]
            jump.reward = int(parts[9].strip())
            self.jumps.append(jump)

    # vers: 1.6
    def get_instances_by_model(self, model_name: str) -> List[IPLInstance]:
        indices = self.instance_list.get(model_name.lower(), [])
        return [self.instances[i] for i in indices]

    # vers: 1.6
    def get_instance_count(self) -> int:
        return len(self.instances)