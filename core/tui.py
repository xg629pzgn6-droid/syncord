import os
from random import choice
from pynput import keyboard
from rich.console import Console

from core.db_manager import SQliteDB
from core.partition import download_file_by_path, assemble_partition
from core.ascii_hell import anime_ascii


def list_children(files_by_folder, current_folder):
    folders = set()
    files = []

    if current_folder == "":
        # ROOT: only folders without '/'
        for path in files_by_folder.keys():
            if "/" not in path:
                folders.add(path)
    else:
        prefix = current_folder + "/"
        for path in files_by_folder.keys():
            if not path.startswith(prefix):
                continue

            rest = path[len(prefix) :]
            if "/" in rest:
                folders.add(rest.split("/")[0])
            elif rest:
                folders.add(rest)

        files = files_by_folder.get(current_folder, [])
        seen = set()
        unique_files = []
        for file in files:
            if file[1] not in seen:
                seen.add(file[1])
                unique_files.append(file)
        files = unique_files
    return sorted(folders), list(files)

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def render(files_by_folder, current_folder, cursor):
    clear_console()
    console = Console()
    console.print(
        """
[yellow]
                                                                  $$\ 
                                                                  $$ |
 $$$$$$$\ $$\   $$\ $$$$$$$\   $$$$$$$\  $$$$$$\   $$$$$$\   $$$$$$$ |
$$  _____|$$ |  $$ |$$  __$$\ $$  _____|$$  __$$\ $$  __$$\ $$  __$$ |
\$$$$$$\  $$ |  $$ |$$ |  $$ |$$ /      $$ /  $$ |$$ |  \__|$$ /  $$ |
 \____$$\ $$ |  $$ |$$ |  $$ |$$ |      $$ |  $$ |$$ |      $$ |  $$ |
$$$$$$$  |\$$$$$$$ |$$ |  $$ |\$$$$$$$\ \$$$$$$  |$$ |      \$$$$$$$ |
\_______/  \____$$ |\__|  \__| \_______| \______/ \__|       \_______|
          $$\   $$ |                                                  
          \$$$$$$  |                                                  
           \______/                                                   
[/yellow]
"""
    )

    display_folder = "/" if current_folder == "" else current_folder
    console.print(f"[bold yellow]Folder:[/bold yellow] {display_folder}\n")

    folders, files = list_children(files_by_folder, current_folder)

    items = [f"[DIR] {f}" for f in folders] + [f"{file[3]}" for file in files]

    if not items:
        console.print("[dim]No items[/dim]")

    for i, item in enumerate(items):
        if i == cursor:
            console.print(f"> [green]{item}[/green]")
        else:
            console.print(f"  {item}", style="dim")

    console.print("\n[red]CONTROLS[/red] w/s move | d open | a back | e dl | q quit")

    return folders, files


def download_folder(folder, files_by_folder):

    fold, files = list_children(files_by_folder, folder)
    for file in files:
        os.makedirs(file[4], exist_ok=True)
        print(f"Downloading file: {file[4]}/{file[3]}")
        download_file_by_path(f"{file[4]}/{file[3]}", path_to_download="./"+file[4])
    
    for x in fold:
        download_folder(folder + "/" + x, files_by_folder)

def show_stats():
    db = SQliteDB()
    total_files = db.get_all_files()
    total_size = sum(file[5] for file in total_files)
    total_folders = db.get_all_folders()

    print("Syncord Usage Statistics")
    print(f"Total files stored: {len(total_files)}")
    print(f"Total folders: {len(total_folders)}")
    print(f"Total storage used: {total_size / (1024 * 1024):.2f} MB\n")

    db.close()


def start_dashboard():
    db = SQliteDB()
    all_folders = db.get_all_folders()

    files_by_folder = {
        folder: db.get_all_folder_files(folder) for folder in all_folders
    }

    clear_console()
    print("Welcome to Syncord TUI Dashboard")
    print(choice(anime_ascii))
    show_stats()
    print("Press any key to continue to the dashboard...")

    # render(files_by_folder, current_folder, cursor)
    current_folder = ""  # ROOT
    cursor = 0

    def on_press(key):
        nonlocal cursor, current_folder

        folders, files = render(files_by_folder, current_folder, cursor)
        total_items = len(folders) + len(files)

        try:
            if hasattr(key, "char"):
                if key.char == "a":
                    if current_folder != "":
                        current_folder = (
                            current_folder.rsplit("/", 1)[0]
                            if "/" in current_folder
                            else ""
                        )
                        cursor = 0

                elif key.char == "e":
                    if cursor < len(folders):
                        selected = folders[cursor]
                        current_folder = (
                            selected
                            if current_folder == ""
                            else f"{current_folder}/{selected}"
                        )
                        cursor = 0
                    if cursor >= len(folders):
                        selected = files[cursor - len(folders)]
                        print(f"Downloading file: {selected[4]}/{selected[3]}")
                        assemble_partition(selected[1])
                        print("Download completed.")
                    else:
                        download_folder(current_folder, files_by_folder)

                elif key.char == "q":
                    return False
                elif key.char == "d":
                    if cursor < len(folders):
                        selected = folders[cursor]
                        current_folder = (
                            selected
                            if current_folder == ""
                            else f"{current_folder}/{selected}"
                        )
                        cursor = 0
                elif key.char == "w":
                    cursor = max(0, cursor - 1)
                elif key.char == "s":
                    cursor = min(max(0, total_items - 1), cursor + 1)

        except Exception as e:
            print(e)

        render(files_by_folder, current_folder, cursor)
    

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    db.close()


if __name__ == "__main__":
    start_dashboard()
