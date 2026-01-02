# ZVidDown – Video Downloader

This is a simple graphical video downloader application that allows you to download video, audio, or just video from thousands of websites.

## Main Features

- Download video + audio
- Download audio only (mp3)
- Download video only
- Resolution selection (available options)
- Choose output folder
- Download progress display
- Built-in player for previewing videos and audio
- Built-in converter: convert audio and video files to different formats, FPS and qualities (bitrate, resolution, etc.)
- Broad website support

## Technologies

- Python 3
- Tkinter (GUI)
- yt-dlp (video downloading)
- ffmpeg, ffprobe (media processing)

## Installation and Usage

### 1. Pre-built version (recommended)

Find the latest version here: https://github.com/zoardgodor/ZVidDown/releases

1. Download `ZVidDown_vX.X_WIN64.zip` or `ZVidDown_vX.X_WIN64_installer.exe`.
2. For the ZIP, extract the archive and run the program (for the installer, follow the instructions).
3. For `ZVidDown_vX.X_WIN64.zip` (and the installer), you do not need to install ffmpeg.exe and ffprobe.exe separately, as they are bundled with the exe and accessible by the program. However, if you want to run main.py directly, these files must be in the same folder as main.py.

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

Then create the exe file according to the make_executable.txt file (found in the repository: https://github.com/zoardgodor/ZVidDown/blob/main/make_executable.txt).

The executable will be in the `dist` folder.

## Usage

1. Start the program (`main.exe` or the shortcut created by the installer).
2. Paste the URL of the video you want to download.
3. Select the download mode (video+audio, audio only, video only).
4. Select the resolution (if available).
5. Set the output folder.
6. Click the Download button.
7. To preview a video or audio before downloading, use the built-in player (Play button).
8. To convert an existing audio or video file, open the "Converter" from the menu (⋮), select the file, choose the target format and quality, and start the conversion. The converted file will be saved in the same folder as the original.

## License
See: LICENSE.txt
BY INSTALLING AND USING THE PROGRAM, YOU ACCEPT THE LICENSE AGREEMENT.

## Multilingual Support (Language Selection)

The program supports multiple languages. By default, you can choose between English and Hungarian.

You can select the language in the menu at the top right corner (⋮), under the "Language" menu. The selected language will be saved and remembered after restarting the program.

### Adding or Using Custom Languages

If you want to add/use more languages, download the `more_languages.json` file and place it in the same folder as `main.py` or `main.exe`.
The installer installs `main.exe` in Program Files. You can place the json file there.

If this file is present, the program will automatically offer the languages listed in it in the menu. If not, only the default English and Hungarian will be available.

The 'more_languages.json' file can be expanded independently.

## Plus Features
- Built-in player: preview videos and audio directly in the app before downloading.
- Built-in converter: convert audio and video files to various formats (mp3, ogg, m4a, mp4, mkv, etc.), change audio bitrate and video resolution, with progress bar and multilingual interface. It also includes an FPS changer.

- Manual selection is now required for both video and audio quality before downloading. If you do not select a quality, a dialog will appear with two options: OK (cancel download) or Continue with default values (downloads with bestvideo+bestaudio).
- The audio quality (bitrate/format) can be selected separately, not just the video resolution.
- All interface texts, warnings, and dialog messages are now fully translatable. The more_languages.json file supports all new texts.
- If you do not select a video or audio quality, the program will not start the download automatically, but will give feedback and let you choose how to proceed.
- Improved error handling and user feedback for missing or invalid selections.
- The language system and more_languages.json have been expanded to cover all new interface elements and messages.

**Created by Zoárd Gódor, developer of ZLockCore**