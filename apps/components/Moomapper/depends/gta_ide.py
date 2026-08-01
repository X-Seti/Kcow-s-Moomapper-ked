#belongs in apps/components/Moomapper/depends/gta_ide.py -Version:1.6
# X-Seti-2026-08-01

import os
from typing import List, Dict, Optional

# vers: 1.6
class IDEObject:
    __slots__ = ['id', 'model_name', 'txd_name', 'render_distance', 'flags', 'object_type']
    def __init__(self):
        self.id: int = 0
        self.model_name: str = ""
        self.txd_name: str = ""
        self.render_distance: float = 0.0
        self.flags: int = 0
        self.object_type: int = 0

# vers: 1.6
class IDETimedObject:
    __slots__ = ['id', 'model_name', 'txd_name', 'render_distance', 'flags', 'time_on', 'time_off']
    def __init__(self):
        self.id: int = 0
        self.model_name: str = ""
        self.txd_name: str = ""
        self.render_distance: float = 0.0
        self.flags: int = 0
        self.time_on: int = 0
        self.time_off: int = 0

# vers: 1.6
class IDEAnimObject:
    __slots__ = ['id', 'model_name', 'txd_name', 'render_distance', 'flags', 'anim_name', 'object_type']
    def __init__(self):
        self.id: int = 0
        self.model_name: str = ""
        self.txd_name: str = ""
        self.render_distance: float = 0.0
        self.flags: int = 0
        self.anim_name: str = ""
        self.object_type: int = 0

# vers: 1.6
class IDEVehicle:
    __slots__ = ['id', 'model_name', 'txd_name', 'type', 'handling_id', 'game_name', 'preferred_radio', 'class_name', 'flags', 'rules']
    def __init__(self):
        self.id: int = 0
        self.model_name: str = ""
        self.txd_name: str = ""
        self.type: str = ""
        self.handling_id: str = ""
        self.game_name: str = ""
        self.preferred_radio: str = ""
        self.class_name: str = ""
        self.flags: int = 0
        self.rules: str = ""

# vers: 1.6
class IDEPedestrian:
    __slots__ = ['type', 'id', 'model_name', 'txd_name', 'ped_stats', 'anim_group', 'cars_can_drive', 'anim_file']
    def __init__(self):
        self.type: int = 0
        self.id: int = 0
        self.model_name: str = ""
        self.txd_name: str = ""
        self.ped_stats: str = ""
        self.anim_group: str = ""
        self.cars_can_drive: int = 0
        self.anim_file: str = ""

# vers: 1.6
class IDE2DFX:
    __slots__ = ['id', 'model_name', 'fx_type', 'position', 'effect_data']
    def __init__(self):
        self.id: int = 0
        self.model_name: str = ""
        self.fx_type: int = 0
        self.position: List[float] = [0.0, 0.0, 0.0]
        self.effect_data: str = ""

