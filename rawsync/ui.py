"""UI layer: splash screen, main window, settings sheet, and small
reusable widgets. Visual language is intentionally restrained and
macOS-inspired: soft neutral surfaces, one accent color, pill buttons,
and generous whitespace instead of icon clutter."""

from __future__ import annotations

import os
import threading
from tkinter import filedialog

import customtkinter as ctk

from . import theme
from .core import copy_matching_files

APP_NAME = "RAWSync"
APP_TAGLINE = "Match client-selected JPEGs to their RAW originals, instantly."
STUDIO_NAME = "ImageGNation"

ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icon.ico")


def _set_window_icon(win: ctk.CTk | ctk.CTkToplevel) -> None:
    if os.path.exists(ICON_PATH):
        try:
            win.iconbitmap(ICON_PATH)
        except Exception:
            pass


def _truncate_middle(path: str, max_chars: int = 46) -> str:
    if len(path) <= max_chars:
        return path
    head_len = max_chars // 2 - 2
    tail_len = max_chars - head_len - 3
    return f"{path[:head_len]}...{path[-tail_len:]}"


# --------------------------------------------------------------------------
# Small reusable widgets
# --------------------------------------------------------------------------
class PillButton(ctk.CTkButton):
    """A rounded, accent-colored (or ghost) button matching the app's style."""

    def __init__(self, master, text, command=None, kind="primary", **kwargs):
        p = theme.palette()
        base = dict(
            corner_radius=theme.RADIUS_PILL,
            font=theme.font(13, "bold"),
            height=38,
            cursor="hand2",
        )
        if kind == "primary":
            base.update(
                fg_color=p["accent"],
                hover_color=p["accent_hover"],
                text_color=p["accent_text"],
            )
        elif kind == "secondary":
            base.update(
                fg_color=p["field"],
                hover_color=p["card_border"],
                text_color=p["text_primary"],
                border_width=1,
                border_color=p["field_border"],
            )
        else:  # ghost
            base.update(
                fg_color="transparent",
                hover_color=p["field"],
                text_color=p["text_secondary"],
                font=theme.font(12, "normal"),
                height=30,
            )
        base.update(kwargs)
        super().__init__(master, text=text, command=command, **base)


class StepBadge(ctk.CTkFrame):
    """Small numbered circle used to give the three folder fields a clear order."""

    def __init__(self, master, number: int, **kwargs):
        p = theme.palette()
        super().__init__(
            master, width=26, height=26, corner_radius=13,
            fg_color=p["field"], border_width=1, border_color=p["field_border"],
            **kwargs,
        )
        self.grid_propagate(False)
        ctk.CTkLabel(
            self, text=str(number), font=theme.font(12, "bold"), text_color=p["text_secondary"],
        ).place(relx=0.5, rely=0.5, anchor="center")


class FolderField(ctk.CTkFrame):
    """One row: step badge, title + hint, path entry, browse pill."""

    def __init__(self, master, number: int, title: str, hint: str, on_change=None, **kwargs):
        p = theme.palette()
        super().__init__(master, fg_color="transparent", **kwargs)
        self.path_var = ctk.StringVar()
        self._on_change = on_change

        self.grid_columnconfigure(1, weight=1)

        StepBadge(self, number).grid(row=0, column=0, rowspan=2, padx=(0, 12), sticky="n")

        ctk.CTkLabel(
            self, text=title, font=theme.font(14, "bold"), text_color=p["text_primary"], anchor="w",
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            self, text=hint, font=theme.font(11), text_color=p["text_tertiary"], anchor="w",
        ).grid(row=1, column=1, sticky="w", pady=(0, 6))

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.grid(row=2, column=1, sticky="ew")
        row.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            row,
            textvariable=self.path_var,
            placeholder_text="No folder selected",
            height=36,
            corner_radius=theme.RADIUS_FIELD,
            fg_color=p["field"],
            border_color=p["field_border"],
            border_width=1,
            font=theme.font(12),
            text_color=p["text_primary"],
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        PillButton(row, "Browse", command=self._browse, kind="secondary", height=36).grid(row=0, column=1)

        if self._on_change:
            self.path_var.trace_add("write", lambda *_: self._on_change())

    def _browse(self):
        path = filedialog.askdirectory(title="Select folder")
        if path:
            self.path_var.set(path)

    def get(self) -> str:
        return self.path_var.get().strip()

    def set(self, value: str):
        self.path_var.set(value)


