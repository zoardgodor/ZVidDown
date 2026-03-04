# ZVidDown – Video Downloader

This is a simple, graphical interface video downloader application with which you can download videos, audio, or just video from thousands of sites.

## Key Features

- Download video + audio
- Download audio only (mp3)
- Download video only
- Resolution selection (available options)
- Output folder selection
- Download progress display
- Built-in converter: convert existing audio and video files to other formats, quality, FPS (bitrate, resolution, etc.)
- Extensive website support

## Technologies

- Python 3
- PySide6 (graphical interface)
- yt-dlp (video downloading)
- ffmpeg, ffprobe (media processing)

## Installation and Running

### 1. Pre-compiled version (recommended)

Find the latest version on the following website: https://github.com/zoardgodor/ZVidDown/releases

1. Download the `ZVidDown_vX.X_WIN64.zip` or the `ZVidDown_vX.X_WIN64_installer.exe`.
2. In the case of ZIP, extract the compressed archive and run it (in the case of installer, follow the instructions).
3. For the `ZVidDown_vX.X_WIN64.zip` version, ffmpeg.exe and ffprobe.exe don't need to be downloaded and placed separately, as they are already pre-installed. However, if you want to run main.py directly, they need to be in the same folder as main.py.

(The Installer was created with the Inno Setup Compiler software)

### 2. Running main.py

Required:
- Python 3
- pip package manager

Install the required packages:
```sh
pip install yt-dlp pyside6
```

Run main.py:
```sh
python main.py
```

### 3. Creating your own build (for developers)

Required:
- Python 3
- pip package manager

Install the required packages:
```sh
pip install yt-dlp pyside6
```
```sh
pip install pyinstaller
```

Then create the exe according to the make_executable.txt file (found in the repository: https://github.com/zoardgodor/ZVidDown/blob/main/make_executable.txt)

The created executable will be in the `dist` folder. Place the ffmpeg.exe, ffplay.exe and ffprobe.exe files next to the ZVidDown.exe!

## Usage

1. Start the program (`ZVidDown.exe` or the shortcut created by the installer).
2. Paste the URL of the video you want to download.
3. Select the download mode (video+audio, audio only, video only).
4. Select the resolution (if available).
5. Set the output folder.
6. Click the Download button.
7. If you want to convert an existing audio or video file, open the "Converter" function from the menu (⋮), select the file, set the desired format and quality, and start the conversion. The converted file will be placed in the original folder.

## License
See: LICENSE.txt
BY INSTALLING AND USING THE PROGRAM, YOU ACCEPT THE LICENSE AGREEMENT.

## Multilingualism (Language Selection)

The program supports multiple languages. By default, you can choose between English and Hungarian.

You can change the language in the three-dot (⋮) menu in the top right corner, under the "Language" menu item. The selected language will be saved, and the program will remember it after restart.

### Adding your own or additional languages

If you want to add/use additional languages, download the file named `more_languages.json` and place it in the folder where `main.py` or `ZVidDown.exe` is located.
In the case of the installer, it installs `ZVidDown.exe` in Program Files. You can place the json there.

If this file is present, the program will automatically offer the languages contained in it in the menu as well. If not, you can only choose between the default English and Hungarian.

The 'more_laungages.json' can also be extended independently.

## Extra Features
- Built-in converter: convert audio and video files to different formats (mp3, ogg, m4a, mp4, mkv, etc.), with audio bitrate and video resolution adjustment options, progress bar and multilingual interface. There's also an FPS changer included.

- Before downloading, you must manually select the video and audio quality. If either is not selected, a window appears with two options: OK (cancels the download) or Continue with default values (downloads bestvideo+bestaudio).
- Audio quality (bitrate/format) can also be selected separately, not just video resolution.
- All captions, warnings and dialog messages are fully translatable. The more_languages.json supports all new text.
- If no video or audio quality is selected, the program does not start automatically, but provides feedback and gives the option to decide.
- Advanced error handling and user feedback in case of missing or incorrect selection.
- The language system and more_languages.json extend to every new interface and message element.

**Created by: Gódor Zoárd, developer of ZLockCore**
