import os
import shutil
from pathlib import Path
from datetime import datetime
import argparse

def get_file_date(file_path):
    try:
        # Use the file's creation or modification time
        creation_time = datetime.fromtimestamp(Path(file_path).stat().st_mtime)
        return creation_time.strftime("%Y%m%d")  # Format: YYYYMMDD
    except Exception as e:
        print(f"Error getting date for {file_path}: {e}")
        return None

def organize_photos_in_place(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Ensure it's a file and not a directory
        if os.path.isfile(file_path):
            file_date = get_file_date(file_path)

            if file_date:
                date_folder = os.path.join(directory, file_date)
                if not os.path.exists(date_folder):
                    os.makedirs(date_folder)

                shutil.move(file_path, os.path.join(date_folder, file_name))
                print(f"Moved {file_name} to {date_folder}")
            else:
                print(f"Could not determine date for {file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize photos by creation date in the same directory.")
    parser.add_argument("directory", help="Path to the directory containing the photos.")
    args = parser.parse_args()

    if os.path.exists(args.directory):
        organize_photos_in_place(args.directory)
    else:
        print("The specified directory does not exist.")
