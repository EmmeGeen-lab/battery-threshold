Name:           battery-threshold
Version:        0.1.0
Release:        0.beta1%{?dist}
Summary:        Graphical battery charge threshold control
License:        GPL-3.0-or-later
URL:            https://github.com/EmmeGeen-lab/battery-threshold
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz
Requires:       python3
Requires:       python3-tkinter
Requires:       polkit

%description
A small desktop-independent interface for setting and restoring the Linux
charge_control_end_threshold value.

%prep
%setup -q

%install
mkdir -p %{buildroot}/usr/bin %{buildroot}/usr/lib/battery-threshold %{buildroot}/usr/lib/systemd/system %{buildroot}/usr/lib/systemd/system-sleep %{buildroot}/usr/share/applications %{buildroot}/usr/share/icons/hicolor/scalable/apps %{buildroot}/usr/share/polkit-1/actions
install -m 755 src/battery_threshold.py %{buildroot}/usr/bin/battery-threshold
install -m 755 src/battery-threshold-helper src/battery-threshold-restore %{buildroot}/usr/lib/battery-threshold/
install -m 644 services/battery-threshold.service %{buildroot}/usr/lib/systemd/system/
install -m 755 services/battery-threshold-sleep %{buildroot}/usr/lib/systemd/system-sleep/battery-threshold
install -m 644 data/battery-threshold.desktop %{buildroot}/usr/share/applications/
install -m 644 data/battery-threshold.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 644 data/io.github.battery-threshold.policy %{buildroot}/usr/share/polkit-1/actions/

%post
if [ ! -r /etc/default/battery-threshold ]; then
    CURRENT=70; for FILE in /sys/class/power_supply/BAT*/charge_control_end_threshold; do if [ -r "$FILE" ]; then CURRENT=$(cat "$FILE"); break; fi; done
    mkdir -p /etc/default; printf 'CHARGE_LIMIT=%s\n' "$CURRENT" > /etc/default/battery-threshold
fi
systemctl daemon-reload || true
systemctl enable --now battery-threshold.service || true

%preun
if [ "$1" -eq 0 ]; then systemctl disable --now battery-threshold.service || true; fi

%postun
systemctl daemon-reload || true
if [ "$1" -eq 0 ]; then rm -f /etc/default/battery-threshold; fi

%files
%license LICENSE
%doc README.md README.it.md COMPATIBILITY.md
/usr/bin/battery-threshold
/usr/lib/battery-threshold/
/usr/lib/systemd/system/battery-threshold.service
/usr/lib/systemd/system-sleep/battery-threshold
/usr/share/applications/battery-threshold.desktop
/usr/share/icons/hicolor/scalable/apps/battery-threshold.svg
/usr/share/polkit-1/actions/io.github.battery-threshold.policy

%changelog
* Sun Sep 13 2026 Marco Z. - 0.1.0-0.beta1
- Initial public beta.
