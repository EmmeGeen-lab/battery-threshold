#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
PREFIX=/usr/local
LIBDIR="$PREFIX/lib/battery-threshold"

as_root() {
    if [ "$(id -u)" -eq 0 ]; then "$@"
    elif command -v sudo >/dev/null 2>&1; then sudo "$@"
    elif command -v doas >/dev/null 2>&1; then doas "$@"
    else echo "Run this installer as root, or install sudo/doas." >&2; exit 1
    fi
}

command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required." >&2; exit 1; }
python3 -c 'import tkinter' >/dev/null 2>&1 || { echo "Python Tkinter support is required." >&2; exit 1; }
command -v pkexec >/dev/null 2>&1 || { echo "Polkit/pkexec is required." >&2; exit 1; }

CURRENT=70
for FILE in /sys/class/power_supply/BAT*/charge_control_end_threshold; do
    if [ -r "$FILE" ]; then CURRENT=$(cat "$FILE"); break; fi
done

as_root install -d -m 755 "$LIBDIR" /usr/local/bin /usr/local/share/applications /usr/local/share/icons/hicolor/scalable/apps /usr/share/polkit-1/actions /etc/default
as_root install -m 755 "$ROOT_DIR/src/battery_threshold.py" /usr/local/bin/battery-threshold
as_root install -m 755 "$ROOT_DIR/src/battery-threshold-helper" "$LIBDIR/"
as_root install -m 755 "$ROOT_DIR/src/battery-threshold-restore" "$LIBDIR/"
as_root install -m 644 "$ROOT_DIR/data/battery-threshold.desktop" /usr/local/share/applications/
as_root install -m 644 "$ROOT_DIR/data/battery-threshold.svg" /usr/local/share/icons/hicolor/scalable/apps/
as_root install -m 644 "$ROOT_DIR/data/io.github.battery-threshold.policy" /usr/share/polkit-1/actions/
as_root sed -i 's|/usr/lib/battery-threshold/|/usr/local/lib/battery-threshold/|' /usr/share/polkit-1/actions/io.github.battery-threshold.policy
as_root "$LIBDIR/battery-threshold-helper" "$CURRENT"

if [ -d /run/systemd/system ] && command -v systemctl >/dev/null 2>&1; then
    as_root install -m 644 "$ROOT_DIR/services/battery-threshold.service" /etc/systemd/system/
    as_root install -d -m 755 /usr/lib/systemd/system-sleep
    as_root install -m 755 "$ROOT_DIR/services/battery-threshold-sleep" /usr/lib/systemd/system-sleep/battery-threshold
    as_root sed -i 's|/usr/lib/battery-threshold/|/usr/local/lib/battery-threshold/|' /etc/systemd/system/battery-threshold.service
    as_root sed -i 's|/usr/lib/battery-threshold/|/usr/local/lib/battery-threshold/|' /usr/lib/systemd/system-sleep/battery-threshold
    as_root systemctl daemon-reload
    as_root systemctl enable --now battery-threshold.service
elif command -v rc-update >/dev/null 2>&1 && command -v rc-service >/dev/null 2>&1; then
    as_root install -m 755 "$ROOT_DIR/services/battery-threshold.openrc" /etc/init.d/battery-threshold
    as_root rc-update add battery-threshold default
    as_root rc-service battery-threshold start
elif command -v update-rc.d >/dev/null 2>&1; then
    as_root install -m 755 "$ROOT_DIR/services/battery-threshold.sysv" /etc/init.d/battery-threshold
    as_root update-rc.d battery-threshold defaults
    as_root /etc/init.d/battery-threshold start
else
    echo "Unsupported init system. Application installed without boot persistence." >&2
    exit 2
fi

echo "Battery Threshold installed successfully."
