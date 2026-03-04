import os
import subprocess
from core.fftools import get_ff_tools


class AudioConverter:
    
    def __init__(self, progress_callback=None):

        self.progress_callback = progress_callback
        self.ff_tools = get_ff_tools()
    
    def get_audio_bitrate(self, file_path):
        try:
            ffprobe = self.ff_tools.get_ffprobe()
            cmd = [
                ffprobe, '-v', 'error', '-select_streams', 'a:0',
                '-show_entries', 'stream=bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            br = result.stdout.strip()
            
            if br.strip().isdigit():
                return int(int(br) / 1000)
            return None
        except Exception:
            return None
    
    def convert(self, src_file, target_format, bitrate=None):

        if not os.path.isfile(src_file):
            raise Exception("A forrás fájl nem létezik!")
        
        ffmpeg = self.ff_tools.get_ffmpeg()
        ffprobe = self.ff_tools.get_ffprobe()
        
        out_dir = os.path.dirname(src_file)
        base = os.path.splitext(os.path.basename(src_file))[0]
        out_path = os.path.join(out_dir, f'{base}_converted.{target_format}')
        

        orig_ext = os.path.splitext(src_file)[1].lstrip('.')
        orig_bitrate = None
        
        try:
            cmd = [
                ffprobe, '-v', 'error', '-select_streams', 'a:0',
                '-show_entries', 'stream=bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                src_file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            br_val = result.stdout.strip()
            if br_val.strip().isdigit():
                orig_bitrate = str(int(int(br_val) / 1000))
        except Exception:
            pass
        
        if target_format == orig_ext and (not bitrate or bitrate == orig_bitrate):
            raise Exception("Nem történt változtatás!")
        
        try:

            cmd_len = [
                ffprobe, '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                src_file
            ]
            result = subprocess.run(cmd_len, capture_output=True, text=True)
            try:
                total_sec = float(result.stdout.strip())
            except Exception:
                total_sec = None
            

            cmd = [ffmpeg, '-y', '-i', src_file]
            if bitrate:
                cmd += ['-b:a', f'{bitrate}k']
            cmd += [out_path, '-progress', 'pipe:1', '-nostats']
            
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            
            last_percent = 0
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                
                if 'out_time_ms=' in line and total_sec:
                    try:
                        ms_str = line.strip().split('=')[1]
                        if ms_str and ms_str.isdigit():
                            ms = int(ms_str)
                            sec = ms / 1_000_000
                            percent = int((sec / total_sec) * 100)
                            if percent > 100:
                                percent = 100
                            if percent != last_percent and self.progress_callback:
                                self.progress_callback(percent)
                                last_percent = percent
                    except (ValueError, IndexError):
                        pass
                elif 'progress=end' in line:
                    if self.progress_callback:
                        self.progress_callback(100)
                    break
            
            proc.wait()
            
            if proc.returncode == 0:
                return out_path
            else:
                raise Exception("FFmpeg konvertálási hiba")
        
        except Exception as e:
            raise Exception(f"Audio konvertálási hiba: {str(e)}")


class VideoConverter:
    
    def __init__(self, progress_callback=None):

        self.progress_callback = progress_callback
        self.ff_tools = get_ff_tools()
    
    def get_video_info(self, file_path):
        try:
            ffprobe = self.ff_tools.get_ffprobe()
            
            info = {}
            

            cmd_res = [
                ffprobe, '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=s=x:p=0',
                file_path
            ]
            res = subprocess.run(cmd_res, capture_output=True, text=True).stdout.strip()
            info['resolution'] = res if res else None
            

            cmd_abr = [
                ffprobe, '-v', 'error', '-select_streams', 'a:0',
                '-show_entries', 'stream=bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                file_path
            ]
            abr = subprocess.run(cmd_abr, capture_output=True, text=True).stdout.strip()
            if abr.strip().isdigit():
                info['audio_bitrate'] = int(int(abr) / 1000)
            else:
                info['audio_bitrate'] = None
            

            cmd_fps = [
                ffprobe, '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=r_frame_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                file_path
            ]
            fps_raw = subprocess.run(cmd_fps, capture_output=True, text=True).stdout.strip()
            try:
                if '/' in fps_raw:
                    num, denom = fps_raw.split('/')
                    fps_val = round(float(num) / float(denom), 2) if float(denom) != 0 else 0
                else:
                    fps_val = float(fps_raw)
                info['fps'] = fps_val
            except Exception:
                info['fps'] = None
            
            return info
        except Exception:
            return {}
    
    def convert(self, src_file, target_format, target_resolution=None, audio_bitrate=None, fps=None):

        if not os.path.isfile(src_file):
            raise Exception("A forrás fájl nem létezik!")
        
        ffmpeg = self.ff_tools.get_ffmpeg()
        ffprobe = self.ff_tools.get_ffprobe()
        
        out_dir = os.path.dirname(src_file)
        base = os.path.splitext(os.path.basename(src_file))[0]
        out_path = os.path.join(out_dir, f'{base}_converted.{target_format}')
        

        orig_ext = os.path.splitext(src_file)[1].lstrip('.')
        orig_bitrate = None
        orig_res = None
        orig_fps = None
        
        try:
            cmd_abr = [
                ffprobe, '-v', 'error', '-select_streams', 'a:0',
                '-show_entries', 'stream=bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                src_file
            ]
            abr_val = subprocess.run(cmd_abr, capture_output=True, text=True).stdout.strip()
            if abr_val.strip().isdigit():
                orig_bitrate = str(int(int(abr_val) / 1000))
            
            cmd_res = [
                ffprobe, '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=s=x:p=0',
                src_file
            ]
            res_val = subprocess.run(cmd_res, capture_output=True, text=True).stdout.strip()
            if res_val:
                orig_res = res_val
            
            cmd_fps = [
                ffprobe, '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=r_frame_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                src_file
            ]
            fps_raw = subprocess.run(cmd_fps, capture_output=True, text=True).stdout.strip()
            if fps_raw and fps_raw.lower() != 'n/a':
                try:
                    if '/' in fps_raw:
                        num, denom = fps_raw.split('/')
                        fps_val = round(float(num) / float(denom), 2) if float(denom) != 0 else 0
                    else:
                        fps_val = float(fps_raw)
                    if fps_val:
                        orig_fps = str(int(fps_val))
                except (ValueError, ZeroDivisionError):
                    pass
        except Exception:
            pass
        
        if (target_format == orig_ext and
            (not audio_bitrate or audio_bitrate == orig_bitrate) and
            (not target_resolution or target_resolution == orig_res) and
            (not fps or fps == orig_fps)):
            raise Exception("Nem történt változtatás!")
        
        try:

            cmd_len = [
                ffprobe, '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                src_file
            ]
            result = subprocess.run(cmd_len, capture_output=True, text=True)
            try:
                total_sec = float(result.stdout.strip())
            except Exception:
                total_sec = None
            

            cmd = [ffmpeg, '-y', '-i', src_file]
            
            if target_resolution and 'x' in target_resolution:
                cmd += ['-vf', f'scale={target_resolution}']
            
            if fps:
                cmd += ['-r', str(fps)]
            
            if audio_bitrate:
                cmd += ['-b:a', f'{audio_bitrate}k']
            
            cmd += [out_path, '-progress', 'pipe:1', '-nostats']
            
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            
            last_percent = 0
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                
                if 'out_time_ms=' in line and total_sec:
                    try:
                        ms_str = line.strip().split('=')[1]
                        if ms_str and ms_str.isdigit():
                            ms = int(ms_str)
                            sec = ms / 1_000_000
                            percent = int((sec / total_sec) * 100)
                            if percent > 100:
                                percent = 100
                            if percent != last_percent and self.progress_callback:
                                self.progress_callback(percent)
                                last_percent = percent
                    except (ValueError, IndexError):
                        pass
                elif 'progress=end' in line:
                    if self.progress_callback:
                        self.progress_callback(100)
                    break
            
            proc.wait()
            
            if proc.returncode == 0:
                return out_path
            else:
                raise Exception("FFmpeg konvertálási hiba")
        
        except Exception as e:
            raise Exception(f"Video konvertálási hiba: {str(e)}")
