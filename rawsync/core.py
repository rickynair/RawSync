"""Core matching/copy logic. No UI dependencies live here."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from typing import Callable, Optional

# Extensions we treat as "RAW". Add proprietary formats here as needed.
RAW_EXTENSIONS = {".cr3", ".cr2", ".arw", ".nef", ".dng", ".tiff", ".tif", ".raf", ".orf", ".rw2"}
JPEG_EXTENSIONS = {".jpg", ".jpeg", ".png"}

ProgressCallback = Callable[[int, int], None]


@dataclass
class CopyResult:
    """Summary of a matching/copy run."""

    copied: int = 0
    skipped: int = 0
    total_raw: int = 0
    copied_files: list[str] = field(default_factory=list)

    @property
    def matched(self) -> bool:
        return self.copied > 0


def copy_matching_files(
    jpeg_folder: str,
    raw_folder: str,
    destination_folder: str,
    callback: Optional[ProgressCallback] = None,
) -> CopyResult:
    """Copy every RAW file in ``raw_folder`` whose base filename matches a
    JPEG in ``jpeg_folder`` into ``destination_folder``.

    Matching is case-insensitive and ignores extension. Metadata/timestamps
    are preserved on copy (``shutil.copy2``).
    """
    if not os.path.isdir(jpeg_folder):
        raise FileNotFoundError(f"JPEG folder not found: {jpeg_folder}")
    if not os.path.isdir(raw_folder):
        raise FileNotFoundError(f"RAW folder not found: {raw_folder}")
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder, exist_ok=True)

    jpeg_basenames = {
        os.path.splitext(f)[0].lower()
        for f in os.listdir(jpeg_folder)
        if os.path.splitext(f)[1].lower() in JPEG_EXTENSIONS
    }

    raw_files = [
        f for f in os.listdir(raw_folder)
        if os.path.splitext(f)[1].lower() in RAW_EXTENSIONS
    ]

    result = CopyResult(total_raw=len(raw_files))

    for index, raw_file in enumerate(raw_files, start=1):
        base = os.path.splitext(raw_file)[0]

        if base.lower() in jpeg_basenames:
            shutil.copy2(
                os.path.join(raw_folder, raw_file),
                os.path.join(destination_folder, raw_file),
            )
            result.copied += 1
            result.copied_files.append(raw_file)
        else:
            result.skipped += 1

        if callback:
            callback(index, result.total_raw)

    return result
