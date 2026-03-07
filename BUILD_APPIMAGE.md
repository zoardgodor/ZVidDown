# Building AppImage for ZVidDown

## English Version

### Prerequisites

Before building the AppImage, ensure you have the following installed:

- **Python 3.8+** - The programming language
- **PyInstaller** - For creating standalone executables
- **ffmpeg and ffprobe** - Media tools (included in the repository)

### Installation of Dependencies

1. **Install Python packages:**
```bash
pip install -r requirements.txt
```

This will install:
- `PySide6` - GUI framework
- `yt_dlp` - Video downloading library
- `PyInstaller` - Executable builder

2. **Download appimagetool (no installation needed):**

Simply download and use it directly:
```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O /tmp/appimagetool
chmod +x /tmp/appimagetool
```

The appimagetool will be ready at `/tmp/appimagetool`

### Building the AppImage

#### Step 1: Create the Executable with PyInstaller

From the project root directory, run:

```bash
python -m PyInstaller --name ZVidDown_linux --onedir --noconsole --noupx \
  --add-data "config:config" \
  --add-data "core:core" \
  --add-data "ui:ui" \
  main.py
```

This will create a `dist/ZVidDown_linux/` directory containing the standalone executable and all dependencies.

#### Step 2: Build the AppImage

Navigate to the packaging directory and run the build script:

```bash
cd packaging/appimage
bash build_appimage.sh
```

The script will:
- Verify the PyInstaller executable exists
- Copy the executable to the AppDir
- Copy ffmpeg and ffprobe binaries
- Copy the application icon
- Create the AppImage using appimagetool

#### Step 3: AppImage Creation

You can also manually create the AppImage directly with appimagetool:

```bash
cd packaging/appimage
/tmp/appimagetool ZVidDown.AppDir ZVidDown-1.6.AppImage
```

### Output

The final AppImage will be created at:
```
packaging/appimage/ZVidDown-1.6.AppImage
```

This is a portable, self-contained executable that can be distributed and run on any Linux system with a compatible glibc version.

### Troubleshooting

**Error: "Desktop file contains errors"**
- Edit `packaging/appimage/ZVidDown.AppDir/ZVidDown.desktop` to fix any category issues.
- Ensure Categories follow the freedesktop specification.

**appimagetool not found**
- Make sure you downloaded it to `/tmp/appimagetool` as described in the Prerequisites section.
- You can also download it to any other location and use the full path.

**AppImage is too large**
- The size (~74MB) is normal for PySide6 + all dependencies. This is acceptable for distribution.

### Making the AppImage Executable

If needed, make the AppImage executable:
```bash
chmod +x ZVidDown-1.6.AppImage
```

### Running the AppImage

To run the application:
```bash
./ZVidDown-1.6.AppImage
```

Or simply double-click it in a file manager.

---

## Magyar verzió

### Előfeltételek

A AppImage építése előtt győződj meg arról, hogy a következők telepítve vannak:

- **Python 3.8+** - A programozási nyelv
- **PyInstaller** - Önálló végrehajtható fájlok létrehozásához
- **ffmpeg és ffprobe** - Médiaeszközök (a repositoryban vannak)

### A függőségek telepítése

1. **Python csomagok telepítése:**
```bash
pip install -r requirements.txt
```

Ez telepíteni fogja:
- `PySide6` - GUI keretrendszer
- `yt_dlp` - Videó letöltési könyvtár
- `PyInstaller` - Végrehajtható fájl builder

2. **appimagetool letöltése (nincs telepítésre szükség):**

Egyszerűen töltsd le és használd közvetlenül:
```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O /tmp/appimagetool
chmod +x /tmp/appimagetool
```

Az appimagetool készen áll a `/tmp/appimagetool` helyen

### Az AppImage építése

#### 1. lépés: A végrehajtható fájl létrehozása PyInstaller-rel

A projekt gyökérkönyvtárából futtasd:

```bash
python -m PyInstaller --name ZVidDown_linux --onedir --noconsole --noupx \
  --add-data "config:config" \
  --add-data "core:core" \
  --add-data "ui:ui" \
  main.py
```

Ez létrehoz egy `dist/ZVidDown_linux/` könyvtárat, amely a végrehajtható fájlt és az összes függőséget tartalmazza.

#### 2. lépés: Az AppImage építése

Navigálj a csomagolás könyvtárba és futtasd az építő scriptet:

```bash
cd packaging/appimage
bash build_appimage.sh
```

A script a következőket végzi el:
- Ellenőrzi, hogy a PyInstaller végrehajtható fájl létezik
- Másolja a végrehajtható fájlt az AppDir-be
- Másolja az ffmpeg és ffprobe bináris fájlokat
- Másolja az alkalmazás ikonját
- Létrehozza az AppImage-et az appimagetool segítségével

#### 3. lépés: AppImage létrehozása

Közvetlenül módon is létrehozhatod az AppImage-et az appimagetool-lal:

```bash
cd packaging/appimage
/tmp/appimagetool ZVidDown.AppDir ZVidDown-1.6.AppImage
```

### Kimenet

A végső AppImage a következő helyen jön létre:
```
packaging/appimage/ZVidDown-1.6.AppImage
```

Ez egy hordozható, önálló végrehajtható fájl, amely bármely Linux rendszeren terjeszthető és futtatható, amely kompatibilis glibc verzióval rendelkezik.

### Hibaelhárítás

**Hiba: "Desktop file contains errors"**
- Szerkeszd a `packaging/appimage/ZVidDown.AppDir/ZVidDown.desktop` fájlt, hogy javítsd a kategória problémáit.
- Győződj meg arról, hogy a Categories követik a freedesktop specifikációt.

**appimagetool nem található**
- Győződj meg arról, hogy az „Előfeltételek" részben leírtak szerint letöltötted a `/tmp/appimagetool` helyre.
- Tetszőleges más helyre is letöltheted és a teljes útvonalat használhatod.

**Az AppImage túl nagy**
- A méret (~74MB) normális a PySide6 + összes függőség esetén. Ez elfogadható a terjesztéshez.

### Az AppImage végrehajthatóvá tétele

Ha szükséges, tedd a AppImage-et végrehajthatóvá:
```bash
chmod +x ZVidDown-1.6.AppImage
```

### Az AppImage futtatása

Az alkalmazás futtatásához:
```bash
./ZVidDown-1.6.AppImage
```

Vagy egyszerűen kattints rá duplán a fájlkezelőben.
