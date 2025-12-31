import sys
import os
import threading
import sys
import yt_dlp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import platform

class LetoltoTk(tk.Tk):
    def __init__(self):
        super().__init__()
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
                'resolutions_need_url': 'Elérhető felbontásokhoz URL-t adj meg!',
                'fetching_resolutions': 'Felbontások lekérése...',
                'no_resolution': 'Nem található felbontás',
                'invalid_url': 'Hibás vagy nem támogatott URL',
                'error': 'Hiba',
                'missing_url': 'Add meg a YouTube videó URL-jét!',
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
                'menu_language': 'Language',
                'audio_quality': 'Hang felbontás:',
                'please_choose': 'Kérjük válassz!',
                'missing_choice_title': 'Missing selection',
                'missing_both': 'No video and audio quality selected!',
                'missing_video': 'No video quality selected!',
                'missing_audio': 'No audio quality selected!',
                'continue_default': 'Continue with default values',
                'play': 'Lejátszás',
                "converter": "Átváltó"
                ,  "audio_converter": "Hang átváltó"
                ,  "video_converter": "Videó átváltó"
                ,  "select_audio_file": "Hangfájl kiválasztása:"
                ,  "select_video_file": "Videófájl kiválasztása:"
                ,  "browse": "Tallózás"
                ,  "current_bitrate": "Jelenlegi bitráta:"
                ,  "target_format": "Cél formátum:"
                ,  "target_bitrate": "Cél bitráta (kbps):"
                ,  "convert": "Átalakítás"
                ,  "conversion_done": "Átalakítás kész: {file}"
                ,  "conversion_failed": "Átalakítás sikertelen: {error}"
                ,  "current_resolution": "Jelenlegi felbontás:"
                ,  "target_resolution": "Cél felbontás (pl. 1280x720):"
                ,  "audio_bitrate": "Hang bitráta:"
                ,  "no_audio": "Nincs vagy nem ismert"
                ,  "progress": "Állapot"
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
                'resolutions_need_url': 'Enter URL to get available resolutions!',
                'fetching_resolutions': 'Fetching resolutions...',
                'no_resolution': 'No resolution found',
                'invalid_url': 'Invalid or unsupported URL',
                'error': 'Error',
                'missing_url': 'Please enter the YouTube video URL!',
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
                'menu_language': 'Language',
                'audio_quality': 'Audio quality:',
                'please_choose': 'Please choose!',
                'missing_choice_title': 'Hiányzó választás',
                'missing_both': 'Nem választottál videó és hang felbontást!',
                'missing_video': 'Nem választottál videó felbontást!',
                'missing_audio': 'Nem választottál hang felbontást!',
                'continue_default': 'Tovább alapértelmezett értékekkel',
                'play': 'Play',
                  "converter": "Converter"
                ,  "audio_converter": "Audio Converter"
                ,  "video_converter": "Video Converter"
                ,  "select_audio_file": "Select audio file:"
                ,  "select_video_file": "Select video file:"
                ,  "browse": "Browse"
                ,  "current_bitrate": "Current bitrate:"
                ,  "target_format": "Target format:"
                ,  "target_bitrate": "Target bitrate (kbps):"
                ,  "convert": "Convert"
                ,  "conversion_done": "Conversion done: {file}"
                ,  "conversion_failed": "Conversion failed: {error}"
                ,  "current_resolution": "Current resolution:"
                ,  "target_resolution": "Target resolution (e.g. 1280x720):"
                ,  "audio_bitrate": "Audio bitrate:"
                ,  "no_audio": "No audio or unknown"
                ,  "progress": "Progress"
            }
        }
        self._load_more_languages()
        self.language = 'en'
        self.config_path = self._get_config_path()
        self._load_language()
        self.title(self._t('title'))
        self.geometry('400x440')
        self.resizable(True, True)
        self.kimeneti_mappa = ''
        self._create_menu()
        self._felulet()

    def _load_more_languages(self):
        prog_dir = os.path.dirname(sys.argv[0])
        lang_path = os.path.join(prog_dir, 'more_languages.json')
        if os.path.isfile(lang_path):
            try:
                with open(lang_path, 'r', encoding='utf-8') as f:
                    langs = json.load(f)
                    if isinstance(langs, dict):
                        self.translations.update(langs)
            except Exception:
                pass

    def _get_config_path(self):
        if platform.system() == 'Windows':
            appdata = os.getenv('APPDATA')
        else:
            appdata = os.path.expanduser('~/.config')
        config_dir = os.path.join(appdata, 'zviddown')
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, 'settings.json')

    def _save_language(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump({'language': self.language}, f)
        except Exception:
            pass

    def _load_language(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'language' in data:
                    self.language = data['language']
        except Exception:
            self.language = 'en'

    def _t(self, key):
        return self.translations[self.language].get(key, key)

    def _create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        more_menu = tk.Menu(menubar, tearoff=0)
        lang_menu = tk.Menu(more_menu, tearoff=0)
        self.lang_var = tk.StringVar(value=self.language)
        for lang_code in self.translations.keys():
            lang_menu.add_radiobutton(label=lang_code, value=lang_code, variable=self.lang_var, command=lambda c=lang_code: self._set_language(c))
        more_menu.add_cascade(label=self._t('menu_language'), menu=lang_menu)
        more_menu.add_separator()
        more_menu.add_command(label=self._t('converter'), command=self._open_converter_window)
        menubar.add_cascade(label='⋮', menu=more_menu)

    def _open_converter_window(self):
        import subprocess
        win = tk.Toplevel(self)
        win.title(self._t('converter'))
        win.geometry('440x420')

        tab_control = ttk.Notebook(win)
        tab_audio = ttk.Frame(tab_control)
        tab_video = ttk.Frame(tab_control)
        tab_control.add(tab_audio, text=self._t('audio_converter'))
        tab_control.add(tab_video, text=self._t('video_converter'))
        tab_control.pack(expand=1, fill='both')

        def select_audio_file():
            filetypes = [('Audio fájlok', '*.mp3 *.ogg *.m4a *.wav *.flac *.aac *.opus'), ('Minden fájl', '*.*')]
            path = filedialog.askopenfilename(title='Válassz hangfájlt', filetypes=filetypes)
            if path:
                entry_audio_file.delete(0, tk.END)
                entry_audio_file.insert(0, path)
                show_audio_bitrate(path)

        def show_audio_bitrate(path):
            try:
                if hasattr(sys, '_MEIPASS'):
                    ffprobe = os.path.join(sys._MEIPASS, 'ffprobe.exe')
                else:
                    ffprobe = 'ffprobe.exe' if os.name == 'nt' else 'ffprobe'
                cmd = [ffprobe, '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                br = result.stdout.strip()
                if br.isdigit():
                    br_kbps = int(int(br) / 1000)
                    label_audio_bitrate.config(text=f'Jelenlegi bitráta: {br_kbps} kbps')
                    spin_audio_bitrate.delete(0, tk.END)
                    spin_audio_bitrate.insert(0, str(br_kbps))
                else:
                    label_audio_bitrate.config(text='Jelenlegi bitráta: nem ismert')
            except Exception:
                label_audio_bitrate.config(text='Jelenlegi bitráta: hiba')

        def convert_audio():
            src = entry_audio_file.get()
            fmt = combo_audio_format.get()
            br = spin_audio_bitrate.get()
            if not src or not os.path.isfile(src):
                messagebox.showerror('Hiba', 'Nincs kiválasztva érvényes hangfájl!')
                return
            if not fmt:
                messagebox.showerror('Hiba', 'Nincs kiválasztva célformátum!')
                return
            try:
                out_dir = os.path.dirname(src)
                base = os.path.splitext(os.path.basename(src))[0]
                out_path = os.path.join(out_dir, f'{base}_converted.{fmt}')
                if hasattr(sys, '_MEIPASS'):
                    ffmpeg = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
                else:
                    ffmpeg = 'ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'
                cmd = [ffmpeg, '-y', '-i', src, '-b:a', f'{br}k', out_path]
                subprocess.run(cmd, check=True)
                messagebox.showinfo('Kész', f'Átalakítás kész: {out_path}')
            except Exception as e:
                messagebox.showerror('Hiba', f'Átalakítás sikertelen: {e}')

        tk.Label(tab_audio, text=self._t('select_audio_file')).pack(anchor='w', padx=10, pady=(10,0))
        frame_audio_file = tk.Frame(tab_audio)
        frame_audio_file.pack(fill='x', padx=10)
        entry_audio_file = tk.Entry(frame_audio_file, width=38)
        entry_audio_file.pack(side='left', fill='x', expand=True)
        btn_audio_browse = tk.Button(frame_audio_file, text=self._t('browse'), command=select_audio_file)
        btn_audio_browse.pack(side='left', padx=4)

        label_audio_bitrate = tk.Label(tab_audio, text=self._t('current_bitrate'))
        label_audio_bitrate.pack(anchor='w', padx=10, pady=(6,0))

        tk.Label(tab_audio, text=self._t('target_format')).pack(anchor='w', padx=10, pady=(10,0))
        combo_audio_format = ttk.Combobox(tab_audio, values=['mp3', 'ogg', 'm4a', 'aac', 'opus', 'wav', 'flac'], state='readonly')
        combo_audio_format.pack(fill='x', padx=10)

        tk.Label(tab_audio, text=self._t('target_bitrate')).pack(anchor='w', padx=10, pady=(10,0))
        spin_audio_bitrate = tk.Entry(tab_audio, width=8)
        spin_audio_bitrate.pack(anchor='w', padx=10)

        tk.Label(tab_audio, text=self._t('progress')).pack(anchor='w', padx=10, pady=(10,0))
        audio_progress = ttk.Progressbar(tab_audio, orient='horizontal', length=320, mode='determinate')
        audio_progress.pack(padx=10, pady=(0,0))
        audio_percent = tk.Label(tab_audio, text='0%')
        audio_percent.pack(anchor='w', padx=10)

        def audio_update_progress(val):
            audio_progress['value'] = val
            audio_percent.config(text=f'{val}%')

        def convert_audio():
            src = entry_audio_file.get()
            fmt = combo_audio_format.get()
            br = spin_audio_bitrate.get()
            if not src or not os.path.isfile(src):
                messagebox.showerror(self._t('error'), self._t('missing_url'))
                return
            if not fmt:
                messagebox.showerror(self._t('error'), self._t('missing_audio'))
                return
            def run_ffmpeg():
                try:
                    out_dir = os.path.dirname(src)
                    base = os.path.splitext(os.path.basename(src))[0]
                    out_path = os.path.join(out_dir, f'{base}_converted.{fmt}')
                    if hasattr(sys, '_MEIPASS'):
                        ffmpeg = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
                        ffprobe = os.path.join(sys._MEIPASS, 'ffprobe.exe')
                    else:
                        ffmpeg = 'ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'
                        ffprobe = 'ffprobe.exe' if os.name == 'nt' else 'ffprobe'
                    cmd_len = [ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', src]
                    result = subprocess.run(cmd_len, capture_output=True, text=True)
                    try:
                        total_sec = float(result.stdout.strip())
                    except Exception:
                        total_sec = None
                    cmd = [ffmpeg, '-y', '-i', src, '-b:a', f'{br}k', out_path, '-progress', 'pipe:1', '-nostats']
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                    last_percent = 0
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        if 'out_time_ms=' in line and total_sec:
                            ms = int(line.strip().split('=')[1])
                            sec = ms / 1_000_000
                            percent = int((sec / total_sec) * 100)
                            if percent > 100:
                                percent = 100
                            if percent != last_percent:
                                win.after(0, audio_update_progress, percent)
                                last_percent = percent
                        elif 'progress=end' in line:
                            win.after(0, audio_update_progress, 100)
                            break
                    proc.wait()
                    if proc.returncode == 0:
                        win.after(0, lambda: messagebox.showinfo(self._t('success'), self._t('conversion_done').format(file=out_path)))
                    else:
                        win.after(0, lambda: messagebox.showerror(self._t('error'), self._t('conversion_failed').format(error='')))
                except Exception as e:
                    win.after(0, lambda: messagebox.showerror(self._t('error'), self._t('conversion_failed').format(error=e)))
                win.after(0, audio_update_progress, 0)
            threading.Thread(target=run_ffmpeg, daemon=True).start()

        btn_audio_convert = tk.Button(tab_audio, text=self._t('convert'), command=convert_audio)
        btn_audio_convert.pack(pady=16)

        def select_video_file():
            filetypes = [('Videó fájlok', '*.mp4 *.mkv *.webm *.avi *.mov *.flv *.wmv'), ('Minden fájl', '*.*')]
            path = filedialog.askopenfilename(title='Válassz videófájlt', filetypes=filetypes)
            if path:
                entry_video_file.delete(0, tk.END)
                entry_video_file.insert(0, path)
                show_video_info(path)

        def show_video_info(path):
            try:
                if hasattr(sys, '_MEIPASS'):
                    ffprobe = os.path.join(sys._MEIPASS, 'ffprobe.exe')
                else:
                    ffprobe = 'ffprobe.exe' if os.name == 'nt' else 'ffprobe'
                cmd_res = [ffprobe, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', path]
                res = subprocess.run(cmd_res, capture_output=True, text=True).stdout.strip()
                label_video_res.config(text=f'Jelenlegi felbontás: {res}' if res else 'Jelenlegi felbontás: nem ismert')
                cmd_abr = [ffprobe, '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', path]
                abr = subprocess.run(cmd_abr, capture_output=True, text=True).stdout.strip()
                if abr.isdigit():
                    abr_kbps = int(int(abr) / 1000)
                    label_video_audio_bitrate.config(text=f'Hang bitráta: {abr_kbps} kbps')
                    spin_video_audio_bitrate.config(state='normal')
                    spin_video_audio_bitrate.delete(0, tk.END)
                    spin_video_audio_bitrate.insert(0, str(abr_kbps))
                else:
                    label_video_audio_bitrate.config(text='Hang bitráta: nincs vagy nem ismert')
                    spin_video_audio_bitrate.delete(0, tk.END)
                    spin_video_audio_bitrate.config(state='disabled')
            except Exception:
                label_video_res.config(text='Jelenlegi felbontás: hiba')
                label_video_audio_bitrate.config(text='Hang bitráta: hiba')
                spin_video_audio_bitrate.delete(0, tk.END)
                spin_video_audio_bitrate.config(state='disabled')

        def convert_video():
            src = entry_video_file.get()
            fmt = combo_video_format.get()
            res = combo_video_res.get()
            abr = spin_video_audio_bitrate.get()
            if not src or not os.path.isfile(src):
                messagebox.showerror('Hiba', 'Nincs kiválasztva érvényes videófájl!')
                return
            if not fmt:
                messagebox.showerror('Hiba', 'Nincs kiválasztva célformátum!')
                return
            try:
                out_dir = os.path.dirname(src)
                base = os.path.splitext(os.path.basename(src))[0]
                out_path = os.path.join(out_dir, f'{base}_converted.{fmt}')
                ffmpeg = 'ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'
                cmd = [ffmpeg, '-y', '-i', src]
                if res and 'x' in res:
                    cmd += ['-vf', f'scale={res}']
                if spin_video_audio_bitrate.cget('state') == 'normal' and abr:
                    cmd += ['-b:a', f'{abr}k']
                cmd += [out_path]
                subprocess.run(cmd, check=True)
                messagebox.showinfo('Kész', f'Átalakítás kész: {out_path}')
            except Exception as e:
                messagebox.showerror('Hiba', f'Átalakítás sikertelen: {e}')

        tk.Label(tab_video, text=self._t('select_video_file')).pack(anchor='w', padx=10, pady=(10,0))
        frame_video_file = tk.Frame(tab_video)
        frame_video_file.pack(fill='x', padx=10)
        entry_video_file = tk.Entry(frame_video_file, width=38)
        entry_video_file.pack(side='left', fill='x', expand=True)
        btn_video_browse = tk.Button(frame_video_file, text=self._t('browse'), command=select_video_file)
        btn_video_browse.pack(side='left', padx=4)

        label_video_res = tk.Label(tab_video, text=self._t('current_resolution'))
        label_video_res.pack(anchor='w', padx=10, pady=(6,0))

        tk.Label(tab_video, text=self._t('target_resolution')).pack(anchor='w', padx=10, pady=(10,0))
        combo_video_res = ttk.Combobox(tab_video, values=['1920x1080', '1280x720', '854x480', '640x360', '320x240'], state='normal')
        combo_video_res.pack(fill='x', padx=10)

        tk.Label(tab_video, text=self._t('target_format')).pack(anchor='w', padx=10, pady=(10,0))
        combo_video_format = ttk.Combobox(tab_video, values=['mp4', 'mkv', 'webm', 'avi', 'mov', 'flv'], state='readonly')
        combo_video_format.pack(fill='x', padx=10)

        label_video_audio_bitrate = tk.Label(tab_video, text=self._t('audio_bitrate'))
        label_video_audio_bitrate.pack(anchor='w', padx=10, pady=(10,0))
        spin_video_audio_bitrate = tk.Entry(tab_video, width=8)
        spin_video_audio_bitrate.pack(anchor='w', padx=10)
        spin_video_audio_bitrate.config(state='disabled')

        tk.Label(tab_video, text=self._t('progress')).pack(anchor='w', padx=10, pady=(10,0))
        video_progress = ttk.Progressbar(tab_video, orient='horizontal', length=320, mode='determinate')
        video_progress.pack(padx=10, pady=(0,0))
        video_percent = tk.Label(tab_video, text='0%')
        video_percent.pack(anchor='w', padx=10)

        def video_update_progress(val):
            video_progress['value'] = val
            video_percent.config(text=f'{val}%')

        def convert_video():
            src = entry_video_file.get()
            fmt = combo_video_format.get()
            res = combo_video_res.get()
            abr = spin_video_audio_bitrate.get()
            if not src or not os.path.isfile(src):
                messagebox.showerror(self._t('error'), self._t('missing_url'))
                return
            if not fmt:
                messagebox.showerror(self._t('error'), self._t('missing_video'))
                return
            def run_ffmpeg():
                try:
                    out_dir = os.path.dirname(src)
                    base = os.path.splitext(os.path.basename(src))[0]
                    out_path = os.path.join(out_dir, f'{base}_converted.{fmt}')
                    if hasattr(sys, '_MEIPASS'):
                        ffmpeg = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
                        ffprobe = os.path.join(sys._MEIPASS, 'ffprobe.exe')
                    else:
                        ffmpeg = 'ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'
                        ffprobe = 'ffprobe.exe' if os.name == 'nt' else 'ffprobe'
                    cmd_len = [ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', src]
                    result = subprocess.run(cmd_len, capture_output=True, text=True)
                    try:
                        total_sec = float(result.stdout.strip())
                    except Exception:
                        total_sec = None
                    cmd = [ffmpeg, '-y', '-i', src]
                    if res and 'x' in res:
                        cmd += ['-vf', f'scale={res}']
                    if spin_video_audio_bitrate.cget('state') == 'normal' and abr:
                        cmd += ['-b:a', f'{abr}k']
                    cmd += [out_path, '-progress', 'pipe:1', '-nostats']
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                    last_percent = 0
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        if 'out_time_ms=' in line and total_sec:
                            ms = int(line.strip().split('=')[1])
                            sec = ms / 1_000_000
                            percent = int((sec / total_sec) * 100)
                            if percent > 100:
                                percent = 100
                            if percent != last_percent:
                                win.after(0, video_update_progress, percent)
                                last_percent = percent
                        elif 'progress=end' in line:
                            win.after(0, video_update_progress, 100)
                            break
                    proc.wait()
                    if proc.returncode == 0:
                        win.after(0, lambda: messagebox.showinfo(self._t('success'), self._t('conversion_done').format(file=out_path)))
                    else:
                        win.after(0, lambda: messagebox.showerror(self._t('error'), self._t('conversion_failed').format(error='')))
                except Exception as e:
                    win.after(0, lambda: messagebox.showerror(self._t('error'), self._t('conversion_failed').format(error=e)))
                win.after(0, video_update_progress, 0)
            threading.Thread(target=run_ffmpeg, daemon=True).start()

        btn_video_convert = tk.Button(tab_video, text=self._t('convert'), command=convert_video)
        btn_video_convert.pack(pady=16)

    def _set_language(self, lang):
        self.language = lang
        self._save_language()
        self._refresh_ui()

    def _felulet(self):
        pady = 4
        self.cimke_url = tk.Label(self, text=self._t('video_url'))
        self.cimke_url.pack(anchor='w', padx=10, pady=(10,0))
        self.mezo_url = tk.Entry(self, width=50)
        self.mezo_url.pack(padx=10, pady=(0,pady))
        self.mezo_url.bind('<KeyRelease>', lambda e: self.felbontasok())

        self.cimke_mod = tk.Label(self, text=self._t('download_mode'))
        self.cimke_mod.pack(anchor='w', padx=10)
        self.mod_valaszto = ttk.Combobox(self, values=[self._t('video_audio'), self._t('audio_only'), self._t('video_only')], state='readonly')
        self.mod_valaszto.current(0)
        self.mod_valaszto.pack(padx=10, pady=(0,pady))
        self.mod_valaszto.bind('<<ComboboxSelected>>', lambda e: self.felbontasok())

        self.cimke_felbontas = tk.Label(self, text=self._t('resolution'))
        self.cimke_felbontas.pack(anchor='w', padx=10)
        self.felbontas_valaszto = ttk.Combobox(self, values=[self._t('please_choose')], state='disabled', width=40)
        self.felbontas_valaszto.pack(padx=10, pady=(0,pady))
        self.felbontas_valaszto.bind('<<ComboboxSelected>>', self._felbontas_kivalasztva)
        self.kivalasztott_felbontas = None

        self.cimke_hangfelbontas = tk.Label(self, text=self._t('audio_quality'))
        self.cimke_hangfelbontas.pack(anchor='w', padx=10)
        self.hangfelbontas_valaszto = ttk.Combobox(self, values=[self._t('please_choose')], state='disabled', width=40)
        self.hangfelbontas_valaszto.pack(padx=10, pady=(0,4))
        self.hangfelbontas_valaszto.bind('<<ComboboxSelected>>', self._hangfelbontas_kivalasztva)
        self.kivalasztott_hangfelbontas = None

        self.gomb_kimenet = tk.Button(self, text=self._t('select_output'), command=self.kimenet)
        self.gomb_kimenet.pack(padx=10, pady=(0,4))

        self.gomb_lejatszas = tk.Button(self, text=self._t('play'), command=self.lejatszas)
        self.gomb_lejatszas.pack(padx=10, pady=(0,4))

        self.gomb_letoltes = tk.Button(self, text=self._t('download_choose_folder'), command=self.letoltes)
        self.gomb_letoltes.pack(padx=10, pady=(0,4))

        self.cimke_allapot = tk.Label(self, text='')
        self.cimke_allapot.pack(anchor='w', padx=10)
        self.sav = ttk.Progressbar(self, orient='horizontal', length=370, mode='determinate')
        self.sav.pack(padx=10, pady=(0,4))
        self.szazalek_label = tk.Label(self, text='0%')
        self.szazalek_label.pack(anchor='w', padx=10)
        self.cimke_statusz = tk.Label(self, text='')
        self.cimke_statusz.pack(anchor='w', padx=10)

    def lejatszas(self):
        import subprocess
        url = self.mezo_url.get().strip()
        if not url:
            messagebox.showwarning(self._t('error'), self._t('missing_url'))
            return
        mod = self.mod_valaszto.get()
        ffplay_path = 'ffplay.exe'
        if hasattr(sys, '_MEIPASS'):
            ffplay_path = os.path.join(sys._MEIPASS, 'ffplay.exe')
        ydl_opts = {'quiet': True, 'skip_download': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                stream_url = None
                def is_original_audio(fmt):
                    lang = fmt.get('language') or ''
                    if lang.lower() in ['original', 'source', 'main', 'hun', 'eng', 'en', 'hu']:
                        return True
                    note = (fmt.get('format_note') or '').lower()
                    if 'original' in note or 'source' in note or 'main' in note or 'hun' in note or 'eng' in note:
                        return True
                    return False
                if mod == self._t('video_audio'):
                    for f in info.get('formats', []):
                        if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url') and is_original_audio(f):
                            stream_url = f['url']
                            break
                    if not stream_url:
                        for f in info.get('formats', []):
                            if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                                stream_url = f['url']
                                break
                    if not stream_url:
                        stream_url = info.get('url')
                elif mod == self._t('audio_only'):
                    for f in info.get('formats', []):
                        if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('url') and is_original_audio(f):
                            stream_url = f['url']
                            break
                    if not stream_url:
                        for f in info.get('formats', []):
                            if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('url'):
                                stream_url = f['url']
                                break
                elif mod == self._t('video_only'):
                    for f in info.get('formats', []):
                        if f.get('vcodec') != 'none' and f.get('acodec') == 'none' and f.get('url'):
                            stream_url = f['url']
                            break
                if not stream_url:
                    messagebox.showerror(self._t('error'), 'Nem található megfelelő stream URL!')
                    return
                args = [ffplay_path, '-autoexit']
                if mod == self._t('audio_only'):
                    args += ['-vn']
                elif mod == self._t('video_only'):
                    args += ['-an']
                args.append(stream_url)
                subprocess.Popen(args)
        except Exception as e:
            messagebox.showerror(self._t('error'), f"ffplay stream hiba: {str(e)}")
    def _felbontas_kivalasztva(self, event=None):
        valasztott = self.felbontas_valaszto.get()
        self.kivalasztott_felbontas = valasztott

    def _hangfelbontas_kivalasztva(self, event=None):
        valasztott = self.hangfelbontas_valaszto.get()
        self.kivalasztott_hangfelbontas = valasztott

    def _refresh_ui(self):
        self.title(self._t('title'))
        self._create_menu()
        self.cimke_url.config(text=self._t('video_url'))
        self.cimke_mod.config(text=self._t('download_mode'))
        current_mode = self.mod_valaszto.get()
        modes = [self._t('video_audio'), self._t('audio_only'), self._t('video_only')]
        self.mod_valaszto['values'] = modes
        if current_mode not in modes:
            self.mod_valaszto.set(modes[0])
        else:
            self.mod_valaszto.set(current_mode)
        self.cimke_felbontas.config(text=self._t('resolution'))
        self.cimke_hangfelbontas.config(text=self._t('audio_quality'))
        if not self.mezo_url.get().strip():
            self.felbontas_valaszto['values'] = [self._t('resolutions_need_url')]
            self.felbontas_valaszto.set(self._t('resolutions_need_url'))
            self.felbontas_valaszto.config(state='disabled')
            self.hangfelbontas_valaszto['values'] = ['']
            self.hangfelbontas_valaszto.set('')
            self.hangfelbontas_valaszto.config(state='disabled')
        self.gomb_kimenet.config(text=self._t('select_output'))
        self.gomb_lejatszas.config(text=self._t('play'))
        if not self.kimeneti_mappa:
            self.gomb_letoltes.config(text=self._t('download_choose_folder'))
        else:
            self.gomb_letoltes.config(text=self._t('download'))

    def felbontasok(self):
        url = self.mezo_url.get().strip()
        if not url:
            self.felbontas_valaszto['values'] = [self._t('please_choose')]
            self.felbontas_valaszto.set(self._t('please_choose'))
            self.felbontas_valaszto.config(state='disabled')
            self.hangfelbontas_valaszto['values'] = [self._t('please_choose')]
            self.hangfelbontas_valaszto.set(self._t('please_choose'))
            self.hangfelbontas_valaszto.config(state='disabled')
            return
        self.felbontas_valaszto['values'] = [self._t('fetching_resolutions')]
        self.felbontas_valaszto.set(self._t('fetching_resolutions'))
        self.felbontas_valaszto.config(state='disabled')
        self.hangfelbontas_valaszto['values'] = ['']
        self.hangfelbontas_valaszto.set('')
        self.hangfelbontas_valaszto.config(state='disabled')
        self.update_idletasks()
        def formatok():
            try:
                ffmpeg_path = 'ffmpeg.exe'
                if hasattr(sys, '_MEIPASS'):
                    ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
                ydl_opts = {'quiet': True, 'skip_download': True, 'ffmpeg_location': ffmpeg_path}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                formatok_lista = info.get('formats', [])
                video_res = []
                audio_res = []
                self.video_itag_map = {}
                self.audio_itag_map = {}
                for f in formatok_lista:
                    if f.get('vcodec') != 'none' and f.get('height') and f.get('format_id'):
                        res = f.get('format_note') or (str(f.get('height')) + 'p')
                        itag = f.get('format_id')
                        ext = f.get('ext')
                        fps = f.get('fps')
                        label = f"{res} ({itag}) [{ext}, {fps}fps]" if fps else f"{res} ({itag}) [{ext}]"
                        if label and itag and label not in video_res:
                            video_res.append(label)
                            self.video_itag_map[label] = itag
                for f in formatok_lista:
                    if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('format_id'):
                        abr = f.get('abr')
                        itag = f.get('format_id')
                        ext = f.get('ext')
                        acodec = f.get('acodec')
                        label = f"{int(abr)} kbps ({itag}) [{ext}, {acodec}]" if abr and acodec else f"{int(abr)} kbps ({itag}) [{ext}]"
                        if label and itag and label not in audio_res:
                            audio_res.append(label)
                            self.audio_itag_map[label] = itag
                mod = self.mod_valaszto.get()
                video_audio = self._t('video_audio')
                audio_only = self._t('audio_only')
                video_only = self._t('video_only')
                if mod == video_audio:
                    if video_res:
                        self.felbontas_valaszto['values'] = [self._t('please_choose')] + video_res
                        self.felbontas_valaszto.set(self._t('please_choose'))
                        self.felbontas_valaszto.config(state='readonly')
                        self.kivalasztott_felbontas = None
                        self.update_idletasks()
                    else:
                        self.felbontas_valaszto['values'] = [self._t('no_resolution')]
                        self.felbontas_valaszto.set(self._t('no_resolution'))
                        self.felbontas_valaszto.config(state='disabled')
                        self.update_idletasks()
                    if audio_res:
                        self.hangfelbontas_valaszto['values'] = [self._t('please_choose')] + audio_res
                        self.hangfelbontas_valaszto.set(self._t('please_choose'))
                        self.hangfelbontas_valaszto.config(state='readonly')
                        self.kivalasztott_hangfelbontas = None
                        self.update_idletasks()
                    else:
                        self.hangfelbontas_valaszto['values'] = ['']
                        self.hangfelbontas_valaszto.set('')
                        self.hangfelbontas_valaszto.config(state='disabled')
                        self.update_idletasks()
                elif mod == video_only:
                    if video_res:
                        self.felbontas_valaszto['values'] = [self._t('please_choose')] + video_res
                        self.felbontas_valaszto.set(self._t('please_choose'))
                        self.felbontas_valaszto.config(state='readonly')
                        self.kivalasztott_felbontas = None
                        self.update_idletasks()
                    else:
                        self.felbontas_valaszto['values'] = [self._t('no_resolution')]
                        self.felbontas_valaszto.set(self._t('no_resolution'))
                        self.felbontas_valaszto.config(state='disabled')
                        self.update_idletasks()
                    self.hangfelbontas_valaszto['values'] = [self._t('please_choose')]
                    self.hangfelbontas_valaszto.set(self._t('please_choose'))
                    self.hangfelbontas_valaszto.config(state='disabled')
                    self.kivalasztott_hangfelbontas = None
                    self.update_idletasks()
                elif mod == audio_only:
                    if audio_res:
                        self.hangfelbontas_valaszto['values'] = [self._t('please_choose')] + audio_res
                        self.hangfelbontas_valaszto.set(self._t('please_choose'))
                        self.hangfelbontas_valaszto.config(state='readonly')
                        self.kivalasztott_hangfelbontas = None
                        self.update_idletasks()
                    else:
                        self.hangfelbontas_valaszto['values'] = [self._t('please_choose')]
                        self.hangfelbontas_valaszto.set(self._t('please_choose'))
                        self.hangfelbontas_valaszto.config(state='disabled')
                        self.kivalasztott_hangfelbontas = None
                        self.update_idletasks()
                    self.felbontas_valaszto['values'] = [self._t('please_choose')]
                    self.felbontas_valaszto.set(self._t('please_choose'))
                    self.felbontas_valaszto.config(state='disabled')
                    self.kivalasztott_felbontas = None
                    self.update_idletasks()
            except Exception:
                self.felbontas_valaszto['values'] = [self._t('invalid_url')]
                self.felbontas_valaszto.set(self._t('invalid_url'))
                self.felbontas_valaszto.config(state='disabled')
                self.hangfelbontas_valaszto['values'] = ['']
                self.hangfelbontas_valaszto.set('')
                self.hangfelbontas_valaszto.config(state='disabled')
        threading.Thread(target=formatok, daemon=True).start()

    def kimenet(self):
        mappa = filedialog.askdirectory(title=self._t('select_output'))
        if mappa:
            self.kimeneti_mappa = mappa
            self.gomb_letoltes.config(text=self._t('download'))

    def letoltes(self):
        url = self.mezo_url.get().strip()
        if not url:
            messagebox.showwarning(self._t('error'), self._t('missing_url'))
            return
        if not self.kimeneti_mappa:
            messagebox.showwarning(self._t('error'), self._t('missing_folder'))
            return
        mod = self.mod_valaszto.get()
        felbontas = self.kivalasztott_felbontas if self.kivalasztott_felbontas else (self.felbontas_valaszto.get() if self.felbontas_valaszto['state'] == 'readonly' else None)
        hangfelbontas = self.kivalasztott_hangfelbontas if self.kivalasztott_hangfelbontas else (self.hangfelbontas_valaszto.get() if self.hangfelbontas_valaszto['state'] == 'readonly' else None)
        video_itag = getattr(self, 'video_itag_map', {}).get(felbontas) if felbontas else None
        audio_itag = getattr(self, 'audio_itag_map', {}).get(hangfelbontas) if hangfelbontas else None
        missing_video = (mod == self._t('video_audio') or mod == self._t('video_only')) and (not felbontas or felbontas == self._t('please_choose') or not video_itag)
        missing_audio = (mod == self._t('video_audio') or mod == self._t('audio_only')) and (not hangfelbontas or hangfelbontas == self._t('please_choose') or not audio_itag)
        def is_original_audio_label(label):
            if not label:
                return False
            l = label.lower()
            return any(x in l for x in ['original', 'source', 'main', 'hun', 'eng', 'en', 'hu'])
        if not missing_audio and (mod == self._t('video_audio') or mod == self._t('audio_only')):
            audio_labels = list(getattr(self, 'audio_itag_map', {}).keys())
            orig_labels = [lbl for lbl in audio_labels if is_original_audio_label(lbl)]
            if len(audio_labels) > 1 and orig_labels and hangfelbontas and not is_original_audio_label(hangfelbontas):
                def use_selected():
                    ablak.destroy()
                    self.sav['value'] = 0
                    self.szazalek_label.config(text='0%')
                    self.cimke_statusz.config(text=self._t('start_download'))
                    threading.Thread(target=self.folyamat, args=(url, mod, video_itag, audio_itag), daemon=True).start()
                def use_original():
                    ablak.destroy()
                    orig_label = orig_labels[0]
                    orig_audio_itag = getattr(self, 'audio_itag_map', {}).get(orig_label)
                    threading.Thread(target=self.folyamat, args=(url, mod, video_itag, orig_audio_itag), daemon=True).start()
                ablak = tk.Toplevel(self)
                ablak.title('Szinkronizált hangsáv')
                ablak.geometry('400x140')
                msg = f"A kiválasztott hangsáv valószínűleg szinkronizált.\nSzeretnéd inkább az eredeti hangsávval letölteni?\n\nKiválasztott: {hangfelbontas}\nEredeti: {orig_labels[0]}"
                label = tk.Label(ablak, text=msg, wraplength=380)
                label.pack(pady=10)
                gomb1 = tk.Button(ablak, text='Maradjon a kiválasztott', command=use_selected)
                gomb1.pack(side='left', padx=30, pady=10)
                gomb2 = tk.Button(ablak, text='Eredeti hangsávval', command=use_original)
                gomb2.pack(side='right', padx=30, pady=10)
                return
        if missing_video or missing_audio:
            def dont_download():
                valaszt_ablak.destroy()
            def download_default():
                valaszt_ablak.destroy()
                self.sav['value'] = 0
                self.szazalek_label.config(text='0%')
                self.cimke_statusz.config(text=self._t('start_download'))
                threading.Thread(target=self.folyamat, args=(url, mod, None, None), daemon=True).start()
            valaszt_ablak = tk.Toplevel(self)
            valaszt_ablak.title(self._t('missing_choice_title'))
            valaszt_ablak.geometry('350x120')
            uzenet = ''
            if missing_video and missing_audio:
                uzenet = self._t('missing_both')
            elif missing_video:
                uzenet = self._t('missing_video')
            elif missing_audio:
                uzenet = self._t('missing_audio')
            label = tk.Label(valaszt_ablak, text=uzenet, wraplength=320)
            label.pack(pady=10)
            gomb1 = tk.Button(valaszt_ablak, text='OK', command=dont_download)
            gomb1.pack(side='left', padx=30, pady=10)
            gomb2 = tk.Button(valaszt_ablak, text=self._t('continue_default'), command=download_default)
            gomb2.pack(side='right', padx=30, pady=10)
            return
        self.sav['value'] = 0
        self.szazalek_label.config(text='0%')
        self.cimke_statusz.config(text=self._t('start_download'))
        threading.Thread(target=self.folyamat, args=(url, mod, video_itag, audio_itag), daemon=True).start()

    def folyamat(self, url, mod, video_itag, audio_itag):
        def horog(d):
            def update_gui():
                if d.get('status') == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate')
                    downloaded = d.get('downloaded_bytes')
                    if total and downloaded:
                        szazalek_ertek = int(downloaded / total * 100)
                    else:
                        szazalek = d.get('_percent_str', '0.0%').replace('%','').strip()
                        try:
                            szazalek_ertek = int(float(szazalek))
                        except:
                            szazalek_ertek = 0
                    self.sav['value'] = szazalek_ertek
                    self.szazalek_label.config(text=f"{szazalek_ertek}%")
                    sebesseg = d.get('speed')
                    ido = d.get('eta')
                    sebesseg_szoveg = f'{sebesseg/1024:.2f} KB/s' if sebesseg else ''
                    ido_szoveg = f'{ido} s' if ido else ''
                    self.cimke_statusz.config(text=f"{self._t('speed')}: {sebesseg_szoveg} | {self._t('remaining_time')}: {ido_szoveg}")
                elif d.get('status') == 'finished':
                    self.sav['value'] = 100
                    self.szazalek_label.config(text="100%")
                    self.cimke_statusz.config(text=self._t('download_complete'))
            self.after(0, update_gui)
        ffmpeg_path = 'ffmpeg.exe'
        if hasattr(sys, '_MEIPASS'):
            ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')

        beallitasok = {
            'outtmpl': f'{self.kimeneti_mappa}/%(title)s.%(ext)s',
            'progress_hooks': [horog],
            'ffmpeg_location': ffmpeg_path,
        }
        video_audio = self._t('video_audio')
        audio_only = self._t('audio_only')
        video_only = self._t('video_only')
        def is_original_audio_fmt(fmt):
            lang = fmt.get('language') or ''
            if lang.lower() in ['original', 'source', 'main', 'hun', 'eng', 'en', 'hu']:
                return True
            note = (fmt.get('format_note') or '').lower()
            if 'original' in note or 'source' in note or 'main' in note or 'hun' in note or 'eng' in note:
                return True
            return False
        if mod == video_audio:
            if video_itag and audio_itag:
                beallitasok['format'] = f"{video_itag}+{audio_itag}"
            elif video_itag:
                beallitasok['format'] = f"{video_itag}"
            elif audio_itag:
                beallitasok['format'] = f"bestaudio/{audio_itag}"
            else:
                try:
                    with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        orig_audio_itag = None
                        for f in info.get('formats', []):
                            if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('format_id') and is_original_audio_fmt(f):
                                orig_audio_itag = f.get('format_id')
                                break
                        if orig_audio_itag:
                            beallitasok['format'] = f"bestvideo+{orig_audio_itag}/best"
                        else:
                            beallitasok['format'] = "bestvideo+bestaudio/best"
                except Exception:
                    beallitasok['format'] = "bestvideo+bestaudio/best"
        elif mod == audio_only:
            if audio_itag:
                beallitasok['format'] = f"{audio_itag}"
            else:
                try:
                    with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        orig_audio_itag = None
                        for f in info.get('formats', []):
                            if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('format_id') and is_original_audio_fmt(f):
                                orig_audio_itag = f.get('format_id')
                                break
                        if orig_audio_itag:
                            beallitasok['format'] = orig_audio_itag
                        else:
                            beallitasok['format'] = "bestaudio/best"
                except Exception:
                    beallitasok['format'] = "bestaudio/best"
        elif mod == video_only:
            if video_itag:
                beallitasok['format'] = f'{video_itag}'
            else:
                beallitasok['format'] = 'bestvideo'
        try:
            with yt_dlp.YoutubeDL(beallitasok) as ydl:
                ydl.download([url])
            messagebox.showinfo(self._t('success'), self._t('download_finished'))
        except Exception as e:
            messagebox.showerror(self._t('error'), f"{self._t('error')}: {str(e)}")

def main():
    app = LetoltoTk()
    app.mainloop()

if __name__ == '__main__':
    main()