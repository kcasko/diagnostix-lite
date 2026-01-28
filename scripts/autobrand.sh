#!/bin/bash

set -e

echo "=== DiagnOStiX AutoBranding ==="

BRAND_DIR="/opt/diagnostix/branding"
WALL_DIR="$BRAND_DIR/wallpapers"
PLYMOUTH_THEME="/usr/share/plymouth/themes/diagnostix"
PLYMOUTH_NAME="diagnostix"

BOOT_IMG="$WALL_DIR/boot.png"
LOGIN_IMG="$WALL_DIR/login.png"
DESKTOP_IMG="$WALL_DIR/desktop.png"

echo "Applying desktop wallpaper..."
gsettings set org.gnome.desktop.background picture-uri "file://$DESKTOP_IMG"
gsettings set org.gnome.desktop.background picture-uri-dark "file://$DESKTOP_IMG"

echo "Applying lockscreen wallpaper..."
gsettings set org.gnome.desktop.screensaver picture-uri "file://$LOGIN_IMG"

echo "Creating Plymouth theme directory..."
sudo mkdir -p "$PLYMOUTH_THEME"

echo "Copying boot image to Plymouth theme..."
sudo cp "$BOOT_IMG" "$PLYMOUTH_THEME/boot.png"

echo "Writing Plymouth descriptor..."
sudo tee "$PLYMOUTH_THEME/diagnostix.plymouth" > /dev/null <<EOF
[Plymouth Theme]
Name=DiagnostiX
Description=DiagnostiX Neon Boot
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/diagnostix
ScriptFile=/usr/share/plymouth/themes/diagnostix/diagnostix.script
EOF

echo "Writing Plymouth script..."
sudo tee "$PLYMOUTH_THEME/diagnostix.script" > /dev/null <<EOF
wallpaper_image = Image("boot.png");
wallpaper_sprite = Sprite(wallpaper_image);
wallpaper_sprite.SetZ(-100);
EOF

echo "Registering Plymouth theme..."
sudo update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth "$PLYMOUTH_THEME/diagnostix.plymouth" 100
sudo update-alternatives --set default.plymouth "$PLYMOUTH_THEME/diagnostix.plymouth"

echo "Updating initramfs..."
sudo update-initramfs -u

echo "Fixing permissions..."
sudo chmod -R 755 "$BRAND_DIR"

echo "Branding complete. Reboot to apply."