class Toast(ctk.CTkToplevel):
    """A borderless, auto-dismissing notification anchored to the main window,
    used instead of native OS dialog boxes to keep the whole experience
    visually consistent."""

    def __init__(self, master, message: str, kind: str = "success", duration_ms: int = 3200):
        super().__init__(master)
        p = theme.palette()
        bg = p["success_bg"] if kind == "success" else p["danger_bg"]
        fg = p["success"] if kind == "success" else p["danger"]

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        try:
            self.attributes("-alpha", 0.0)
        except Exception:
            pass
        self.configure(fg_color=bg)

        frame = ctk.CTkFrame(self, fg_color=bg, corner_radius=theme.RADIUS_FIELD, border_width=1, border_color=fg)
        frame.pack(fill="both", expand=True)
        ctk.CTkLabel(
            frame, text=message, font=theme.font(12, "bold"), text_color=fg,
            wraplength=320, justify="left",
        ).pack(padx=16, pady=12)

        self.update_idletasks()
        master.update_idletasks()
        mx, my = master.winfo_rootx(), master.winfo_rooty()
        mw, mh = master.winfo_width(), master.winfo_height()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{mx + mw - w - 24}+{my + mh - h - 24}")

        self._fade_in()
        self.after(duration_ms, self._fade_out)

    def _fade_in(self, alpha=0.0):
        try:
            alpha = min(alpha + 0.15, 1.0)
            self.attributes("-alpha", alpha)
            if alpha < 1.0:
                self.after(15, lambda: self._fade_in(alpha))
        except Exception:
            pass

    def _fade_out(self, alpha=1.0):
        try:
            alpha = max(alpha - 0.12, 0.0)
            self.attributes("-alpha", alpha)
            if alpha > 0.0:
                self.after(15, lambda: self._fade_out(alpha))
            else:
                self.destroy()
        except Exception:
            self.destroy()


class SettingsSheet(ctk.CTkToplevel):
    """Modal settings window. Currently: appearance mode only, matching the
    original app's feature set."""

    def __init__(self, master, on_appearance_change=None):
        super().__init__(master)
        p = theme.palette()
        self.title("Settings")
        self.geometry("360x260")
        self.resizable(False, False)
        self.configure(fg_color=p["bg"])
        _set_window_icon(self)
        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(
            self, text="Settings", font=theme.font(20, "bold"), text_color=p["text_primary"],
        ).pack(pady=(26, 4))
        ctk.CTkLabel(
            self, text="Appearance", font=theme.font(12), text_color=p["text_secondary"],
        ).pack(pady=(12, 8))

        seg = ctk.CTkSegmentedButton(
            self,
            values=["Light", "Dark", "System"],
            command=lambda choice: self._change_appearance(choice, on_appearance_change),
            selected_color=p["accent"],
            selected_hover_color=p["accent_hover"],
            fg_color=p["field"],
            unselected_color=p["field"],
            text_color=p["text_primary"],
            font=theme.font(12, "bold"),
        )
        seg.set(ctk.get_appearance_mode())
        seg.pack(padx=28, fill="x")

        PillButton(self, "Done", command=self.destroy, kind="primary").pack(pady=28)

    def _change_appearance(self, choice, callback):
        ctk.set_appearance_mode(choice)
        if callback:
            callback()


