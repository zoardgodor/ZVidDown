# ZVidDown – Video Downloader

This is a simple graphical video downloader application that allows you to download video, audio, or just video from YouTube and other supported sites.

## Main Features

- Download video + audio
- Download audio only (mp3)
- Download video only
- Resolution selection (available options)
- Choose output folder
- Download progress display
- Broad website support (YouTube, Videa, etc.)

## Technologies

- Python 3
- Tkinter (GUI)
- yt-dlp (video downloading)
- ffmpeg, ffprobe (media processing)

## Installation and Usage

### 1. Pre-built version (recommended)

Find the latest version here: https://github.com/zoardgodor/ZVidDown/releases

1. Download `ZVidDown.zip` or `ZVidDown_installer.exe`.
2. For the ZIP, extract the archive and run the program (for the installer, follow the instructions).
3. For ZVidDown.exe (and the installer), you do not need to install ffmpeg.exe and ffprobe.exe separately, as they are bundled with the exe and accessible by the program. However, if you want to run main.py directly, these files must be in the same folder as main.py.

(The installer was created using software called Inno Setup Compiler.)

### 2. Running main.py

Requirements:
- Python 3
- pip package manager

Install the required packages:
```sh
pip install yt-dlp
```

Run main.py:
```sh
python main.py
```

### 3. Building your own executable (for developers)

Requirements:
- Python 3
- pip package manager

Install the required packages:
```sh
pip install yt-dlp
```
```sh
pip install pyinstaller
```

Then create the exe with the following command (see `make_exe.txt`):
```sh
pyinstaller --onefile --noconsole --icon=icon.ico --noupx --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." main.py
```

The executable will be in the `dist` folder.

## Usage

1. Start the program (`ZVidDown.exe` or the shortcut created by the installer).
2. Paste the URL of the video you want to download.
3. Select the download mode (video+audio, audio only, video only).
4. Select the resolution (if available).
5. Set the output folder.
6. Click the Download button.

## License
See: LICENSE.txt
BY INSTALLING AND USING THE PROGRAM, YOU ACCEPT THE LICENSE AGREEMENT.

## Multilingual Support (Language Selection)

The program supports multiple languages. By default, you can choose between English and Hungarian.

You can select the language in the menu at the top right corner (⋮), under the "Language" menu. The selected language will be saved and remembered after restarting the program.

### Adding or Using Custom Languages

If you want to add/use more languages, download the `more_languages.json` file and place it in the same folder as `main.py` or `ZVidDown.exe`. (The ZVidDown_installer automatically installs the more_languages.json file into the program folder.)

If this file is present, the program will automatically offer the languages listed in it in the menu. If not, only the default English and Hungarian will be available.

The 'more_languages.json' file can be expanded independently.

## Latest Features and Changes

- Manual selection is now required for both video and audio quality before downloading. If you do not select a quality, a dialog will appear with two options: OK (cancel download) or Continue with default values (downloads with bestvideo+bestaudio).
- The audio quality (bitrate/format) can be selected separately, not just the video resolution.
- All interface texts, warnings, and dialog messages are now fully translatable. The more_languages.json file supports all new texts.
- If you do not select a video or audio quality, the program will not start the download automatically, but will give feedback and let you choose how to proceed.
- Improved error handling and user feedback for missing or invalid selections.
- The language system and more_languages.json have been expanded to cover all new interface elements and messages.

**Created by Zoárd Gódor, developer of ZLockCore**