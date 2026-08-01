import os
import sys
from pathlib import Path

APP_NAME = "HyprChan"
TARGET_SCRIPT_NAME = "main.py"

def get_paths():
    current_dir = Path(__file__).resolve().parent
    target_path = current_dir / TARGET_SCRIPT_NAME
    return current_dir, target_path

def add_xdg_autostart(exec_path: Path):
    autostart_dir = Path.home() / ".config" / "autostart"
    autostart_dir.mkdir(parents=True, exist_ok=True)
    
    desktop_file = autostart_dir / f"{APP_NAME.lower()}.desktop"
    python_bin = sys.executable

    content = f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Comment=HyprChan Autostart
Exec={python_bin} {exec_path}
Path={exec_path.parent}
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
"""
    
    with open(desktop_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[+] Added XDG Autostart entry: {desktop_file}")

def main():
    print("=== HyprChan Installer ===")
    _, target_script = get_paths()
    
    if not target_script.exists():
        print(f"[!] Error: {TARGET_SCRIPT_NAME} not found!")
        return

    add_xdg_autostart(target_script)
    print("\n[✓] Autostart configuration complete!")

if __name__ == "__main__":
    main()