# --------------------------------------------------------------------------
# Splash screen
# --------------------------------------------------------------------------
class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        p = theme.palette()
        self.overrideredirect(True)
        self.configure(fg_color=p["bg"])
        w, h = 420, 260
        self.geometry(f"{w}x{h}")
        self.eval("tk::PlaceWindow . center")
        try:
            self.attributes("-alpha", 0.0)
        except Exception:
            pass

        card = ctk.CTkFrame(self, fg_color=p["bg"])
        card.pack(fill="both", expand=True)

        ctk.CTkLabel(
            card, text=APP_NAME, font=theme.font(32, "bold"), text_color=p["text_primary"],
        ).pack(pady=(70, 4))
        ctk.CTkLabel(
            card, text=f"by {STUDIO_NAME}", font=theme.font(13), text_color=p["text_secondary"],
        ).pack()

        self.bar = ctk.CTkProgressBar(
            card, width=200, height=4, corner_radius=2,
            fg_color=p["track"], progress_color=p["accent"], mode="indeterminate",
        )
        self.bar.pack(pady=36)
        self.bar.start()

        self._fade_in()
        self.after(1400, self._start_main)

    def _fade_in(self, alpha=0.0):
        try:
            alpha = min(alpha + 0.1, 1.0)
            self.attributes("-alpha", alpha)
            if alpha < 1.0:
                self.after(12, lambda: self._fade_in(alpha))
        except Exception:
            pass

    def _start_main(self):
        self.destroy()
        app = MainApp()
        app.mainloop()


