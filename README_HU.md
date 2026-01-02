# ZVidDown – Videó Letöltő

Ez egy egyszerű, grafikus felületű videóletöltő alkalmazás, amellyel több ezer
oldalról tölthetsz le videót, hangot vagy csak videót.

## Fő funkciók

- Videó + hang letöltése
- Csak hang (mp3) letöltése
- Csak videó letöltése
- Felbontás választás (elérhető opciók)
- Kimeneti mappa kiválasztása
- Letöltési folyamat kijelzése
- Beépített lejátszó: videók és hangok előnézete letöltés előtt
- Beépített átváltó: meglévő hang- és videófájlok átkonvertálása más formátumra, minőségre, FPS-re (bitráta, felbontás stb.)
- Széleskörű weboldal támogatás

## Technológiák

- Python 3
- Tkinter (grafikus felület)
- yt-dlp (videóletöltés)
- ffmpeg, ffprobe (médiafeldolgozás)

## Telepítés és futtatás

### 1. Előre lefordított verzió (ajánlott)

Keresd meg a legfrisseb verziót a következő weboldalon: https://github.com/zoardgodor/ZVidDown/releases

1. Töltsd le a `ZVidDown_vX.X_WIN64.zip`-et vagy a `ZVidDown_vX.X_WIN64_installer.exe`-t.
2. A ZIP esetén bonsd ki a tömörített archívumot, és futtasd (telepítő esetén kövesd az utasításokat).
3. Az ffmpeg.exe és az ffprobe.exe a `ZVidDown_vX.X_WIN64.zip`-nél (sem az installer-nél) nem kell őket külön letölteni, berakni, mert már előre be van helyezve. De ha simán a main.py-t szeretnéd tuttatni, ott ezeknek abban a mappában kell lennie ahol a main.py van.

(Az Installer az Inno Setup Compiler nevű szoftverrel készült)

### 2. main.py futtatása

Szükséges:
- Python 3
- pip csomagkezelő

Telepítsd a szükséges csomagokat:
```sh
pip install yt-dlp
```

Futtasd a main.py-t:
```sh
python main.py
```

### 3. Saját build készítése (fejlesztőknek)

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

Majd készítsd el az exe-t a make_executable.txt fájl szerint (a repóban megtalálható: https://github.com/zoardgodor/ZVidDown/blob/main/make_executable.txt)

Az elkészült futtatható fájl a `dist` mappában lesz.

## Használat

1. Indítsd el a programot (`main.exe` vagy a telepítő által létrehozott parancsikonnal).
2. Illeszd be a letölteni kívánt videó URL-jét.
3. Válaszd ki a letöltési módot (videó+hang, csak hang, csak videó).
4. Válaszd ki a felbontást (ha elérhető).
5. Állítsd be a kimeneti mappát.
6. Kattints a Letöltés gombra.
7. Ha szeretnéd előnézetben lejátszani a videót vagy hangot letöltés előtt, használd a beépített lejátszót (Lejátszás gomb).
8. Ha meglévő hang- vagy videófájlt szeretnél átkonvertálni, nyisd meg a menüből (⋮) az "Átváltó" funkciót, válaszd ki a fájlt, állítsd be a kívánt formátumot és minőséget, majd indítsd el az átalakítást. Az átalakított fájl az eredeti mappába kerül.

## Licenc
Lásd: LICENSE.txt
A PROGRAM TELEPÍTÉSÉVEL ÉS HASZNÁLATÁVAL ELOGADJA A LICENCSZERZŐDÉST.

## Többnyelvűség (nyelvválasztás)

A program több nyelvet is támogat. Alapértelmezés szerint angol és magyar nyelv közül lehet választani.

Nyelvet a jobb felső sarokban található hárompontos (⋮) menüben, a "Language" menüpont alatt lehet választani. A kiválasztott nyelv elmentésre kerül, és a program újraindítás után is megjegyzi.

### Saját vagy további nyelvek hozzáadása

Ha szeretnél további nyelveket hozzáadni/használni, tölsd le a `more_languages.json` nevű fájlt, és rakd abba a mappába, ahol a `main.py` vagy a `main.exe` található.
Az installernél a Program Files-ba telepíti a `main.exe`-t. oda lehet behelyezni a json-t.

Ha ez a fájl jelen van, a program automatikusan felkínálja a benne szereplő nyelveket is a menüben. Ha nincs, akkor csak az alapértelmezett angol és magyar közül lehet választani.

A 'more_laungages.json' akár önnállóan is bővíthető.

## Plusz Funkciók
- Beépített lejátszó: videók és hangok előnézete közvetlenül a programban, letöltés előtt.
- Beépített átváltó: hang- és videófájlok átkonvertálása különböző formátumokra (mp3, ogg, m4a, mp4, mkv stb.), hang bitráta és videó felbontás állítási lehetőséggel, állapotsávval és többnyelvű felülettel. FPS változtató is van benne.

- Letöltés előtt kötelező manuálisan kiválasztani a videó és a hang minőségét. Ha valamelyik nincs kiválasztva, egy ablak jelenik meg két opcióval: OK (megszakítja a letöltést) vagy Tovább alapértelmezett értékekkel (bestvideo+bestaudio letöltése).
- A hangminőség (bitráta/formátum) is külön választható, nem csak a videó felbontás.
- Minden felirat, figyelmeztetés és ablaküzenet teljesen fordítható. A more_languages.json minden új szöveget támogat.
- Ha nincs kiválasztva videó vagy hang minőség, a program nem indul el automatikusan, hanem visszajelzést ad és lehetőséget ad a döntésre.
- Fejlettebb hibakezelés és felhasználói visszajelzés hiányzó vagy hibás választás esetén.
- A nyelvi rendszer és a more_languages.json minden új felület- és üzenetelemre kiterjed.

**Készítette: Gódor Zoárd a ZLockCore fejlesztője**
