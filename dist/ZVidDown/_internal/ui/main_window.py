from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QLineEdit, QComboBox, QProgressBar, QFileDialog, QMessageBox, QMenuBar, QMenu)
from PySide6.QtCore import Qt, QThread, Signal
import os
from core.translations import TranslationManager
from core.downloader import VideoDownloader
from config.config import get_config
from ui.converter_window import ConverterWindow


class DownloadWorker(QThread):
    progress = Signal(dict)
    finished = Signal()
    error = Signal(str)
    
    def __init__(self, downloader, url, mode, video_itag, audio_itag):
        super().__init__()
        self.downloader = downloader
        self.url = url
        self.mode = mode
        self.video_itag = video_itag
        self.audio_itag = audio_itag
    
    def run(self):
        try:
            def progress_hook(d):
                self.progress.emit(d)
            
            self.downloader.progress_callback = progress_hook
            self.downloader.download(self.url, self.mode, self.video_itag, self.audio_itag)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class ResolutionFetchWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, downloader, url):
        super().__init__()
        self.downloader = downloader
        self.url = url
    
    def run(self):
        try:
            formats = self.downloader.get_available_formats(self.url)
            self.finished.emit(formats)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    
    def __init__(self, translations: TranslationManager):
        super().__init__()
        self.translations = translations
        self.config = get_config()
        self.selected_output_folder = ''
        self.selected_video_format = None
        self.selected_audio_format = None
        self.video_itag_map = {}
        self.audio_itag_map = {}
        self.converter_window = None
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(self.translations.get('title'))
        self.setGeometry(100, 100, 500, 500)
        
        self.create_menu_bar()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        url_label = QLabel(self.translations.get('video_url'))
        layout.addWidget(url_label)
        self.url_input = QLineEdit()
        self.url_input.textChanged.connect(self.on_url_changed)
        layout.addWidget(self.url_input)
        
        mode_label = QLabel(self.translations.get('download_mode'))
        layout.addWidget(mode_label)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            self.translations.get('video_audio'),
            self.translations.get('audio_only'),
            self.translations.get('video_only')
        ])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        layout.addWidget(self.mode_combo)
        
        video_res_label = QLabel(self.translations.get('resolution'))
        layout.addWidget(video_res_label)
        self.video_res_combo = QComboBox()
        self.video_res_combo.setEnabled(False)
        layout.addWidget(self.video_res_combo)
        
        audio_qual_label = QLabel(self.translations.get('audio_quality'))
        layout.addWidget(audio_qual_label)
        self.audio_qual_combo = QComboBox()
        self.audio_qual_combo.setEnabled(False)
        layout.addWidget(self.audio_qual_combo)
        
        self.folder_button = QPushButton(self.translations.get('select_output'))
        self.folder_button.clicked.connect(self.select_output_folder)
        layout.addWidget(self.folder_button)
        
        
        self.download_button = QPushButton(self.translations.get('download_choose_folder'))
        self.download_button.clicked.connect(self.download)
        layout.addWidget(self.download_button)
        
        self.status_label = QLabel('')
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        self.percent_label = QLabel('0%')
        layout.addWidget(self.percent_label)
        
        self.info_label = QLabel('')
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        central_widget.setLayout(layout)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        more_menu = menubar.addMenu('⋮')
        
        lang_menu = QMenu(self.translations.get('menu_language'), self)
        lang_submenu = more_menu.addMenu(lang_menu)
        
        for lang_code in self.translations.get_available_languages():
            action = lang_submenu.addAction(lang_code)
            action.triggered.connect(lambda checked, lc=lang_code: self.set_language(lc))
        
        converter_action = more_menu.addAction(self.translations.get('converter'))
        converter_action.triggered.connect(self.open_converter)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        more_menu = menubar.addMenu('⋮')
        
        lang_menu = more_menu.addMenu(self.translations.get('menu_language'))
        
        for lang_code in self.translations.get_available_languages():
            action = lang_menu.addAction(lang_code)
            action.triggered.connect(lambda checked, lc=lang_code: self.set_language(lc))
        
        more_menu.addSeparator()
        
        converter_action = more_menu.addAction(self.translations.get('converter'))
        converter_action.triggered.connect(self.open_converter)
    
    def set_language(self, lang_code):
        self.translations.set_language(lang_code)
        self.config.set_language(lang_code)
        self.refresh_ui()
    
    def open_converter(self):
        if self.converter_window is None or not self.converter_window.isVisible():
            self.converter_window = ConverterWindow(self.translations)
        self.converter_window.show()
        self.converter_window.raise_()
    
    def refresh_ui(self):
        self.setWindowTitle(self.translations.get('title'))
    
    def on_url_changed(self):
        if self.url_input.text().strip():
            self.fetch_resolutions()
        else:
            self.video_res_combo.clear()
            self.video_res_combo.setEnabled(False)
            self.audio_qual_combo.clear()
            self.audio_qual_combo.setEnabled(False)
    
    def on_mode_changed(self):
        url = self.url_input.text().strip()
        if url:
            self.fetch_resolutions()
    
    def fetch_resolutions(self):
        url = self.url_input.text().strip()
        if not url:
            return
        
        try:
            downloader = VideoDownloader(self.selected_output_folder)
            self.resolution_worker = ResolutionFetchWorker(downloader, url)
            self.resolution_worker.finished.connect(self.on_resolutions_fetched)
            self.resolution_worker.error.connect(self.on_resolution_error)
            self.resolution_worker.start()
            
            self.status_label.setText(self.translations.get('fetching_resolutions'))
        except Exception as e:
            self.status_label.setText(f"Hiba: {str(e)}")
    
    def on_resolutions_fetched(self, formats):
        self.video_itag_map = formats.get('video_itag_map', {})
        self.audio_itag_map = formats.get('audio_itag_map', {})
        
        mode = self.mode_combo.currentText()
        video_audio = self.translations.get('video_audio')
        audio_only = self.translations.get('audio_only')
        video_only = self.translations.get('video_only')
        
        video_formats = formats.get('video_formats', [])
        audio_formats = formats.get('audio_formats', [])
        video_itag_map = formats.get('video_itag_map', {})
        audio_itag_map = formats.get('audio_itag_map', {})
        
        if mode == video_audio:
            if video_formats:
                self.video_res_combo.clear()
                self.video_res_combo.addItem(self.translations.get('please_choose'), None)
                for label in video_formats:
                    itag = video_itag_map.get(label)
                    self.video_res_combo.addItem(label, itag)
                self.video_res_combo.setEnabled(True)
                self.selected_video_format = None
            else:
                self.video_res_combo.clear()
                self.video_res_combo.addItem(self.translations.get('no_resolution'), None)
                self.video_res_combo.setEnabled(False)
            
            if audio_formats:
                self.audio_qual_combo.clear()
                self.audio_qual_combo.addItem(self.translations.get('please_choose'), None)
                for label in audio_formats:
                    itag = audio_itag_map.get(label)
                    self.audio_qual_combo.addItem(label, itag)
                self.audio_qual_combo.setEnabled(True)
                self.selected_audio_format = None
            else:
                self.audio_qual_combo.clear()
                self.audio_qual_combo.setEnabled(False)
        
        elif mode == video_only:
            if video_formats:
                self.video_res_combo.clear()
                self.video_res_combo.addItem(self.translations.get('please_choose'), None)
                for label in video_formats:
                    itag = video_itag_map.get(label)
                    self.video_res_combo.addItem(label, itag)
                self.video_res_combo.setEnabled(True)
                self.selected_video_format = None
            else:
                self.video_res_combo.clear()
                self.video_res_combo.addItem(self.translations.get('no_resolution'), None)
                self.video_res_combo.setEnabled(False)
            
            self.audio_qual_combo.clear()
            self.audio_qual_combo.setEnabled(False)
        
        elif mode == audio_only:
            if audio_formats:
                self.audio_qual_combo.clear()
                self.audio_qual_combo.addItem(self.translations.get('please_choose'), None)
                for label in audio_formats:
                    itag = audio_itag_map.get(label)
                    self.audio_qual_combo.addItem(label, itag)
                self.audio_qual_combo.setEnabled(True)
                self.selected_audio_format = None
            else:
                self.audio_qual_combo.clear()
                self.audio_qual_combo.setEnabled(False)
            
            self.video_res_combo.clear()
            self.video_res_combo.setEnabled(False)
        
        self.status_label.setText(self.translations.get('ready'))
    
    def on_resolution_error(self, error):
        self.status_label.setText(f"{self.translations.get('error')}: {error}")
        self.video_res_combo.clear()
        self.video_res_combo.addItem(self.translations.get('invalid_url'))
        self.video_res_combo.setEnabled(False)
        self.audio_qual_combo.clear()
        self.audio_qual_combo.setEnabled(False)
    
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            self.translations.get('select_output')
        )
        if folder:
            self.selected_output_folder = folder
            self.download_button.setText(self.translations.get('download'))
    
    
    def download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, self.translations.get('error'), self.translations.get('missing_url'))
            return
        
        if not self.selected_output_folder:
            QMessageBox.warning(self, self.translations.get('error'), self.translations.get('missing_folder'))
            return
        
        raw_mode = self.mode_combo.currentText()
        if raw_mode == self.translations.get('video_audio'):
            mode_code = 'video_audio'
        elif raw_mode == self.translations.get('audio_only'):
            mode_code = 'audio_only'
        elif raw_mode == self.translations.get('video_only'):
            mode_code = 'video_only'
        else:
            mode_code = 'video_audio'
        
        video_itag = self.video_res_combo.currentData()
        audio_itag = self.audio_qual_combo.currentData()

        if mode_code == 'video_audio':
            if not video_itag and not audio_itag:
                ans = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_both'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if ans == QMessageBox.Cancel:
                    return
            elif not video_itag:
                ans = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_video'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if ans == QMessageBox.Cancel:
                    return
            elif not audio_itag:
                ans = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_audio'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if ans == QMessageBox.Cancel:
                    return
        elif mode_code == 'video_only':
            if not video_itag:
                ans = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_video'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if ans == QMessageBox.Cancel:
                    return
        elif mode_code == 'audio_only':
            if not audio_itag:
                ans = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_audio'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if ans == QMessageBox.Cancel:
                    return
        
        video_audio = self.translations.get('video_audio')
        audio_only = self.translations.get('audio_only')
        video_only = self.translations.get('video_only')
        mode = mode_code
        if mode == video_audio:
            if not video_itag and not audio_itag:
                reply = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_both'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if reply == QMessageBox.Cancel:
                    return
            elif not video_itag:
                reply = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_video'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if reply == QMessageBox.Cancel:
                    return
            elif not audio_itag:
                reply = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_audio'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if reply == QMessageBox.Cancel:
                    return
        elif mode == video_only:
            if not video_itag:
                reply = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_video'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if reply == QMessageBox.Cancel:
                    return
        elif mode == audio_only:
            if not audio_itag:
                reply = QMessageBox.question(
                    self,
                    self.translations.get('missing_choice_title'),
                    self.translations.get('missing_audio'),
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if reply == QMessageBox.Cancel:
                    return
        
        self.status_label.setText(self.translations.get('start_download'))
        self.progress_bar.setValue(0)
        self.percent_label.setText('0%')
        
        downloader = VideoDownloader(self.selected_output_folder)
        self.download_worker = DownloadWorker(downloader, url, mode_code, video_itag, audio_itag)
        self.download_worker.progress.connect(self.update_progress)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.error.connect(self.on_download_error)
        self.download_worker.start()
        
        self.download_button.setEnabled(False)
    
    def update_progress(self, d):
        if d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes')
            
            if total and downloaded:
                percent = int(downloaded / total * 100)
            else:
                percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
                try:
                    percent = int(float(percent_str))
                except:
                    percent = 0
            
            self.progress_bar.setValue(percent)
            self.percent_label.setText(f'{percent}%')
            
            speed = d.get('speed')
            eta = d.get('eta')
            
            speed_text = f"{speed / 1024:.2f} KB/s" if speed else ''
            eta_text = f"{eta} s" if eta else ''
            
            self.info_label.setText(
                f"{self.translations.get('speed')}: {speed_text} | {self.translations.get('remaining_time')}: {eta_text}"
            )
        
        elif d.get('status') == 'finished':
            self.progress_bar.setValue(100)
            self.percent_label.setText('100%')
            self.status_label.setText(self.translations.get('download_complete'))
    
    def on_download_finished(self):
        self.download_button.setEnabled(True)
        QMessageBox.information(
            self,
            self.translations.get('success'),
            self.translations.get('download_finished')
        )
    
    def on_download_error(self, error):
        self.download_button.setEnabled(True)
        QMessageBox.critical(
            self,
            self.translations.get('error'),
            f"{self.translations.get('error')}: {error}"
        )
