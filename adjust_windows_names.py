import os
import subprocess
from pathlib import Path

INVALID_CHARS = '<>:"|?*'
RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def make_name_windows_safe(name: str) -> str:
    """
    Converts one file or folder name into a Windows-compatible name.
    Invalid Windows characters are replaced with hyphens.
    Reserved Windows device names are prefixed with an underscore.
    """
    safe_name = name

    for char in INVALID_CHARS:
        safe_name = safe_name.replace(char, "-")

    safe_name = safe_name.rstrip(" .")

    if not safe_name:
        safe_name = "_"

    base_name = safe_name.split(".")[0].upper()
    if base_name in RESERVED_NAMES:
        safe_name = f"_{safe_name}"

    return safe_name


def make_path_windows_safe(path: str) -> str:
    """
    Converts a complete Git path into a Windows-compatible path.
    Each folder name and the file name are processed separately.
    """
    return "/".join(make_name_windows_safe(part) for part in path.split("/"))


def make_unique_path(path: str, used_paths: set[str]) -> str:
    """
    Prevents name collisions after renaming.
    If the cleaned path already exists, a numeric suffix is added before the file extension.
    """
    if path not in used_paths:
        return path

    path_obj = Path(path)
    parent = "" if str(path_obj.parent) == "." else f"{path_obj.parent}/"
    stem = path_obj.stem
    suffix = path_obj.suffix

    counter = 1

    while True:
        candidate = f"{parent}{stem}_windows_{counter}{suffix}"

        if candidate not in used_paths:
            return candidate

        counter += 1


def get_tracked_files() -> list[str]:
    """
    Reads all files tracked by Git.
    Only tracked files are renamed, so temporary files and the .git folder are ignored.
    """
    raw_output = subprocess.check_output(["git", "ls-files", "-z"])
    files = raw_output.decode("utf-8", errors="replace").split("\0")

    return [file for file in files if file]


def rename_files_for_windows() -> None:
    """
    Renames all tracked files whose paths are not Windows-compatible.
    The rename is done through git mv so Git records the changes cleanly.
    """
    tracked_files = get_tracked_files()
    used_paths = set(tracked_files)
    renamed_count = 0

    for old_path in tracked_files:
        new_path = make_path_windows_safe(old_path)

        if new_path == old_path:
            continue

        used_paths.remove(old_path)
        new_path = make_unique_path(new_path, used_paths)
        used_paths.add(new_path)

        os.makedirs(os.path.dirname(new_path) or ".", exist_ok=True)

        print(f"Rename: {old_path} -> {new_path}")
        subprocess.run(["git", "mv", old_path, new_path], check=True)

        renamed_count += 1

    print(f"\nFertig. Umbenannte Dateien: {renamed_count}")


if __name__ == "__main__":
    rename_files_for_windows()