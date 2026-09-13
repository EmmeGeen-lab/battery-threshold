#!/usr/bin/env python3
"""Battery Threshold — small desktop UI for Linux charge thresholds."""

from __future__ import annotations

import glob
import locale
import os
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

VERSION = "0.1.0-beta1"
APP_ID = "io.github.battery-threshold"
HELPERS = (
    "/usr/lib/battery-threshold/battery-threshold-helper",
    "/usr/libexec/battery-threshold/battery-threshold-helper",
    "/usr/local/lib/battery-threshold/battery-threshold-helper",
)

STRINGS = {
    "en": {
        "title": "Battery Threshold",
        "subtitle": "Set a maximum charge level and restore it after reboot.",
        "apply": "Apply and save",
        "waiting": "Waiting for authorization…",
        "detected": "Detected: {devices}",
        "current": "Current threshold: {value}%",
        "unsupported": "No compatible battery detected",
        "unavailable": "This feature is not available on this computer",
        "read_error": "Unable to read the current threshold",
        "helper_missing": "System helper not found. Reinstall Battery Threshold.",
        "pkexec_missing": "pkexec is not installed. Install Polkit first.",
        "cancelled": "The operation was cancelled or not authorized.",
        "failed": "The threshold could not be applied.",
        "success": "Charge limit set to {value}% and saved for future boots.",
        "verify_warning": "The setting was saved, but cannot yet be read back.",
        "timeout": "Authorization timed out. Please try again.",
        "about": "Version {version} · GPL-3.0 · Marco Z.",
    },
    "it": {
        "title": "Battery Threshold",
        "subtitle": "Imposta la carica massima e la ripristina dopo il riavvio.",
        "apply": "Applica e salva",
        "waiting": "In attesa dell’autorizzazione…",
        "detected": "Rilevata: {devices}",
        "current": "Soglia attuale: {value}%",
        "unsupported": "Nessuna batteria compatibile rilevata",
        "unavailable": "Funzione non disponibile su questo computer",
        "read_error": "Impossibile leggere la soglia attuale",
        "helper_missing": "Componente di sistema non trovato. Reinstalla Battery Threshold.",
        "pkexec_missing": "pkexec non è installato. Installa prima Polkit.",
        "cancelled": "Operazione annullata o autorizzazione non concessa.",
        "failed": "Non è stato possibile applicare la soglia.",
        "success": "Limite impostato al {value}% e salvato per i prossimi avvii.",
        "verify_warning": "Impostazione salvata, ma il valore non è ancora leggibile.",
        "timeout": "Autorizzazione scaduta. Riprova.",
        "about": "Versione {version} · GPL-3.0 · Marco Z.",
    },
}


def language() -> str:
    code = (
        os.environ.get("LANGUAGE")
        or os.environ.get("LC_ALL")
        or os.environ.get("LC_MESSAGES")
        or os.environ.get("LANG")
        or locale.getlocale()[0]
        or "en"
    ).lower()
    return "it" if code.startswith("it") else "en"


TEXT = STRINGS[language()]


def threshold_files() -> list[Path]:
    root = os.environ.get("BATTERY_THRESHOLD_SYSFS_ROOT", "/sys/class/power_supply")
    return [Path(p) for p in sorted(glob.glob(f"{root}/BAT*/charge_control_end_threshold"))]


def read_threshold() -> tuple[int | None, str]:
    files = threshold_files()
    if not files:
        return None, TEXT["unsupported"]
    try:
        values = [int(path.read_text(encoding="utf-8").strip()) for path in files]
    except (OSError, ValueError):
        return None, TEXT["read_error"]
    devices = ", ".join(path.parent.name for path in files)
    return values[0], TEXT["detected"].format(devices=devices)


def helper_path() -> str | None:
    return next((path for path in HELPERS if os.path.isfile(path)), None)


class BatteryThresholdApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(TEXT["title"])
        self.geometry("480x420")
        self.minsize(440, 390)
        self.configure(bg="#f5f7fb")

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Page.TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#f5f7fb", foreground="#152033", font=("Sans", 20, "bold"))
        style.configure("Sub.TLabel", background="#f5f7fb", foreground="#5a6678", font=("Sans", 10))
        style.configure("Big.TLabel", background="#ffffff", foreground="#2463eb", font=("Sans", 35, "bold"))
        style.configure("Card.TLabel", background="#ffffff", foreground="#344054", font=("Sans", 10))
        style.configure("Apply.TButton", font=("Sans", 11, "bold"), padding=(18, 10))

        page = ttk.Frame(self, padding=24, style="Page.TFrame")
        page.pack(fill="both", expand=True)
        ttk.Label(page, text=TEXT["title"], style="Title.TLabel").pack(anchor="w")
        ttk.Label(page, text=TEXT["subtitle"], style="Sub.TLabel").pack(anchor="w", pady=(2, 18))

        card = ttk.Frame(page, style="Card.TFrame", padding=22)
        card.pack(fill="both", expand=True)
        self.value = tk.IntVar(value=70)
        self.value_label = ttk.Label(card, text="70%", style="Big.TLabel")
        self.value_label.pack()

        self.scale = ttk.Scale(card, from_=50, to=100, orient="horizontal", command=self.on_slide)
        self.scale.pack(fill="x", pady=(8, 2))
        labels = ttk.Frame(card, style="Card.TFrame")
        labels.pack(fill="x")
        ttk.Label(labels, text="50%", style="Card.TLabel").pack(side="left")
        ttk.Label(labels, text="100%", style="Card.TLabel").pack(side="right")

        quick = ttk.Frame(card, style="Card.TFrame")
        quick.pack(pady=14)
        for amount in (60, 65, 70, 80, 100):
            ttk.Button(quick, text=str(amount), width=4, command=lambda n=amount: self.set_value(n)).pack(side="left", padx=3)

        self.apply_button = ttk.Button(card, text=TEXT["apply"], style="Apply.TButton", command=self.apply)
        self.apply_button.pack(pady=(2, 12))
        self.status = ttk.Label(card, text="", style="Card.TLabel")
        self.status.pack()
        self.device = ttk.Label(card, text="", style="Card.TLabel")
        self.device.pack(pady=(3, 0))
        ttk.Label(card, text=TEXT["about"].format(version=VERSION), style="Card.TLabel").pack(side="bottom", pady=(12, 0))
        self.refresh()

    def set_value(self, value: int) -> None:
        value = max(50, min(100, int(value)))
        self.value.set(value)
        self.scale.set(value)
        self.value_label.configure(text=f"{value}%")

    def on_slide(self, raw_value: str) -> None:
        value = int(round(float(raw_value) / 5) * 5)
        self.value.set(value)
        self.value_label.configure(text=f"{value}%")

    def refresh(self) -> None:
        current, device_text = read_threshold()
        self.device.configure(text=device_text)
        if current is None:
            self.status.configure(text=TEXT["unavailable"])
            self.apply_button.state(["disabled"])
            return
        self.set_value(current)
        self.status.configure(text=TEXT["current"].format(value=current))

    def apply(self) -> None:
        helper = helper_path()
        if helper is None:
            messagebox.showerror(TEXT["title"], TEXT["helper_missing"])
            return
        value = self.value.get()
        self.apply_button.state(["disabled"])
        self.status.configure(text=TEXT["waiting"])
        self.update_idletasks()
        try:
            result = subprocess.run(["pkexec", helper, str(value)], text=True, capture_output=True, timeout=120, check=False)
        except FileNotFoundError:
            messagebox.showerror(TEXT["title"], TEXT["pkexec_missing"])
        except subprocess.TimeoutExpired:
            messagebox.showerror(TEXT["title"], TEXT["timeout"])
        else:
            if result.returncode != 0:
                detail = TEXT["cancelled"] if result.returncode in (126, 127) else (result.stderr or result.stdout).strip()
                messagebox.showerror(TEXT["title"], detail or TEXT["failed"])
            else:
                current, _ = read_threshold()
                if current == value:
                    messagebox.showinfo(TEXT["title"], TEXT["success"].format(value=value))
                else:
                    messagebox.showwarning(TEXT["title"], TEXT["verify_warning"])
        self.apply_button.state(["!disabled"])
        self.refresh()


if __name__ == "__main__":
    BatteryThresholdApp().mainloop()
