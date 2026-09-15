"""RAWSync entry point.

Scans a JPEG folder and a RAW folder, and copies every RAW file whose base
filename matches a JPEG into a destination folder -- so a photographer can
hand off a client's picks and get the matching originals ready for import.
"""

from rawsync.ui import launch

if __name__ == "__main__":
    launch()
