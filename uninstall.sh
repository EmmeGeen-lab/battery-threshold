#!/bin/sh
set -eu
as_root() { if [ "$(id -u)" -eq 0 ]; then "$@"; elif command -v sudo >/dev/null 2>&1; then sudo "$@"; elif command -v doas >/dev/null 2>&1; then doas "$@"; else exit 1; fi; }

if [ -d /run/systemd/system ] && command -v systemctl >/dev/null 2>&1; then
    as_root systemctl disable --now battery-threshold.service || true
    as_root rm -f /etc/systemd/system/battery-threshold.service
    as_root rm -f /usr/lib/systemd/system-sleep/battery-threshold
    as_root systemctl daemon-reload
elif command -v rc-update >/dev/null 2>&1; then
    as_root rc-service battery-threshold stop || true
    as_root rc-update del battery-threshold default || true
    as_root rm -f /etc/init.d/battery-threshold
elif command -v update-rc.d >/dev/null 2>&1; then
    as_root update-rc.d -f battery-threshold remove || true
    as_root rm -f /etc/init.d/battery-threshold
fi
as_root rm -f /usr/local/bin/battery-threshold /etc/default/battery-threshold
as_root rm -rf /usr/local/lib/battery-threshold
as_root rm -f /usr/local/share/applications/battery-threshold.desktop
as_root rm -f /usr/local/share/icons/hicolor/scalable/apps/battery-threshold.svg
as_root rm -f /usr/share/polkit-1/actions/io.github.battery-threshold.policy
echo "Battery Threshold removed."
