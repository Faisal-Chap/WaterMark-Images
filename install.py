import os
import shutil
from pathlib import Path

home = str(Path.home())

# Source paths
icon_src = os.path.join("assets", "icon.png")
desktop_src = "imagewatermark.desktop"

# Destination paths
icon_dest = os.path.join(home, ".local", "share", "icons", "imagewatermark.png")
desktop_dest = os.path.join(home, ".local", "share", "applications", "imagewatermark.desktop")

# Copy icon
os.makedirs(os.path.dirname(icon_dest), exist_ok=True)
shutil.copy(icon_src, icon_dest)

# Copy .desktop file
os.makedirs(os.path.dirname(desktop_dest), exist_ok=True)
shutil.copy(desktop_src, desktop_dest)

# Ensure it's executable
os.chmod(desktop_dest, 0o755)

print("✅ Installed! You can now find 'Image Watermark' in your app menu.")
