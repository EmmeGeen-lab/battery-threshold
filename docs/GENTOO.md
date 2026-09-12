# Gentoo and OpenRC

The portable installer includes a native `openrc-run` service and registers it
with the default runlevel through `rc-update`.

Before installation, ensure the system provides:

- Python 3 built with Tk support
- Polkit and `pkexec`
- OpenRC
- either `sudo`, `doas`, or a root shell

Gentoo USE flags and package names may change. Confirm that Tk support works with:

```bash
python3 -c 'import tkinter'
```

Then install from the extracted source archive:

```bash
chmod +x install.sh uninstall.sh
./install.sh
```

Verify registration and the saved threshold:

```bash
rc-update show | grep battery-threshold
rc-service battery-threshold status
cat /sys/class/power_supply/BAT*/charge_control_end_threshold
```
