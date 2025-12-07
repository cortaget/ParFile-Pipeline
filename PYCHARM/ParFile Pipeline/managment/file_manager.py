



def get_file_suffix(file_path):
    """Get the file suffix (extension) from a file path."""
    from pathlib import Path

    filename = Path(file_path)
    if not filename.exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    return filename.suffix  # Returns the file extension, e.g., .jpg


def move_file_to_folder(file_path, folder_path):
    """Move a file to a specified folder."""
    from shutil import move
    try:
        move(file_path, folder_path)
    except FileNotFoundError as e:
        print(f"Error moving file '{file_path}' to folder '{folder_path}': {e}")