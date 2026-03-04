import os
import sys
import subprocess
import platform


class FFToolsManager:
    
    _FFT_TOOLS = {
        'ffmpeg': 'ffmpeg.exe' if os.name == 'nt' else 'ffmpeg',
        'ffprobe': 'ffprobe.exe' if os.name == 'nt' else 'ffprobe',
        'ffplay': 'ffplay.exe' if os.name == 'nt' else 'ffplay'
    }
    
    def __init__(self):
        self.tool_paths = self._get_tool_paths()
    
    @staticmethod
    def _get_tool_paths():

        tools = {}
        

        if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):

            app_dir = os.path.dirname(sys.executable)
        else:

            app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        for tool_name, tool_filename in FFToolsManager._FFT_TOOLS.items():

            app_tool_path = os.path.join(app_dir, tool_filename)
            if os.path.isfile(app_tool_path):
                tools[tool_name] = app_tool_path
            else:

                try:
                    result = subprocess.run(
                        ['where' if os.name == 'nt' else 'which', tool_filename],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        tools[tool_name] = result.stdout.strip().split('\n')[0]
                    else:
                        tools[tool_name] = tool_filename
                except Exception:
                    tools[tool_name] = tool_filename
        
        return tools
    
    def get_ffmpeg(self):
        return self.tool_paths.get('ffmpeg', 'ffmpeg')
    
    def get_ffprobe(self):
        return self.tool_paths.get('ffprobe', 'ffprobe')
    
    def get_ffplay(self):
        return self.tool_paths.get('ffplay', 'ffplay')
    
    def get_all_tools(self):
        return self.tool_paths.copy()



_ff_tools_instance = None


def get_ff_tools():
    global _ff_tools_instance
    if _ff_tools_instance is None:
        _ff_tools_instance = FFToolsManager()
    return _ff_tools_instance
