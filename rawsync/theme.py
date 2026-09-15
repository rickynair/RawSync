"""Design tokens for a clean, macOS-inspired look: soft neutrals, a single
system-blue accent, generous spacing, and consistent rounding."""

from __future__ import annotations

import customtkinter as ctk

FONT_FAMILY = "Segoe UI"
FONT_FAMILY_MONO = "Consolas"

LIGHT = {
    "bg": "#F5F5F7",
    "card": "#FFFFFF",
    "card_border": "#E5E5EA",
    "field": "#F2F2F5",
    "field_border": "#E1E1E6",
    "text_primary": "#1D1D1F",
    "text_secondary": "#6E6E73",
    "text_tertiary": "#A1A1A6",
    "accent": "#0A84FF",
    "accent_hover": "#0071E3",
    "accent_text": "#FFFFFF",
    "success": "#248A3D",
    "success_bg": "#E6F6EA",
    "danger": "#D70015",
    "danger_bg": "#FDEBEA",
    "track": "#E5E5EA",
    "divider": "#EDEDF0",
}

DARK = {
    "bg": "#1C1C1E",
    "card": "#2C2C2E",
    "card_border": "#3A3A3C",
    "field": "#242426",
    "field_border": "#3A3A3C",
    "text_primary": "#F5F5F7",
    "text_secondary": "#98989D",
    "text_tertiary": "#6E6E73",
    "accent": "#0A84FF",
    "accent_hover": "#409CFF",
    "accent_text": "#FFFFFF",
    "success": "#32D74B",
    "success_bg": "#1E3323",
    "danger": "#FF453A",
    "danger_bg": "#3A2323",
    "track": "#3A3A3C",
    "divider": "#333335",
}


def palette() -> dict:
    """Current color palette for the active CTk appearance mode."""
    return DARK if ctk.get_appearance_mode() == "Dark" else LIGHT


def dual(key: str):
    """(light, dark) tuple for a token, for CTk's built-in appearance-mode-
    aware color parameters (fg_color, text_color, border_color, ...).

    Every widget in this app is colored with these tuples rather than a
    resolved single color, so CustomTkinter can restyle everything live
    when the appearance mode changes -- no manual rebuild required."""
    return (LIGHT[key], DARK[key])


def font(size: int, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)


RADIUS_CARD = 18
RADIUS_FIELD = 10
RADIUS_PILL = 999
RADIUS_SMALL = 8
