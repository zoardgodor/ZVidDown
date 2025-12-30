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
                'audio_only': 'Csak Hang (mp3)',
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
            },
            'en': {
                'title': 'Video Downloader',
                'video_url': 'Video URL:',
                'download_mode': 'Download mode:',
                'video_audio': 'Video + Audio',
                'audio_only': 'Audio Only (mp3)',
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
            }
        }
        self._load_more_languages()
        self.language = 'en'
        self.config_path = self._get_config_path()
        self._load_language()
        self.title(self._t('title'))
        self.geometry('400x340')
        self.resizable(False, False)
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
        menubar.add_cascade(label='⋮', menu=more_menu)

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
        self.felbontas_valaszto = ttk.Combobox(self, values=[self._t('please_choose')], state='disabled')
        self.felbontas_valaszto.pack(padx=10, pady=(0,pady))
        self.felbontas_valaszto.bind('<<ComboboxSelected>>', self._felbontas_kivalasztva)
        self.kivalasztott_felbontas = None

        self.cimke_hangfelbontas = tk.Label(self, text=self._t('audio_quality'))
        self.cimke_hangfelbontas.pack(anchor='w', padx=10)
        self.hangfelbontas_valaszto = ttk.Combobox(self, values=[self._t('please_choose')], state='disabled')
        self.hangfelbontas_valaszto.pack(padx=10, pady=(0,4))
        self.hangfelbontas_valaszto.bind('<<ComboboxSelected>>', self._hangfelbontas_kivalasztva)
        self.kivalasztott_hangfelbontas = None

        self.gomb_kimenet = tk.Button(self, text=self._t('select_output'), command=self.kimenet)
        self.gomb_kimenet.pack(padx=10, pady=(0,4))

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
    def _felbontas_kivalasztva(self, event=None):
        valasztott = self.felbontas_valaszto.get()
        self.kivalasztott_felbontas = valasztott
        print(f"[DEBUG] felbontas_valaszto kiválasztva: {valasztott}")

    def _hangfelbontas_kivalasztva(self, event=None):
        valasztott = self.hangfelbontas_valaszto.get()
        self.kivalasztott_hangfelbontas = valasztott
        print(f"[DEBUG] hangfelbontas_valaszto kiválasztva: {valasztott}")

    def _refresh_ui(self):
        self.title(self._t('title'))
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
        print(f"[DEBUG] letoltes: url={url}, mod={mod}, felbontas={felbontas}, hangfelbontas={hangfelbontas}, video_itag={video_itag}, audio_itag={audio_itag}")
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
        print(f"[DEBUG] folyamat: url={url}, mod={mod}, video_itag={video_itag}, audio_itag={audio_itag}")
        if mod == video_audio:
            if video_itag and audio_itag:
                beallitasok['format'] = f"{video_itag}+{audio_itag}"
            elif video_itag:
                beallitasok['format'] = f"{video_itag}"
            elif audio_itag:
                beallitasok['format'] = f"bestaudio/{audio_itag}"
            else:
                beallitasok['format'] = "bestvideo+bestaudio/best"
        elif mod == audio_only:
            if audio_itag:
                beallitasok['format'] = f"{audio_itag}"
            else:
                beallitasok['format'] = "bestaudio/best"
            beallitasok['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif mod == video_only:
            if video_itag:
                beallitasok['format'] = f'{video_itag}'
            else:
                beallitasok['format'] = 'bestvideo'
        print(f"[DEBUG] yt-dlp beallitasok: {beallitasok}")
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