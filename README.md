# ZVidDown – Video Downloader

This is a simple graphical video downloader application that allows you to download video, audio, or just video from YouTube and other supported sites.

## Main Features

- Download video + audio
- Download audio only (mp3)
- Download video only
- Resolution selection (available options)
- Choose output folder
- Download progress display
- Wide website support (YouTube, Videa, etc.)

## Technologies

- Python 3
- Tkinter (GUI)
- yt-dlp (video downloading)
- ffmpeg, ffprobe (media processing)

## Installation and Usage

### 1. Pre-built Version (Recommended)

If you don't want to install anything, use the included `ZVidDown.exe` or for system-level installation, use the `ZVidDown_installer.exe` file.

1. Download `ZVidDown.exe` or `ZVidDown_installer.exe`.
2. Run the file (for the installer, follow the instructions).
3. You do not need to install ffmpeg.exe and ffprobe.exe for ZVidDown.exe (or the installer), as they are bundled inside the exe and the program can access them internally. For main.py, these files must be present in the same folder as main.py.

### 2. Build Your Own (For Developers)

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

Then build the exe with the following command (see `make_exe.txt`):
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

## Multilanguage (Language Selection)

The program supports multiple languages. By default, you can choose between English and Hungarian.

You can select the language in the three-dot (⋮) menu at the top right, under the "Language" menu. The selected language will be saved and remembered after restarting the program.

### Adding or Using More Languages

If you want to add/use more languages, download the `more_languages.json` file and place it in the same folder as `main.py` or `ZVidDown.exe`. (The ZVidDown_installer automatically installs the more_languages.json file into the program folder.)

If this file is present, the program will automatically offer the languages listed in it in the menu. If not, only the default English and Hungarian will be available.
