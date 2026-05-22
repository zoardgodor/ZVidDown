import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from core.fftools import get_ff_tools
from core.version import APP_NAME, APP_VERSION, GITHUB_REPOSITORY


class UpdateError(Exception):
    pass


class Updater:
    GITHUB_API_BASE = "https://api.github.com/repos"
    FFMPEG_VERSION_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip.ver"
    FFMPEG_ARCHIVE_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    def __init__(self):
        self.ff_tools = get_ff_tools()
        self.runtime_dir = self._get_runtime_dir()
        self.is_frozen = bool(getattr(sys, "frozen", False))
        self.is_windows = os.name == "nt"
        self.is_linux = sys.platform.startswith("linux")
        self.user_agent = f"{APP_NAME}/{APP_VERSION}"

    @staticmethod
    def _get_runtime_dir():
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    @staticmethod
    def _normalize_version(version):
        if not version:
            return ()
        clean = version.strip().lower()
        clean = clean.lstrip("v")
        parts = re.findall(r"\d+", clean)
        return tuple(int(part) for part in parts)

    def _is_newer_version(self, latest_version, current_version):
        return self._normalize_version(latest_version) > self._normalize_version(current_version)

    def _request_text(self, url):
        request = Request(url, headers={"User-Agent": self.user_agent, "Accept": "application/json"})
        try:
            with urlopen(request, timeout=30) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except (HTTPError, URLError) as exc:
            raise UpdateError(f"Network request failed: {exc}") from exc

    def _request_json(self, url):
        return json.loads(self._request_text(url))

    def _download_file(self, url, destination):
        request = Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urlopen(request, timeout=60) as response, open(destination, "wb") as file_handle:
                shutil.copyfileobj(response, file_handle)
        except (HTTPError, URLError) as exc:
            raise UpdateError(f"Download failed: {exc}") from exc

    def _run_command(self, command, cwd=None):
        try:
            completed = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
            )
            return completed.stdout.strip()
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            stdout = (exc.stdout or "").strip()
            message = stderr or stdout or str(exc)
            raise UpdateError(message) from exc

    def _requirements_path(self):
        path = os.path.join(self.runtime_dir, "requirements.txt")
        return path if os.path.isfile(path) else None

    def _load_upgradable_requirements(self):
        requirements_path = self._requirements_path()
        if not requirements_path:
            return []

        packages = []
        with open(requirements_path, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                package_name = re.split(r"[<>=!~\[]", line, maxsplit=1)[0].strip()
                if not package_name:
                    continue
                if package_name.lower() == "pyside6":
                    continue
                packages.append(package_name)
        return packages

    def _get_latest_release(self, repository):
        return self._request_json(f"{self.GITHUB_API_BASE}/{repository}/releases/latest")

    def _is_directory_writable(self, directory):
        try:
            with tempfile.NamedTemporaryFile(dir=directory, delete=True):
                return True
        except OSError:
            return False

    def _select_app_asset(self, release):
        assets = release.get("assets", [])
        if self.is_windows:
            zip_asset = None
            installer_asset = None
            for asset in assets:
                name = asset.get("name", "")
                if name.endswith("_WIN64.zip"):
                    zip_asset = asset
                elif name.endswith("_WIN64_installer.exe"):
                    installer_asset = asset
            if self._is_directory_writable(self.runtime_dir) and zip_asset:
                return zip_asset, "portable_zip"
            if installer_asset:
                return installer_asset, "installer"
            if zip_asset:
                return zip_asset, "portable_zip"
        if self.is_linux:
            for asset in assets:
                name = asset.get("name", "")
                if name.endswith(".AppImage"):
                    return asset, "appimage"
        return None, None

    def _find_ffmpeg_binaries(self, extracted_dir):
        for root, _, files in os.walk(extracted_dir):
            if "ffmpeg.exe" in files and "ffprobe.exe" in files:
                return os.path.join(root, "ffmpeg.exe"), os.path.join(root, "ffprobe.exe")
        raise UpdateError("Downloaded ffmpeg archive does not contain ffmpeg.exe and ffprobe.exe.")

    def _get_current_ffmpeg_version(self):
        ffmpeg_path = self.ff_tools.get_ffmpeg()
        if not ffmpeg_path or not os.path.isfile(ffmpeg_path):
            return None
        try:
            output = self._run_command([ffmpeg_path, "-version"])
        except UpdateError:
            return None
        first_line = output.splitlines()[0] if output else ""
        match = re.search(r"ffmpeg version\s+([^\s]+)", first_line)
        return match.group(1) if match else None

    def get_update_summary(self):
        summary = {
            "app_version": APP_VERSION,
            "ffmpeg_version": self._get_current_ffmpeg_version(),
            "yt_dlp_version": self._get_yt_dlp_version(),
            "mode": "frozen" if self.is_frozen else "source",
        }
        return summary

    def _get_yt_dlp_version(self):
        try:
            import yt_dlp
        except Exception:
            return None
        version_module = getattr(yt_dlp, "version", None)
        if version_module is not None and hasattr(version_module, "__version__"):
            return version_module.__version__
        return getattr(yt_dlp, "__version__", None)

    def check_app_update(self):
        release = self._get_latest_release(GITHUB_REPOSITORY)
        latest_version = release.get("tag_name") or release.get("name") or APP_VERSION
        latest_version = latest_version.lstrip("v")
        update_available = self._is_newer_version(latest_version, APP_VERSION)
        asset, asset_mode = self._select_app_asset(release)
        return {
            "current_version": APP_VERSION,
            "latest_version": latest_version,
            "update_available": update_available,
            "release_url": release.get("html_url"),
            "asset": asset,
            "asset_mode": asset_mode,
            "release": release,
        }

    def update_ffmpeg(self):
        if not self.is_windows:
            return {
                "checked": False,
                "updated": False,
                "message": "Automatic ffmpeg binary update is currently implemented for Windows builds.",
            }

        current_version = self._get_current_ffmpeg_version()
        latest_version = self._request_text(self.FFMPEG_VERSION_URL).strip()
        if current_version and not self._is_newer_version(latest_version, current_version):
            return {
                "checked": True,
                "updated": False,
                "current_version": current_version,
                "latest_version": latest_version,
                "message": "ffmpeg is already up to date.",
            }

        with tempfile.TemporaryDirectory(prefix="zviddown-ffmpeg-") as temp_dir:
            archive_path = os.path.join(temp_dir, "ffmpeg-release-essentials.zip")
            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            self._download_file(self.FFMPEG_ARCHIVE_URL, archive_path)
            with zipfile.ZipFile(archive_path, "r") as archive:
                archive.extractall(extract_dir)
            ffmpeg_src, ffprobe_src = self._find_ffmpeg_binaries(extract_dir)
            ffmpeg_dst = os.path.join(self.runtime_dir, "ffmpeg.exe")
            ffprobe_dst = os.path.join(self.runtime_dir, "ffprobe.exe")
            shutil.copy2(ffmpeg_src, ffmpeg_dst)
            shutil.copy2(ffprobe_src, ffprobe_dst)

        self.ff_tools.refresh_tool_paths()
        return {
            "checked": True,
            "updated": True,
            "current_version": current_version,
            "latest_version": latest_version,
            "message": f"ffmpeg updated to {latest_version}.",
        }

    def update_pip_packages(self):
        if self.is_frozen:
            return {
                "checked": False,
                "updated": False,
                "message": "Bundled builds carry Python packages inside the app. They update when the app itself updates.",
            }

        updated_steps = []
        packages = self._load_upgradable_requirements()

        self._run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], cwd=self.runtime_dir)
        updated_steps.append("pip")

        if packages:
            self._run_command(
                [sys.executable, "-m", "pip", "install", "--upgrade", *packages],
                cwd=self.runtime_dir,
            )
            updated_steps.extend(packages)

        return {
            "checked": True,
            "updated": True,
            "updated_steps": updated_steps,
            "message": "Python packages were upgraded with pip. PySide6 is intentionally skipped while the GUI is running.",
        }

    def schedule_app_self_update(self):
        if not self.is_frozen:
            return {
                "updated": False,
                "restart_required": False,
                "message": "Source mode does not self-update automatically. Pull new code or download a new release.",
            }

        app_update = self.check_app_update()
        if not app_update["update_available"]:
            return {
                "updated": False,
                "restart_required": False,
                "message": "Application is already up to date.",
                "latest_version": app_update["latest_version"],
            }

        asset = app_update["asset"]
        asset_mode = app_update["asset_mode"]
        if not asset:
            raise UpdateError("No suitable release asset was found for this platform.")

        temp_root = tempfile.mkdtemp(prefix="zviddown-app-update-")
        asset_name = asset["name"]
        downloaded_asset = os.path.join(temp_root, asset_name)
        self._download_file(asset["browser_download_url"], downloaded_asset)

        if self.is_windows and asset_mode == "portable_zip":
            return self._schedule_windows_portable_update(downloaded_asset, app_update["latest_version"])
        if self.is_windows and asset_mode == "installer":
            return self._schedule_windows_installer(downloaded_asset, app_update["latest_version"])
        if self.is_linux and asset_mode == "appimage":
            return self._schedule_linux_appimage_update(downloaded_asset, app_update["latest_version"])

        raise UpdateError("Unsupported update mode for this platform.")

    def _schedule_windows_portable_update(self, archive_path, latest_version):
        staging_dir = tempfile.mkdtemp(prefix="zviddown-portable-")
        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(staging_dir)

        extracted_root = staging_dir
        entries = [entry for entry in os.listdir(staging_dir) if os.path.isdir(os.path.join(staging_dir, entry))]
        if len(entries) == 1:
            extracted_root = os.path.join(staging_dir, entries[0])

        app_executable = sys.executable
        script_path = os.path.join(tempfile.gettempdir(), "zviddown_apply_update.ps1")
        script_content = f"""
$targetPid = {os.getpid()}
$sourceDir = "{extracted_root}"
$targetDir = "{self.runtime_dir}"
$targetExe = "{app_executable}"

while (Get-Process -Id $targetPid -ErrorAction SilentlyContinue) {{
    Start-Sleep -Milliseconds 400
}}

Copy-Item -Path (Join-Path $sourceDir '*') -Destination $targetDir -Recurse -Force
Start-Process -FilePath $targetExe
"""
        with open(script_path, "w", encoding="utf-8") as handle:
            handle.write(script_content.strip() + "\n")

        subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", script_path],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return {
            "updated": True,
            "restart_required": True,
            "latest_version": latest_version,
            "message": f"Update to {latest_version} has been prepared and will be applied after exit.",
        }

    def _schedule_windows_installer(self, installer_path, latest_version):
        script_path = os.path.join(tempfile.gettempdir(), "zviddown_launch_installer.ps1")
        script_content = f"""
$targetPid = {os.getpid()}
$installer = "{installer_path}"

while (Get-Process -Id $targetPid -ErrorAction SilentlyContinue) {{
    Start-Sleep -Milliseconds 400
}}

Start-Process -FilePath $installer
"""
        with open(script_path, "w", encoding="utf-8") as handle:
            handle.write(script_content.strip() + "\n")

        subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", script_path],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return {
            "updated": True,
            "restart_required": True,
            "latest_version": latest_version,
            "message": f"Installer for version {latest_version} has been prepared and will open after exit.",
        }

    def _schedule_linux_appimage_update(self, downloaded_appimage, latest_version):
        target_path = os.path.abspath(sys.executable)
        replacement_path = f"{target_path}.new"
        shutil.copy2(downloaded_appimage, replacement_path)
        os.chmod(replacement_path, os.stat(replacement_path).st_mode | stat.S_IEXEC)

        script_path = os.path.join(tempfile.gettempdir(), "zviddown_apply_update.sh")
        script_content = f"""#!/bin/sh
TARGET_PID={os.getpid()}
TARGET_PATH="{target_path}"
REPLACEMENT_PATH="{replacement_path}"

while kill -0 "$TARGET_PID" 2>/dev/null; do
    sleep 1
done

mv "$REPLACEMENT_PATH" "$TARGET_PATH"
chmod +x "$TARGET_PATH"
"$TARGET_PATH" >/dev/null 2>&1 &
"""
        with open(script_path, "w", encoding="utf-8") as handle:
            handle.write(script_content)
        os.chmod(script_path, os.stat(script_path).st_mode | stat.S_IEXEC)

        subprocess.Popen(["sh", script_path])
        return {
            "updated": True,
            "restart_required": True,
            "latest_version": latest_version,
            "message": f"AppImage update to {latest_version} has been prepared and will be applied after exit.",
        }

    def run_startup_maintenance(self, update_app=True, update_ffmpeg=True, update_pip=True):
        report = {
            "summary": self.get_update_summary(),
            "steps": [],
            "restart_required": False,
            "errors": [],
        }

        if update_ffmpeg:
            try:
                ffmpeg_result = self.update_ffmpeg()
                report["steps"].append(("ffmpeg", ffmpeg_result))
            except Exception as exc:
                report["errors"].append(f"ffmpeg: {exc}")

        if update_pip:
            try:
                pip_result = self.update_pip_packages()
                report["steps"].append(("pip", pip_result))
            except Exception as exc:
                report["errors"].append(f"pip: {exc}")

        if update_app:
            try:
                app_result = self.schedule_app_self_update()
                report["steps"].append(("app", app_result))
                report["restart_required"] = report["restart_required"] or app_result.get("restart_required", False)
            except Exception as exc:
                report["errors"].append(f"app: {exc}")

        return report
