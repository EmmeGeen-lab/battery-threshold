#!/bin/sh
set -eu
ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
TOP="$ROOT/build/rpmbuild"
mkdir -p "$TOP/BUILD" "$TOP/BUILDROOT" "$TOP/RPMS" "$TOP/SOURCES" "$TOP/SPECS" "$TOP/SRPMS" "$ROOT/dist"
install -m 644 "$ROOT/dist/battery-threshold-0.1.0.tar.gz" "$TOP/SOURCES/"
rpmbuild -bb --define "_topdir $TOP" "$ROOT/packaging/rpm/battery-threshold.spec"
install -m 644 "$TOP/RPMS/noarch/battery-threshold-0.1.0-0.beta1.noarch.rpm" "$ROOT/dist/"
