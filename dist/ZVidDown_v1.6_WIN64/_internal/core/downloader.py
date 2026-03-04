import yt_dlp
import os
from core.fftools import get_ff_tools


class VideoDownloader:
    
    def __init__(self, output_path, progress_callback=None):

        self.output_path = output_path
        self.progress_callback = progress_callback
        self.ff_tools = get_ff_tools()
    
    def _get_hook(self):

        def hook(d):
            if self.progress_callback:
                self.progress_callback(d)
        return hook
    
    @staticmethod
    def _is_original_audio_fmt(fmt):
        lang = fmt.get('language') or ''
        if lang.lower() in ['original', 'source', 'main', 'hun', 'eng', 'en', 'hu']:
            return True
        note = (fmt.get('format_note') or '').lower()
        if 'original' in note or 'source' in note or 'main' in note or 'hun' in note or 'eng' in note:
            return True
        return False
    
    def get_available_formats(self, url):

        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'ffmpeg_location': self.ff_tools.get_ffmpeg()
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            formats = info.get('formats', [])
            
            video_formats = []
            audio_formats = []
            video_itag_map = {}
            audio_itag_map = {}
            

            for f in formats:
                if f.get('vcodec') != 'none' and f.get('height') and f.get('format_id'):
                    res = f.get('format_note') or (str(f.get('height')) + 'p')
                    itag = str(f.get('format_id'))
                    ext = f.get('ext', 'unknown')
                    fps = f.get('fps', 0)
                    label = f"{res} ({itag}) [{ext}, {fps}fps]" if fps else f"{res} ({itag}) [{ext}]"
                    
                    if label and itag and label not in video_formats:
                        video_formats.append(label)
                        video_itag_map[label] = itag
            

            for f in formats:
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('format_id'):
                    abr = f.get('abr')
                    itag = str(f.get('format_id'))
                    ext = f.get('ext', 'unknown')
                    acodec = f.get('acodec', 'unknown')
                    label = f"{int(abr)} kbps ({itag}) [{ext}, {acodec}]" if abr and acodec else f"{int(abr)} kbps ({itag}) [{ext}]"
                    
                    if label and itag and label not in audio_formats:
                        audio_formats.append(label)
                        audio_itag_map[label] = itag
            
            return {
                'video_formats': video_formats,
                'audio_formats': audio_formats,
                'video_itag_map': video_itag_map,
                'audio_itag_map': audio_itag_map
            }
        except Exception as e:
            raise Exception(f"Formátumok lekérésének hiba: {str(e)}")
    
    def download(self, url, mode, video_itag=None, audio_itag=None):

        ydl_opts = {
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self._get_hook()],
            'ffmpeg_location': self.ff_tools.get_ffmpeg(),
            'continuedl': True,
            'retries': 5,
            'nocheckcertificate': True,
            'quiet': True,
        }
        

        if mode == 'video_audio':
            if video_itag and audio_itag:
                ydl_opts['format'] = f"{video_itag}+{audio_itag}/best"
            elif video_itag:
                ydl_opts['format'] = f"{video_itag}+bestaudio/best"
            elif audio_itag:
                ydl_opts['format'] = f"bestvideo+{audio_itag}/best"
            else:
                try:
                    with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        orig_audio_itag = None
                        for f in info.get('formats', []):
                            if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('format_id') and self._is_original_audio_fmt(f):
                                orig_audio_itag = f.get('format_id')
                                break
                        if orig_audio_itag:
                            ydl_opts['format'] = f"bestvideo+{orig_audio_itag}/best"
                        else:
                            ydl_opts['format'] = "bestvideo+bestaudio/best"
                except Exception:
                    ydl_opts['format'] = "bestvideo+bestaudio/best"
        
        elif mode == 'audio_only':
            if audio_itag:
                ydl_opts['format'] = f"{audio_itag}/bestaudio"
            else:
                try:
                    with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        orig_audio_itag = None
                        for f in info.get('formats', []):
                            if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('format_id') and self._is_original_audio_fmt(f):
                                orig_audio_itag = f.get('format_id')
                                break
                        if orig_audio_itag:
                            ydl_opts['format'] = orig_audio_itag
                        else:
                            ydl_opts['format'] = "bestaudio/best"
                except Exception:
                    ydl_opts['format'] = "bestaudio/best"
        
        elif mode == 'video_only':
            if video_itag:
                ydl_opts['format'] = f'{video_itag}/bestvideo'
            else:
                ydl_opts['format'] = 'bestvideo/best'
        

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            msg = str(e)
            if 'HTTP Error 403' in msg or '403' in msg:
                raise Exception(
                    "Letöltés hiba: HTTP 403 Forbidden (videó blokkolva/korlátozott). "
                    "Próbálkozás sütikkel vagy VPN-nel, vagy frissítsd yt-dlp-t. "
                    f"eredeti üzenet: {msg}"
                )
            raise Exception(f"Letöltés hiba: {msg}")
