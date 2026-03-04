#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication
from core.translations import TranslationManager
from config.config import get_config
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    
    translations = TranslationManager()
    config = get_config()
    
    saved_language = config.get_language()
    if saved_language:
        translations.set_language(saved_language)
    
    window = MainWindow(translations)
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
