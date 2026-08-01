#belongs in apps/components/Moomapper/depends/game_profiles.py -Version:1.6
# X-Seti-2026-08-01

import os
import json
from typing import List, Dict, Optional

# vers: 1.6
class GameProfile:
    def __init__(self, name: str = "", game_type: str = "", dat_path: str = "", img_path: str = ""):
        self.name = name
        self.game_type = game_type  # 'gta3', 'gta_vc', 'gta_sa'
        self.dat_path = dat_path
        self.img_path = img_path

    # vers: 1.6
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'game_type': self.game_type,
            'dat_path': self.dat_path,
            'img_path': self.img_path
        }

    # vers: 1.6
    @classmethod
    def from_dict(cls, data: Dict) -> 'GameProfile':
        profile = cls()
        profile.name = data.get('name', '')
        profile.game_type = data.get('game_type', '')
        profile.dat_path = data.get('dat_path', '')
        profile.img_path = data.get('img_path', '')
        return profile

# vers: 1.6
class GameProfileManager:
    def __init__(self):
        self.profiles: List[GameProfile] = []
        self.config_file = os.path.join(os.path.expanduser('~'), '.moomapper_profiles.json')
        self.load_profiles()

    # vers: 1.6
    def load_profiles(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.profiles = [GameProfile.from_dict(p) for p in data.get('profiles', [])]
            except Exception as e:
                print(f"Failed to load profiles: {e}")
                self.profiles = []

    # vers: 1.6
    def save_profiles(self):
        try:
            data = {'profiles': [p.to_dict() for p in self.profiles]}
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save profiles: {e}")

    # vers: 1.6
    def add_profile(self, profile: GameProfile):
        self.profiles.append(profile)
        self.save_profiles()

    # vers: 1.6
    def remove_profile(self, index: int):
        if 0 <= index < len(self.profiles):
            self.profiles.pop(index)
            self.save_profiles()

    # vers: 1.6
    def update_profile(self, index: int, profile: GameProfile):
        if 0 <= index < len(self.profiles):
            self.profiles[index] = profile
            self.save_profiles()

    # vers: 1.6
    def get_profile(self, index: int) -> Optional[GameProfile]:
        if 0 <= index < len(self.profiles):
            return self.profiles[index]
        return None

    # vers: 1.6
    def get_all_profiles(self) -> List[GameProfile]:
        return self.profiles