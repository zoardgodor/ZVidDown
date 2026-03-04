from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QLineEdit, QComboBox, QProgressBar, QTabWidget, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
import os
from core.translations import TranslationManager
from core.converter import AudioConverter, VideoConverter


class ConverterWorker(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, task_type, *args, **kwargs):
        super().__init__()
        self.task_type = task_type
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            if self.task_type == 'audio':
                converter = AudioConverter(progress_callback=self.progress.emit)
                result = converter.convert(*self.args, **self.kwargs)
                self.finished.emit(result)
            elif self.task_type == 'video':
                converter = VideoConverter(progress_callback=self.progress.emit)
                result = converter.convert(*self.args, **self.kwargs)
                self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ConverterWindow(QMainWindow):
    
    def __init__(self, translations: TranslationManager):
        super().__init__()
        self.translations = translations
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(self.translations.get('converter'))
        self.setGeometry(100, 100, 500, 550)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        
        audio_tab = QWidget()
        audio_layout = QVBoxLayout()
        
        audio_file_label = QLabel(self.translations.get('select_audio_file'))
        audio_layout.addWidget(audio_file_label)
        
        audio_file_layout = QHBoxLayout()
        self.audio_file_input = QLineEdit()
        self.audio_file_button = QPushButton(self.translations.get('browse'))
        self.audio_file_button.clicked.connect(self.select_audio_file)
        audio_file_layout.addWidget(self.audio_file_input)
        audio_file_layout.addWidget(self.audio_file_button)
        audio_layout.addLayout(audio_file_layout)
        
        self.audio_bitrate_label = QLabel(self.translations.get('current_bitrate'))
        audio_layout.addWidget(self.audio_bitrate_label)
        
        audio_format_label = QLabel(self.translations.get('target_format'))
        audio_layout.addWidget(audio_format_label)
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(['mp3', 'ogg', 'm4a', 'aac', 'opus', 'wav', 'flac'])
        audio_layout.addWidget(self.audio_format_combo)
        
        audio_bitrate_target_label = QLabel(self.translations.get('target_bitrate'))
        audio_layout.addWidget(audio_bitrate_target_label)
        self.audio_bitrate_input = QLineEdit()
        audio_layout.addWidget(self.audio_bitrate_input)
        
        progress_label = QLabel(self.translations.get('progress'))
        audio_layout.addWidget(progress_label)
        self.audio_progress = QProgressBar()
        audio_layout.addWidget(self.audio_progress)
        self.audio_percent_label = QLabel('0%')
        audio_layout.addWidget(self.audio_percent_label)
        
        self.audio_convert_button = QPushButton(self.translations.get('convert'))
        self.audio_convert_button.clicked.connect(self.convert_audio)
        audio_layout.addWidget(self.audio_convert_button)
        
        audio_layout.addStretch()
        audio_tab.setLayout(audio_layout)
        tabs.addTab(audio_tab, self.translations.get('audio_converter'))
        
        video_tab = QWidget()
        video_layout = QVBoxLayout()
        
        video_file_label = QLabel(self.translations.get('select_video_file'))
        video_layout.addWidget(video_file_label)
        
        video_file_layout = QHBoxLayout()
        self.video_file_input = QLineEdit()
        self.video_file_button = QPushButton(self.translations.get('browse'))
        self.video_file_button.clicked.connect(self.select_video_file)
        video_file_layout.addWidget(self.video_file_input)
        video_file_layout.addWidget(self.video_file_button)
        video_layout.addLayout(video_file_layout)
        
        self.video_resolution_label = QLabel(self.translations.get('current_resolution'))
        video_layout.addWidget(self.video_resolution_label)
        
        video_resolution_target_label = QLabel(self.translations.get('target_resolution'))
        video_layout.addWidget(video_resolution_target_label)
        self.video_resolution_combo = QComboBox()
        self.video_resolution_combo.addItems(['1920x1080', '1280x720', '854x480', '640x360', '320x240'])
        video_layout.addWidget(self.video_resolution_combo)
        
        video_format_label = QLabel(self.translations.get('target_format'))
        video_layout.addWidget(video_format_label)
        self.video_format_combo = QComboBox()
        self.video_format_combo.addItems(['mp4', 'mkv', 'webm', 'avi', 'mov', 'flv'])
        video_layout.addWidget(self.video_format_combo)
        
        self.video_audio_bitrate_label = QLabel(self.translations.get('audio_bitrate'))
        video_layout.addWidget(self.video_audio_bitrate_label)
        self.video_audio_bitrate_input = QLineEdit()
        self.video_audio_bitrate_input.setEnabled(False)
        video_layout.addWidget(self.video_audio_bitrate_input)
        
        self.video_fps_label = QLabel(self.translations.get('current_fps'))
        video_layout.addWidget(self.video_fps_label)
        self.video_fps_input = QLineEdit()
        self.video_fps_input.setEnabled(False)
        video_layout.addWidget(self.video_fps_input)
        
        video_progress_label = QLabel(self.translations.get('progress'))
        video_layout.addWidget(video_progress_label)
        self.video_progress = QProgressBar()
        video_layout.addWidget(self.video_progress)
        self.video_percent_label = QLabel('0%')
        video_layout.addWidget(self.video_percent_label)
        
        self.video_convert_button = QPushButton(self.translations.get('convert'))
        self.video_convert_button.clicked.connect(self.convert_video)
        video_layout.addWidget(self.video_convert_button)
        
        video_layout.addStretch()
        video_tab.setLayout(video_layout)
        tabs.addTab(video_tab, self.translations.get('video_converter'))
        
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
    
    def select_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.translations.get('select_audio_file'),
            '',
            "Audio files (*.mp3 *.ogg *.m4a *.wav *.flac *.aac *.opus);;All files (*.*)"
        )
        if file_path:
            self.audio_file_input.setText(file_path)
            self.show_audio_bitrate(file_path)
    
    def show_audio_bitrate(self, file_path):
        try:
            converter = AudioConverter()
            bitrate = converter.get_audio_bitrate(file_path)
            if bitrate:
                self.audio_bitrate_label.setText(f"{self.translations.get('current_bitrate')}: {bitrate} kbps")
                self.audio_bitrate_input.setText(str(bitrate))
            else:
                self.audio_bitrate_label.setText(f"{self.translations.get('current_bitrate')}: {self.translations.get('no_audio')}")
        except Exception:
            self.audio_bitrate_label.setText(f"{self.translations.get('current_bitrate')}: {self.translations.get('error')}")
    
    def convert_audio(self):
        src = self.audio_file_input.text().strip()
        fmt = self.audio_format_combo.currentText()
        br = self.audio_bitrate_input.text().strip()
        
        if not src or not os.path.isfile(src):
            QMessageBox.critical(self, self.translations.get('error'), self.translations.get('invalid_audio_file'))
            return
        
        if not fmt:
            QMessageBox.critical(self, self.translations.get('error'), self.translations.get('no_target_format'))
            return
        
        self.audio_convert_button.setEnabled(False)
        
        self.worker = ConverterWorker('audio', src, fmt, br if br else None)
        self.worker.progress.connect(self.update_audio_progress)
        self.worker.finished.connect(self.on_audio_conversion_finished)
        self.worker.error.connect(self.on_audio_conversion_error)
        self.worker.start()
    
    def update_audio_progress(self, percent):
        self.audio_progress.setValue(percent)
        self.audio_percent_label.setText(f'{percent}%')
    
    def on_audio_conversion_finished(self, output_file):
        self.audio_convert_button.setEnabled(True)
        self.audio_progress.setValue(0)
        self.audio_percent_label.setText('0%')
        QMessageBox.information(
            self,
            self.translations.get('success'),
            self.translations.get('conversion_done').format(file=output_file)
        )
    
    def on_audio_conversion_error(self, error_msg):
        self.audio_convert_button.setEnabled(True)
        self.audio_progress.setValue(0)
        self.audio_percent_label.setText('0%')
        QMessageBox.critical(
            self,
            self.translations.get('error'),
            self.translations.get('conversion_failed').format(error=error_msg)
        )
    
    def select_video_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.translations.get('select_video_file'),
            '',
            "Video files (*.mp4 *.mkv *.webm *.avi *.mov *.flv *.wmv);;All files (*.*)"
        )
        if file_path:
            self.video_file_input.setText(file_path)
            self.show_video_info(file_path)
    
    def show_video_info(self, file_path):
        try:
            converter = VideoConverter()
            info = converter.get_video_info(file_path)
            
            if info.get('resolution'):
                self.video_resolution_label.setText(f"{self.translations.get('current_resolution')}: {info['resolution']}")
            else:
                self.video_resolution_label.setText(f"{self.translations.get('current_resolution')}: {self.translations.get('no_audio')}")
            
            if info.get('audio_bitrate'):
                self.video_audio_bitrate_label.setText(f"{self.translations.get('audio_bitrate')}: {info['audio_bitrate']} kbps")
                self.video_audio_bitrate_input.setEnabled(True)
                self.video_audio_bitrate_input.setText(str(info['audio_bitrate']))
            else:
                self.video_audio_bitrate_label.setText(f"{self.translations.get('audio_bitrate')}: {self.translations.get('no_audio')}")
                self.video_audio_bitrate_input.setEnabled(False)
                self.video_audio_bitrate_input.setText('')
            
            if info.get('fps'):
                self.video_fps_label.setText(f"{self.translations.get('current_fps')}: {info['fps']}")
                self.video_fps_input.setEnabled(True)
                self.video_fps_input.setText(str(int(info['fps'])))
            else:
                self.video_fps_label.setText(f"{self.translations.get('current_fps')}: {self.translations.get('no_audio')}")
                self.video_fps_input.setEnabled(False)
                self.video_fps_input.setText('')
        except Exception:
            self.video_resolution_label.setText(f"{self.translations.get('current_resolution')}: {self.translations.get('error')}")
            self.video_audio_bitrate_label.setText(f"{self.translations.get('audio_bitrate')}: {self.translations.get('error')}")
            self.video_fps_label.setText(f"{self.translations.get('current_fps')}: {self.translations.get('error')}")
    
    def convert_video(self):
        src = self.video_file_input.text().strip()
        fmt = self.video_format_combo.currentText()
        res = self.video_resolution_combo.currentText()
        abr = self.video_audio_bitrate_input.text().strip()
        fps = self.video_fps_input.text().strip()
        
        if not src or not os.path.isfile(src):
            QMessageBox.critical(self, self.translations.get('error'), self.translations.get('invalid_video_file'))
            return
        
        if not fmt:
            QMessageBox.critical(self, self.translations.get('error'), self.translations.get('no_target_format'))
            return
        
        self.video_convert_button.setEnabled(False)
        
        self.worker = ConverterWorker(
            'video',
            src, fmt,
            res if res else None,
            abr if abr else None,
            fps if fps else None
        )
        self.worker.progress.connect(self.update_video_progress)
        self.worker.finished.connect(self.on_video_conversion_finished)
        self.worker.error.connect(self.on_video_conversion_error)
        self.worker.start()
    
    def update_video_progress(self, percent):
        self.video_progress.setValue(percent)
        self.video_percent_label.setText(f'{percent}%')
    
    def on_video_conversion_finished(self, output_file):
        self.video_convert_button.setEnabled(True)
        self.video_progress.setValue(0)
        self.video_percent_label.setText('0%')
        QMessageBox.information(
            self,
            self.translations.get('success'),
            self.translations.get('conversion_done').format(file=output_file)
        )
    
    def on_video_conversion_error(self, error_msg):
        self.video_convert_button.setEnabled(True)
        self.video_progress.setValue(0)
        self.video_percent_label.setText('0%')
        QMessageBox.critical(
            self,
            self.translations.get('error'),
            self.translations.get('conversion_failed').format(error=error_msg)
        )
