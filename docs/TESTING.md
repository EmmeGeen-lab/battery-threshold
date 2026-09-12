# Testing

## Automated checks

```bash
make check
```

This compiles the Python source, runs unit tests against a temporary fake sysfs
tree, and checks POSIX shell syntax.

## Manual hardware test

1. Record the current threshold.
2. Apply a different safe threshold through the GUI.
3. Confirm the sysfs value changed.
4. Reboot and confirm it persisted.
5. On systemd, suspend and resume, then confirm it again.

```bash
cat /sys/class/power_supply/BAT*/charge_control_end_threshold
```

Do not test arbitrary values outside the range accepted by the laptop vendor.
