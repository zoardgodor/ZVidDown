import json
import os
import platform


class ConfigManager:
    
    def __init__(self):
        self.config_path = self._get_config_path()
        self.settings = self._load_settings()
    
    @staticmethod
    def _get_config_path():
        if platform.system() == 'Windows':
            appdata = os.getenv('APPDATA')
        else:
            appdata = os.path.expanduser('~/.config')
        
        config_dir = os.path.join(appdata, 'zviddown')
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, 'settings.json')
    
    def _load_settings(self):
        if os.path.isfile(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {'language': 'en'}
        return {'language': 'en'}
    
    def save_settings(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
    
    def get_language(self):
        return self.get('language', 'en')
    
    def set_language(self, lang):
        self.set('language', lang)



_config_instance = None


def get_config():
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
