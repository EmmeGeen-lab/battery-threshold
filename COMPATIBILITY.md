# Hardware compatibility

Battery Threshold requires the standard Linux power-supply attribute
`charge_control_end_threshold`. Distribution support does not guarantee laptop
support: the firmware and kernel driver must expose this attribute.

## Verified

| Vendor | Model | Battery | System | Status |
|---|---|---|---|---|
| ASUS | TUF Gaming A15 FA506IV (`FA506IV_FA506IV`) | BAT1 | iDeal OS 4.4 (Debian/MX), SysVinit 3.14, kernel 7.2.4-4-liquorix-amd64 | DEB 0.1.0 beta 1 verified: GUI change to 65%, then saved and restored at 70% after reboot |

The verified system uses KDE Plasma 6.3.6 on Wayland. The desktop environment
and graphics platform do not normally affect threshold support; the important
parts are the laptop firmware, kernel driver, sysfs attribute and init system.

## How to report a test

Open an issue and include:

```bash
cat /sys/devices/virtual/dmi/id/sys_vendor
cat /sys/devices/virtual/dmi/id/product_name
uname -r
cat /proc/1/comm
ls /sys/class/power_supply/BAT*/charge_control_end_threshold
```

Do not include serial numbers or other unique device identifiers.
