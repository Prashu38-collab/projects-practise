from pathlib import Path
import hashlib


def get_files(folder_path):
    """Return all files inside the given folder."""
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError("Folder does not exist.")

    if not folder.is_dir():
        raise NotADirectoryError("The path is not a folder.")

    return [file for file in folder.rglob("*") if file.is_file()]


def group_by_size(files):
    """Group files that have the same size."""
    groups = {}

    for file in files:
        size = file.stat().st_size

        if size not in groups:
            groups[size] = []

        groups[size].append(file)

    return {
        size: files
        for size, files in groups.items()
        if len(files) > 1
    }


def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(1024 * 1024):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(files):
    """Find duplicate files using SHA-256 hashes."""
    hash_groups = {}

    for file in files:
        file_hash = calculate_hash(file)

        if file_hash not in hash_groups:
            hash_groups[file_hash] = []

        hash_groups[file_hash].append(file)

    return {
        file_hash: files
        for file_hash, files in hash_groups.items()
        if len(files) > 1
    }


def format_size(size):
    """Convert bytes into a human-readable size."""
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def main():
    folder_path = input("\nEnter folder path: ").strip()

    try:
        files = get_files(folder_path)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"\nError: {error}")
        return

    print(f"\nFiles found: {len(files)}")

    # First eliminate files that cannot possibly be duplicates.
    same_size_groups = group_by_size(files)

    possible_duplicates = [
        file
        for group in same_size_groups.values()
        for file in group
    ]

    print(f"Files requiring hash comparison: {len(possible_duplicates)}")

    duplicates = find_duplicates(possible_duplicates)

    if not duplicates:
        print("\nNo duplicate files found.")
        return

    

    wasted_space = 0
    duplicate_groups = 0

    for file_hash, files in duplicates.items():
        duplicate_groups += 1

        file_size = files[0].stat().st_size

        print(f"\nGroup {duplicate_groups}")
        print(f"Size: {format_size(file_size)}")

        for file in files:
            print(f"  → {file}")

        # Keep one copy; every additional copy is wasted space.
        wasted_space += file_size * (len(files) - 1)

    
    print(f"Duplicate groups: {duplicate_groups}")
    print(f"Wasted storage:   {format_size(wasted_space)}")
 


if __name__ == "__main__":
    main()