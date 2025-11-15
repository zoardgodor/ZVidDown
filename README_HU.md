# ZVidDown – Videó Letöltő

Ez egy egyszerű, grafikus felületű videóletöltő alkalmazás, amellyel YouTube és más támogatott oldalakról tölthetsz le videót, hangot vagy csak videót.

## Fő funkciók

- Videó + hang letöltése
- Csak hang (mp3) letöltése
- Csak videó letöltése
- Felbontás választás (elérhető opciók)
- Kimeneti mappa kiválasztása
- Letöltési folyamat kijelzése
- Széleskörű weboldal támogatás (YouTube, Videa, stb.)

## Technológiák

- Python 3
- Tkinter (grafikus felület)
- yt-dlp (videóletöltés)
- ffmpeg, ffprobe (médiafeldolgozás)

## Telepítés és futtatás

### 1. Előre lefordított verzió (ajánlott)

Ha nem szeretnél semmit telepíteni, használd a mellékelt `ZVidDown.exe` vagy a rendszerszintű telepítéshez a `ZVidDown_installer.exe` fájlt.

1. Töltsd le a `ZVidDown.exe`-t vagy a `ZVidDown_installer.exe`-t.
2. Futtasd a fájlt (telepítő esetén kövesd az utasításokat).
3. Az ffmpeg.exe és az ffprobe.exe a ZvidDown.exe-nél (sem az installer-nél) nem kell őket telepíteni, mert az exe-be be van csomagolva, és a program magából eléri. de a main.py nél ott kell ezeknek lennie abban a mappában ahol a main.py. van

### 2. Saját build készítése (fejlesztőknek)

Szükséges:
- Python 3
- pip csomagkezelő

Telepítsd a szükséges csomagokat:
```sh
pip install yt-dlp
```
```sh
pip install pyinstaller
```

Majd készítsd el az exe-t a következő paranccsal (lásd `make_exe.txt`):
```sh
pyinstaller --onefile --noconsole --icon=icon.ico --noupx --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." main.py
```

Az elkészült futtatható fájl a `dist` mappában lesz.

## Használat

1. Indítsd el a programot (`ZVidDown.exe` vagy a telepítő által létrehozott parancsikonnal).
2. Illeszd be a letölteni kívánt videó URL-jét.
3. Válaszd ki a letöltési módot (videó+hang, csak hang, csak videó).
4. Válaszd ki a felbontást (ha elérhető).
5. Állítsd be a kimeneti mappát.
6. Kattints a Letöltés gombra.

## Többnyelvűség (nyelvválasztás)

A program több nyelvet is támogat. Alapértelmezés szerint angol és magyar nyelv közül lehet választani.

Nyelvet a jobb felső sarokban található hárompontos (⋮) menüben, a "Language" menüpont alatt lehet választani. A kiválasztott nyelv elmentésre kerül, és a program újraindítás után is megjegyzi.

### Saját vagy további nyelvek hozzáadása

Ha szeretnél további nyelveket hozzáadni/használni, tölsd le a `more_languages.json` nevű fájlt, és rakd abba a mappába, ahol a `main.py` vagy a `ZVidDown.exe` található. (A ZVidDown_installer automatikusan telepíti a more_laungages.json fájlt a program mappájába)

Ha ez a fájl jelen van, a program automatikusan felkínálja a benne szereplő nyelveket is a menüben. Ha nincs, akkor csak az alapértelmezett angol és magyar közül lehet választani.
