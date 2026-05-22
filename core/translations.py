import json
import os
import sys
import platform


class TranslationManager:
    
    def __init__(self):
        self.translations = {
            'hu': {
                'title': 'Videó Letöltő',
                'video_url': 'Videó URL:',
                'download_mode': 'Letöltési mód:',
                'video_audio': 'Videó + Hang',
                'audio_only': 'Csak Hang',
                'video_only': 'Csak Videó',
                'resolution': 'Felbontás:',
                'select_output': 'Kimeneti mappa kiválasztása',
                'download': 'Letöltés',
                'download_choose_folder': 'Letöltés (Előbb válaszd ki a kimeneti mapát)',
                'status': '',
                'ok': 'OK',
                'cancel': 'Mégse',
                'ready': 'Kész',
                'invalid_audio_file': 'Nincs kiválasztva érvényes hangfájl!',
                'invalid_video_file': 'Nincs kiválasztva érvényes videófájl!',
                'no_target_format': 'Nem történt változtatás!',
                'sync_audio_title': 'Szinkronizált hangsáv',
                'sync_audio_msg': 'A kiválasztott hangsáv valószínűleg szinkronizált.\nSzeretnéd inkább az eredeti hangsávval letölteni?\n\nKiválasztott: {selected}\nEredeti: {original}',
                'original_audio': 'Eredeti hangsávval',
                'keep_selected': 'Maradjon a kiválasztott',
                'fps_too_high': 'A megadott FPS nagyobb, mint a jelenlegi FPS!',
                'resolutions_need_url': 'Elérhető felbontásokhoz URL-t adj meg!',
                'fetching_resolutions': 'Felbontások lekérése...',
                'no_resolution': 'Nem található felbontás',
                'invalid_url': 'Hibás vagy nem támogatott URL',
                'error': 'Hiba',
                'missing_url': 'Add meg a videó URL-jét!',
                'missing_folder': 'Válassz kimeneti mappát!',
                'start_download': 'Letöltés indítása...',
                'speed': 'Sebesség',
                'remaining_time': 'Hátralévő idő',
                'download_complete': 'Letöltés kész!',
                'success': 'Sikeres letöltés',
                'download_finished': 'A letöltés befejeződött!',
                'language': 'Nyelv:',
                'english': 'Angol',
                'hungarian': 'Magyar',
                'current_resolution': 'Jelenlegi felbontás:',
                'current_bitrate': 'Jelenlegi bitráta:',
                'current_fps': 'Jelenlegi FPS:',
                'no_change': 'Nem történt változtatás.',
                'menu_language': 'Language',
                'audio_quality': 'Hang felbontás:',
                'please_choose': 'Kérjük válassz!',
                'missing_choice_title': 'Hiányzó választás',
                'missing_both': 'Nincs videó és hang felbontás kiválasztva! Folytatod alapértelmezett értékekkel?',
                'missing_video': 'Nincs videó felbontás kiválasztva! Folytatod alapértelmezett értékekkel?',
                'missing_audio': 'Nincs hang felbontás kiválasztva! Folytatod alapértelmezett értékekkel?',
                'continue_default': 'Folytatás',
                "converter": "Átalakító",
                "audio_converter": "Hang átváltó",
                "video_converter": "Videó átváltó",
                "select_audio_file": "Hangfájl kiválasztása:",
                "select_video_file": "Videófájl kiválasztása:",
                "browse": "Tallózás",
                "target_format": "Cél formátum:",
                "target_bitrate": "Cél bitráta (kbps):",
                "convert": "Átalakítás",
                "conversion_done": "Átalakítás kész: {file}",
                "conversion_failed": "Átalakítás sikertelen: {error}",
                "target_resolution": "Cél felbontás (pl. 1280x720):",
                "audio_bitrate": "Hang bitráta:",
                "no_audio": "Nincs vagy nem ismert",
                "progress": "Állapot",
                "updates": "Frissítések",
                "check_updates_now": "Frissítés indítása most",
                "current_version": "Jelenlegi verzió: {version}",
                "checking_updates": "Frissítések ellenőrzése...",
                "updates_finished": "Frissítések ellenőrzése kész.",
                "restart_required": "A frissítés befejezéséhez az alkalmazás újraindul.",
                "no_updates_needed": "Nem volt szükség frissítésre."
            },
            'en': {
                'title': 'Video Downloader',
                'video_url': 'Video URL:',
                'download_mode': 'Download mode:',
                'video_audio': 'Video + Audio',
                'audio_only': 'Audio Only',
                'video_only': 'Video Only',
                'resolution': 'Resolution:',
                'select_output': 'Select output folder',
                'download': 'Download',
                'download_choose_folder': 'Download (Select output folder first)',
                'status': '',
                'ok': 'OK',
                'cancel': 'Cancel',
                'ready': 'Ready',
                'invalid_audio_file': 'No valid audio file selected!',
                'invalid_video_file': 'No valid video file selected!',
                'no_target_format': 'Nothing changed!',
                'sync_audio_title': 'Synchronized audio track',
                'sync_audio_msg': 'The selected audio track is likely synchronized.\nWould you rather download with the original audio track?\n\nSelected: {selected}\nOriginal: {original}',
                'original_audio': 'With original audio',
                'keep_selected': 'Keep selected',
                'fps_too_high': 'The given FPS is higher than the current FPS!',
                'resolutions_need_url': 'Enter URL to get available resolutions!',
                'fetching_resolutions': 'Fetching resolutions...',
                'no_resolution': 'No resolution found',
                'invalid_url': 'Invalid or unsupported URL',
                'error': 'Error',
                'missing_url': 'Please enter the video URL!',
                'missing_folder': 'Please select output folder!',
                'start_download': 'Starting download...',
                'speed': 'Speed',
                'remaining_time': 'Remaining time',
                'download_complete': 'Download complete!',
                'success': 'Download successful',
                'download_finished': 'Download finished!',
                'language': 'Language:',
                'english': 'English',
                'hungarian': 'Hungarian',
                'current_resolution': 'Current resolution:',
                'current_bitrate': 'Current bitrate:',
                'current_fps': 'Current FPS:',
                'no_change': 'No changes made.',
                'menu_language': 'Language',
                'audio_quality': 'Audio quality:',
                'please_choose': 'Please choose!',
                'missing_choice_title': 'Missing selection',
                'missing_both': 'No video and audio quality selected! Continue with default values?',
                'missing_video': 'No video quality selected! Continue with default values?',
                'missing_audio': 'No audio quality selected! Continue with default values?',
                'continue_default': 'Continue',
                "converter": "Transformer",
                "audio_converter": "Audio Converter",
                "video_converter": "Video Converter",
                "select_audio_file": "Select audio file:",
                "select_video_file": "Select video file:",
                "browse": "Browse",
                "target_format": "Target format:",
                "target_bitrate": "Target bitrate (kbps):",
                "convert": "Transform",
                "conversion_done": "Conversion done: {file}",
                "conversion_failed": "Conversion failed: {error}",
                "target_resolution": "Target resolution (e.g. 1280x720):",
                "audio_bitrate": "Audio bitrate:",
                "no_audio": "No audio or unknown",
                "progress": "Progress",
                "updates": "Updates",
                "check_updates_now": "Run updates now",
                "current_version": "Current version: {version}",
                "checking_updates": "Checking for updates...",
                "updates_finished": "Update check finished.",
                "restart_required": "The application will restart to finish the update.",
                "no_updates_needed": "Everything is already up to date."
            }
        }
        self._load_more_languages()
        self.language = 'en'

    def _load_more_languages(self):
        prog_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        lang_path = os.path.join(prog_dir, 'more_languages.json')
        if os.path.isfile(lang_path):
            try:
                with open(lang_path, 'r', encoding='utf-8') as f:
                    langs = json.load(f)
                    if isinstance(langs, dict):
                        self.translations.update(langs)
            except Exception:
                pass

    def set_language(self, lang_code):
        if lang_code in self.translations:
            self.language = lang_code

    def get(self, key):
        return self.translations[self.language].get(key, key)

    def get_available_languages(self):
        return list(self.translations.keys())
