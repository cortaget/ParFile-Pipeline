

def create_folder_if_not_exists(folder_path):
    """Create a folder if it does not exist.

    Args:
        folder_path (str): The path of the folder to create.
    """
    import os

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def create_folder(folder_path):
    """Create a folder.

    Args:
        folder_path (str): The path of the folder to create.
    """
    import os
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        print(f"Folder '{folder_path}' already exists.")