# vers: 1.6
class GTAIDE:
    def __init__(self, filename: str = ""):
        self.filename = filename
        self.loaded = False
        
        self.objects: List[IDEObject] = []
        self.timed_objects: List[IDETimedObject] = []
        self.anim_objects: List[IDEAnimObject] = []
        self.vehicles: List[IDEVehicle] = []
        self.peds: List[IDEPedestrian] = []
        self.effects_2d: List[IDE2DFX] = []
        
        self.object_list: Dict[str, int] = {}
        self.vehicle_list: Dict[str, int] = {}
        self.ped_list: Dict[str, int] = {}
        
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
        self.objects.clear()
        self.timed_objects.clear()
        self.anim_objects.clear()
        self.vehicles.clear()
        self.peds.clear()
        self.effects_2d.clear()
        self.object_list.clear()
        self.vehicle_list.clear()
        self.ped_list.clear()

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
            
            if line.startswith('objs'):
                current_section = 'objs'
                continue
            elif line.startswith('tobj'):
                current_section = 'tobj'
                continue
            elif line.startswith('anim'):
                current_section = 'anim'
                continue
            elif line.startswith('cars'):
                current_section = 'cars'
                continue
            elif line.startswith('peds'):
                current_section = 'peds'
                continue
            elif line.startswith('2dfx'):
                current_section = '2dfx'
                continue
            
            if current_section == 'objs':
                self._parse_object(line)
            elif current_section == 'tobj':
                self._parse_timed_object(line)
            elif current_section == 'anim':
                self._parse_anim_object(line)
            elif current_section == 'cars':
                self._parse_vehicle(line)
            elif current_section == 'peds':
                self._parse_pedestrian(line)
            elif current_section == '2dfx':
                self._parse_2dfx(line)

    # vers: 1.6
    def _parse_object(self, line: str):
        parts = line.split(',')
        if len(parts) >= 5:
            obj = IDEObject()
            obj.id = int(parts[0].strip())
            obj.model_name = parts[1].strip()
            obj.txd_name = parts[2].strip()
            obj.render_distance = float(parts[3].strip())
            obj.flags = int(parts[4].strip())
            if len(parts) > 5:
                obj.object_type = int(parts[5].strip())
            self.objects.append(obj)
            self.object_list[obj.model_name.lower()] = len(self.objects) - 1

    # vers: 1.6
    def _parse_timed_object(self, line: str):
        parts = line.split(',')
        if len(parts) >= 7:
            obj = IDETimedObject()
            obj.id = int(parts[0].strip())
            obj.model_name = parts[1].strip()
            obj.txd_name = parts[2].strip()
            obj.render_distance = float(parts[3].strip())
            obj.flags = int(parts[4].strip())
            obj.time_on = int(parts[5].strip())
            obj.time_off = int(parts[6].strip())
            self.timed_objects.append(obj)

    # vers: 1.6
    def _parse_anim_object(self, line: str):
        parts = line.split(',')
        if len(parts) >= 6:
            obj = IDEAnimObject()
            obj.id = int(parts[0].strip())
            obj.model_name = parts[1].strip()
            obj.txd_name = parts[2].strip()
            obj.render_distance = float(parts[3].strip())
            obj.flags = int(parts[4].strip())
            obj.anim_name = parts[5].strip()
            if len(parts) > 6:
                obj.object_type = int(parts[6].strip())
            self.anim_objects.append(obj)

    # vers: 1.6
    def _parse_vehicle(self, line: str):
        parts = line.split(',')
        if len(parts) >= 9:
            veh = IDEVehicle()
            veh.id = int(parts[0].strip())
            veh.model_name = parts[1].strip()
            veh.txd_name = parts[2].strip()
            veh.type = parts[3].strip()
            veh.handling_id = parts[4].strip()
            veh.game_name = parts[5].strip()
            veh.preferred_radio = parts[6].strip()
            veh.class_name = parts[7].strip()
            veh.flags = int(parts[8].strip())
            if len(parts) > 9:
                veh.rules = parts[9].strip()
            self.vehicles.append(veh)
            self.vehicle_list[veh.model_name.lower()] = len(self.vehicles) - 1

    # vers: 1.6
    def _parse_pedestrian(self, line: str):
        parts = line.split(',')
        if len(parts) >= 6:
            ped = IDEPedestrian()
            ped.type = int(parts[0].strip())
            ped.id = int(parts[1].strip())
            ped.model_name = parts[2].strip()
            ped.txd_name = parts[3].strip()
            ped.ped_stats = parts[4].strip()
            ped.anim_group = parts[5].strip()
            if len(parts) > 6:
                ped.cars_can_drive = int(parts[6].strip())
            if len(parts) > 7:
                ped.anim_file = parts[7].strip()
            self.peds.append(ped)
            self.ped_list[ped.model_name.lower()] = len(self.peds) - 1

    # vers: 1.6
    def _parse_2dfx(self, line: str):
        parts = line.split(',')
        if len(parts) >= 6:
            fx = IDE2DFX()
            fx.id = int(parts[0].strip())
            fx.model_name = parts[1].strip()
            fx.position = [float(parts[2].strip()), float(parts[3].strip()), float(parts[4].strip())]
            fx.fx_type = int(parts[5].strip())
            if len(parts) > 6:
                fx.effect_data = parts[6].strip()
            self.effects_2d.append(fx)

    # vers: 1.6
    def get_object_by_name(self, name: str) -> Optional[IDEObject]:
        idx = self.object_list.get(name.lower(), -1)
        return self.objects[idx] if idx != -1 else None

    # vers: 1.6
    def get_vehicle_by_name(self, name: str) -> Optional[IDEVehicle]:
        idx = self.vehicle_list.get(name.lower(), -1)
        return self.vehicles[idx] if idx != -1 else None

    # vers: 1.6
    def get_ped_by_name(self, name: str) -> Optional[IDEPedestrian]:
        idx = self.ped_list.get(name.lower(), -1)
        return self.peds[idx] if idx != -1 else None