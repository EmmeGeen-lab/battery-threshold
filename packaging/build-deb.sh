#!/bin/sh
set -eu
ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
STAGE="$ROOT/build/deb/battery-threshold_0.1.0.beta1_all"
DIST="$ROOT/dist"
mkdir -p "$STAGE/DEBIAN" "$STAGE/usr/bin" "$STAGE/usr/lib/battery-threshold" "$STAGE/lib/systemd/system" "$STAGE/usr/lib/systemd/system-sleep" "$STAGE/etc/init.d" "$STAGE/usr/share/applications" "$STAGE/usr/share/icons/hicolor/scalable/apps" "$STAGE/usr/share/polkit-1/actions" "$STAGE/usr/share/doc/battery-threshold" "$DIST"
install -m 644 "$ROOT/packaging/debian/control" "$STAGE/DEBIAN/control"
install -m 755 "$ROOT/packaging/debian/postinst" "$ROOT/packaging/debian/prerm" "$ROOT/packaging/debian/postrm" "$STAGE/DEBIAN/"
install -m 755 "$ROOT/src/battery_threshold.py" "$STAGE/usr/bin/battery-threshold"
install -m 755 "$ROOT/src/battery-threshold-helper" "$ROOT/src/battery-threshold-restore" "$STAGE/usr/lib/battery-threshold/"
install -m 644 "$ROOT/services/battery-threshold.service" "$STAGE/lib/systemd/system/"
install -m 755 "$ROOT/services/battery-threshold-sleep" "$STAGE/usr/lib/systemd/system-sleep/battery-threshold"
install -m 755 "$ROOT/services/battery-threshold.sysv" "$STAGE/etc/init.d/battery-threshold"
install -m 644 "$ROOT/data/battery-threshold.desktop" "$STAGE/usr/share/applications/"
install -m 644 "$ROOT/data/battery-threshold.svg" "$STAGE/usr/share/icons/hicolor/scalable/apps/"
install -m 644 "$ROOT/data/io.github.battery-threshold.policy" "$STAGE/usr/share/polkit-1/actions/"
install -m 644 "$ROOT/README.md" "$ROOT/README.it.md" "$ROOT/COMPATIBILITY.md" "$ROOT/LICENSE" "$STAGE/usr/share/doc/battery-threshold/"
dpkg-deb --root-owner-group --build "$STAGE" "$DIST/battery-threshold_0.1.0.beta1_all.deb"
