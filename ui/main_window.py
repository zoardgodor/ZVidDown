from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config.config import get_config
from core.downloader import VideoDownloader
from core.translations import TranslationManager
from core.updater import Updater
from core.version import APP_VERSION
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
            def progress_hook(data):
                self.progress.emit(data)

            self.downloader.progress_callback = progress_hook
            self.downloader.download(self.url, self.mode, self.video_itag, self.audio_itag)
            self.finished.emit()
        except Exception as exc:
            self.error.emit(str(exc))


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
        except Exception as exc:
            self.error.emit(str(exc))


class UpdateWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, updater, run_app_update, run_ffmpeg_update, run_pip_update):
        super().__init__()
        self.updater = updater
        self.run_app_update = run_app_update
        self.run_ffmpeg_update = run_ffmpeg_update
        self.run_pip_update = run_pip_update

    def run(self):
        try:
            report = self.updater.run_startup_maintenance(
                update_app=self.run_app_update,
                update_ffmpeg=self.run_ffmpeg_update,
                update_pip=self.run_pip_update,
            )
            self.finished.emit(report)
        except Exception as exc:
            self.error.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self, translations: TranslationManager):
        super().__init__()
        self.translations = translations
        self.config = get_config()
        self.updater = Updater()
        self.selected_output_folder = ''
        self.selected_video_format = None
        self.selected_audio_format = None
        self.video_itag_map = {}
        self.audio_itag_map = {}
        self.converter_window = None
        self.update_worker = None
        self.update_menu = None
        self.check_updates_action = None
        self.version_action = None

        self.init_ui()

        if self.config.get_auto_update_on_startup():
            QTimer.singleShot(1200, self.run_startup_updates)

    def init_ui(self):
        self.setWindowTitle(self.translations.get('title'))
        self.setGeometry(100, 100, 500, 500)

        self.create_menu_bar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        layout.addWidget(QLabel(self.translations.get('video_url')))
        self.url_input = QLineEdit()
        self.url_input.textChanged.connect(self.on_url_changed)
        layout.addWidget(self.url_input)

        layout.addWidget(QLabel(self.translations.get('download_mode')))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            self.translations.get('video_audio'),
            self.translations.get('audio_only'),
            self.translations.get('video_only')
        ])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        layout.addWidget(self.mode_combo)

        layout.addWidget(QLabel(self.translations.get('resolution')))
        self.video_res_combo = QComboBox()
        self.video_res_combo.setEnabled(False)
        layout.addWidget(self.video_res_combo)

        layout.addWidget(QLabel(self.translations.get('audio_quality')))
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
        menubar.clear()
        more_menu = menubar.addMenu('⋮')

        lang_menu = more_menu.addMenu(self.translations.get('menu_language'))
        for lang_code in self.translations.get_available_languages():
            action = lang_menu.addAction(lang_code)
            action.triggered.connect(lambda checked, lc=lang_code: self.set_language(lc))

        more_menu.addSeparator()

        converter_action = more_menu.addAction(self.translations.get('converter'))
        converter_action.triggered.connect(self.open_converter)

        self.update_menu = more_menu.addMenu(self.translations.get('updates'))
        self.check_updates_action = self.update_menu.addAction(self.translations.get('check_updates_now'))
        self.check_updates_action.triggered.connect(self.run_manual_updates)
        self.version_action = self.update_menu.addAction(
            self.translations.get('current_version').format(version=APP_VERSION)
        )
        self.version_action.setEnabled(False)

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
        self.folder_button.setText(self.translations.get('select_output'))
        if self.selected_output_folder:
            self.download_button.setText(self.translations.get('download'))
        else:
            self.download_button.setText(self.translations.get('download_choose_folder'))
        self.create_menu_bar()

    def on_url_changed(self):
        if self.url_input.text().strip():
            self.fetch_resolutions()
            return
        self.video_res_combo.clear()
        self.video_res_combo.setEnabled(False)
        self.audio_qual_combo.clear()
        self.audio_qual_combo.setEnabled(False)

    def on_mode_changed(self):
        if self.url_input.text().strip():
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
        except Exception as exc:
            self.status_label.setText(f"{self.translations.get('error')}: {exc}")

    def on_resolutions_fetched(self, formats):
        self.video_itag_map = formats.get('video_itag_map', {})
        self.audio_itag_map = formats.get('audio_itag_map', {})

        mode = self.mode_combo.currentText()
        video_formats = formats.get('video_formats', [])
        audio_formats = formats.get('audio_formats', [])

        if mode in (self.translations.get('video_audio'), self.translations.get('video_only')):
            self._fill_format_combo(self.video_res_combo, video_formats, self.video_itag_map)
            self.selected_video_format = None
        else:
            self.video_res_combo.clear()
            self.video_res_combo.setEnabled(False)

        if mode in (self.translations.get('video_audio'), self.translations.get('audio_only')):
            self._fill_format_combo(self.audio_qual_combo, audio_formats, self.audio_itag_map)
            self.selected_audio_format = None
        else:
            self.audio_qual_combo.clear()
            self.audio_qual_combo.setEnabled(False)

        self.status_label.setText(self.translations.get('ready'))

    def _fill_format_combo(self, combo, labels, itag_map):
        combo.clear()
        if labels:
            combo.addItem(self.translations.get('please_choose'), None)
            for label in labels:
                combo.addItem(label, itag_map.get(label))
            combo.setEnabled(True)
            return
        combo.addItem(self.translations.get('no_resolution'), None)
        combo.setEnabled(False)

    def on_resolution_error(self, error):
        self.status_label.setText(f"{self.translations.get('error')}: {error}")
        self.video_res_combo.clear()
        self.video_res_combo.addItem(self.translations.get('invalid_url'))
        self.video_res_combo.setEnabled(False)
        self.audio_qual_combo.clear()
        self.audio_qual_combo.setEnabled(False)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.translations.get('select_output'))
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

        mode_code = self._get_mode_code()
        video_itag = self.video_res_combo.currentData()
        audio_itag = self.audio_qual_combo.currentData()

        if not self._confirm_missing_selection(mode_code, video_itag, audio_itag):
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

    def _get_mode_code(self):
        raw_mode = self.mode_combo.currentText()
        if raw_mode == self.translations.get('audio_only'):
            return 'audio_only'
        if raw_mode == self.translations.get('video_only'):
            return 'video_only'
        return 'video_audio'

    def _confirm_missing_selection(self, mode_code, video_itag, audio_itag):
        message_key = None
        if mode_code == 'video_audio':
            if not video_itag and not audio_itag:
                message_key = 'missing_both'
            elif not video_itag:
                message_key = 'missing_video'
            elif not audio_itag:
                message_key = 'missing_audio'
        elif mode_code == 'video_only' and not video_itag:
            message_key = 'missing_video'
        elif mode_code == 'audio_only' and not audio_itag:
            message_key = 'missing_audio'

        if not message_key:
            return True

        answer = QMessageBox.question(
            self,
            self.translations.get('missing_choice_title'),
            self.translations.get(message_key),
            QMessageBox.Ok | QMessageBox.Cancel
        )
        return answer != QMessageBox.Cancel

    def update_progress(self, data):
        if data.get('status') == 'downloading':
            total = data.get('total_bytes') or data.get('total_bytes_estimate')
            downloaded = data.get('downloaded_bytes')

            if total and downloaded:
                percent = int(downloaded / total * 100)
            else:
                percent_str = data.get('_percent_str', '0%').replace('%', '').strip()
                try:
                    percent = int(float(percent_str))
                except ValueError:
                    percent = 0

            self.progress_bar.setValue(percent)
            self.percent_label.setText(f'{percent}%')

            speed = data.get('speed')
            eta = data.get('eta')
            speed_text = f"{speed / 1024:.2f} KB/s" if speed else ''
            eta_text = f"{eta} s" if eta else ''
            self.info_label.setText(
                f"{self.translations.get('speed')}: {speed_text} | {self.translations.get('remaining_time')}: {eta_text}"
            )
            return

        if data.get('status') == 'finished':
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

    def run_startup_updates(self):
        self._start_update_worker(startup_mode=True)

    def run_manual_updates(self):
        self._start_update_worker(startup_mode=False)

    def _start_update_worker(self, startup_mode):
        if self.update_worker and self.update_worker.isRunning():
            return

        self.status_label.setText(self.translations.get('checking_updates'))
        self.check_updates_action.setEnabled(False)
        self.update_worker = UpdateWorker(
            self.updater,
            run_app_update=self.config.get_auto_update_app(),
            run_ffmpeg_update=self.config.get_auto_update_ffmpeg(),
            run_pip_update=self.config.get_auto_update_pip(),
        )
        self.update_worker.finished.connect(lambda report: self.on_updates_finished(report, startup_mode))
        self.update_worker.error.connect(self.on_updates_error)
        self.update_worker.start()

    def on_updates_finished(self, report, startup_mode):
        if self.check_updates_action:
            self.check_updates_action.setEnabled(True)

        messages = []
        updated_anything = False

        for _, step in report.get('steps', []):
            message = step.get('message')
            if message:
                messages.append(message)
            updated_anything = updated_anything or bool(step.get('updated'))

        for error in report.get('errors', []):
            messages.append(error)

        if report.get('restart_required'):
            messages.append(self.translations.get('restart_required'))

        if not messages:
            messages.append(self.translations.get('no_updates_needed'))

        self.status_label.setText(self.translations.get('updates_finished'))

        if startup_mode and not updated_anything and not report.get('errors'):
            return

        QMessageBox.information(
            self,
            self.translations.get('updates'),
            "\n\n".join(messages)
        )

        if report.get('restart_required'):
            self.close()

    def on_updates_error(self, error):
        if self.check_updates_action:
            self.check_updates_action.setEnabled(True)
        self.status_label.setText(f"{self.translations.get('error')}: {error}")
        QMessageBox.critical(
            self,
            self.translations.get('error'),
            f"{self.translations.get('error')}: {error}"
        )
