#!/bin/bash

# AppImage Build Script for ZVidDown
# This script builds the ZVidDown AppImage

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "========================================"
echo "ZVidDown AppImage Builder"
echo "========================================"
echo ""

if [ ! -f "$PROJECT_ROOT/dist/ZVidDown_linux/ZVidDown_linux" ]; then
    echo "Error: ZVidDown_linux executable not found in dist/ZVidDown_linux/"
    echo "Please run PyInstaller first:"
    echo "  python -m PyInstaller --name ZVidDown_linux --onedir --noconsole --noupx --add-data 'config:config' --add-data 'core:core' --add-data 'ui:ui' main.py"
    exit 1
fi

echo "✓ Found ZVidDown_linux executable"
echo ""

echo "Copying PyInstaller output to AppDir..."
mkdir -p "$SCRIPT_DIR/ZVidDown.AppDir/ZVidDown"
cp -r "$PROJECT_ROOT/dist/ZVidDown_linux/"* "$SCRIPT_DIR/ZVidDown.AppDir/ZVidDown/" || true

if [ -f "$PROJECT_ROOT/ffmpeg" ]; then
    echo "Copying ffmpeg..."
    cp "$PROJECT_ROOT/ffmpeg" "$SCRIPT_DIR/ZVidDown.AppDir/ZVidDown/"
    chmod +x "$SCRIPT_DIR/ZVidDown.AppDir/ZVidDown/ffmpeg"
fi

if [ -f "$PROJECT_ROOT/ffprobe" ]; then
    echo "Copying ffprobe..."
    cp "$PROJECT_ROOT/ffprobe" "$SCRIPT_DIR/ZVidDown.AppDir/ZVidDown/"
    chmod +x "$SCRIPT_DIR/ZVidDown.AppDir/ZVidDown/ffprobe"
fi

if [ -f "$PROJECT_ROOT/icon.png" ]; then
    echo "Copying icon..."
    cp "$PROJECT_ROOT/icon.png" "$SCRIPT_DIR/ZVidDown.AppDir/"
fi

chmod +x "$SCRIPT_DIR/ZVidDown.AppDir/AppRun"

echo ""
echo "✓ AppDir prepared successfully"
echo ""

if command -v appimagetool &> /dev/null; then
    echo "Building AppImage with appimagetool..."
    cd "$SCRIPT_DIR"
    
    appimagetool -v "ZVidDown.AppDir" "ZVidDown-1.6.AppImage"
    
    echo ""
    echo "✓ AppImage created successfully!"
    echo "AppImage location: $SCRIPT_DIR/ZVidDown-1.6.AppImage"
    echo ""
else
    echo "⚠ appimagetool not found. Install it with:"
    echo "  wget https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage"
    echo "  chmod +x appimagetool-x86_64.AppImage"
    echo "  sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
    echo ""
    echo "AppDir is ready at: $SCRIPT_DIR/ZVidDown.AppDir"
    echo "You can now build the AppImage manually using appimagetool"
fi