# --------------------------------------------------------------------------
# Main application window
# --------------------------------------------------------------------------
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        p = theme.palette()

        self.title(APP_NAME)
        self.geometry("760x640")
        self.resizable(False, False)
        self.configure(fg_color=p["bg"])
        _set_window_icon(self)

        self._build_header()
        self._build_card()

    # -- layout -----------------------------------------------------------
    def _build_header(self):
        p = theme.palette()
        header = ctk.CTkFrame(self, fg_color="transparent")
        self._header_frame = header
        header.pack(fill="x", padx=32, pady=(28, 12))
        header.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            title_box, text=APP_NAME, font=theme.font(26, "bold"), text_color=p["text_primary"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box, text=APP_TAGLINE, font=theme.font(12), text_color=p["text_secondary"],
        ).pack(anchor="w", pady=(2, 0))

        PillButton(
            header, "⚙  Settings", command=self.open_settings, kind="secondary",
        ).grid(row=0, column=1, sticky="e")

    def _build_card(self):
        p = theme.palette()
        self.card = ctk.CTkFrame(
            self, fg_color=p["card"], corner_radius=theme.RADIUS_CARD,
            border_width=1, border_color=p["card_border"],
        )
        self.card.pack(fill="both", expand=True, padx=32, pady=(0, 28))

        inner = ctk.CTkFrame(self.card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=28, pady=26)

        self.jpeg_field = FolderField(
            inner, 1, "JPEG folder", "The client's selected JPEG previews", on_change=self._validate,
        )
        self.jpeg_field.pack(fill="x", pady=(0, 20))

        self.raw_field = FolderField(
            inner, 2, "RAW folder", "Where the original RAW files live", on_change=self._validate,
        )
        self.raw_field.pack(fill="x", pady=(0, 20))

        self.dest_field = FolderField(
            inner, 3, "Destination folder", "Matched RAW files are copied here", on_change=self._validate,
        )
        self.dest_field.pack(fill="x", pady=(0, 8))

        divider = ctk.CTkFrame(inner, fg_color=p["divider"], height=1)
        divider.pack(fill="x", pady=(14, 20))

        # Progress
        progress_row = ctk.CTkFrame(inner, fg_color="transparent")
        progress_row.pack(fill="x", pady=(0, 8))
        progress_row.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            progress_row, text="Ready", font=theme.font(12, "bold"), text_color=p["text_secondary"], anchor="w",
        )
        self.status_label.grid(row=0, column=0, sticky="w")
        self.percent_label = ctk.CTkLabel(
            progress_row, text="", font=theme.font(12), text_color=p["text_tertiary"], anchor="e",
        )
        self.percent_label.grid(row=0, column=1, sticky="e")

        self.progress_bar = ctk.CTkProgressBar(
            inner, height=8, corner_radius=4, fg_color=p["track"], progress_color=p["accent"],
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(8, 24))

        # Actions
        action_row = ctk.CTkFrame(inner, fg_color="transparent")
        action_row.pack(fill="x")
        action_row.grid_columnconfigure(0, weight=1)

        self.run_button = PillButton(
            action_row, "Run Match && Copy", command=self.run_task, kind="primary", height=44,
        )
        self.run_button.configure(state="disabled")
        self.run_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        PillButton(action_row, "Reset", command=self.reset_fields, kind="ghost").grid(row=0, column=1)

    # -- behaviour ----------------------------------------------------------
    def _validate(self):
        ready = all([self.jpeg_field.get(), self.raw_field.get(), self.dest_field.get()])
        self.run_button.configure(state="normal" if ready else "disabled")

    def reset_fields(self):
        self.jpeg_field.set("")
        self.raw_field.set("")
        self.dest_field.set("")
        self.progress_bar.set(0)
        self.percent_label.configure(text="")
        self.status_label.configure(text="Ready")
        self.run_button.configure(state="disabled")

    def open_settings(self):
        SettingsSheet(self, on_appearance_change=self._refresh_theme)

    def _refresh_theme(self):
        # Rebuild just our own header/card content in place so the new
        # palette applies everywhere. Deliberately does NOT touch
        # self.winfo_children() wholesale, since that would also tear down
        # any open Toplevel (e.g. the Settings sheet calling this) while
        # it's still on screen.
        p = theme.palette()
        self.configure(fg_color=p["bg"])
        self._header_frame.destroy()
        self.card.destroy()
        self._build_header()
        self._build_card()
        self._validate()

    def run_task(self):
        jpeg = self.jpeg_field.get()
        raw = self.raw_field.get()
        dest = self.dest_field.get()

        if not jpeg or not raw or not dest:
            Toast(self, "Please choose all three folders first.", kind="error")
            return

        self.run_button.configure(state="disabled")
        self.status_label.configure(text="Scanning...")
        self.percent_label.configure(text="")
        self.progress_bar.set(0)

        threading.Thread(target=self._background_run, args=(jpeg, raw, dest), daemon=True).start()

    def _background_run(self, jpeg, raw, dest):
        try:
            def progress_callback(done, total):
                def _update():
                    pct = done / total if total else 0
                    self.progress_bar.set(pct)
                    self.percent_label.configure(text=f"{done}/{total}")
                    self.status_label.configure(text="Matching & copying...")
                self.after(0, _update)

            result = copy_matching_files(jpeg, raw, dest, callback=progress_callback)

            def _on_success():
                self.progress_bar.set(1.0)
                if result.total_raw == 0:
                    self.status_label.configure(text="No RAW files found in that folder.")
                    Toast(self, "No RAW files were found to scan.", kind="error")
                elif result.copied == 0:
                    self.status_label.configure(text="No matches found.")
                    Toast(self, "None of the RAW files matched a JPEG.", kind="error")
                else:
                    self.status_label.configure(text=f"Done — {result.copied} of {result.total_raw} copied.")
                    Toast(self, f"Copied {result.copied} matching RAW file(s) to the destination folder.")
            self.after(0, _on_success)

        except Exception as e:
            def _on_error():
                self.status_label.configure(text="Something went wrong.")
                Toast(self, str(e), kind="error", duration_ms=5000)
            self.after(0, _on_error)

        finally:
            self.after(0, lambda: self.run_button.configure(state="normal"))


def launch():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    SplashScreen().mainloop()
