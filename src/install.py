import os
import sys
from pathlib import Path

APP_NAME = "HyprChan"
TARGET_SCRIPT_NAME = "main.py"


def get_paths():
    current_dir = Path(__file__).resolve().parent

    src_target = current_dir / "src" / TARGET_SCRIPT_NAME
    root_target = current_dir / TARGET_SCRIPT_NAME

    if src_target.exists():
        return current_dir, src_target
    elif root_target.exists():
        return current_dir, root_target

    return current_dir, None


def add_xdg_autostart(exec_path: Path):
    autostart_dir = Path.home() / ".config" / "autostart"
    autostart_dir.mkdir(parents=True, exist_ok=True)

    desktop_file = autostart_dir / f"{APP_NAME.lower()}.desktop"
    python_bin = sys.executable

    content = f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Comment=HyprChan Autostart
Exec={python_bin} "{exec_path}"
Path={exec_path.parent}
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
"""

    with open(desktop_file, "w", encoding="utf-8") as f:
        f.write(content)

    desktop_file.chmod(0o755)

    print(f"[+] Added XDG Autostart entry: {desktop_file}")


def main():
    print("=== HyprChan Installer ===")
    _, target_script = get_paths()

    if target_script is None:
        print(
            f"[!] Error: {TARGET_SCRIPT_NAME} not found neither in root nor in 'src/'!"
        )
        return

    add_xdg_autostart(target_script)
    print(f"[✓] Target script bound to: {target_script}")
    print("\n[✓] Autostart configuration complete!")


if __name__ == "__main__":
    main()
