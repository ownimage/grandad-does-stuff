import os
import shutil
import argparse


def organize_jpg_files(root_folder_path):
    # Iterate over each folder in the root directory
    for folder_name in os.listdir(root_folder_path):
        folder_path = os.path.join(root_folder_path, folder_name)

        # Check if the item is a folder
        if os.path.isdir(folder_path):
            # Create a subfolder for jpg files
            jpg_folder = os.path.join(folder_path, "origJpg")
            os.makedirs(jpg_folder, exist_ok=True)

            # Move all jpg files into the subfolder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                # Check if the item is a jpg file (case insensitive)
                if os.path.isfile(file_path) and file_name.lower().endswith(".jpg"):
                    shutil.move(file_path, os.path.join(jpg_folder, file_name))
                    print(f"Moved: {file_name} to {jpg_folder}")


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize photos by creation date in the same directory.")
    parser.add_argument("directory", help="Path to the directory containing the photos.")
    args = parser.parse_args()

    if os.path.exists(args.directory):
        organize_jpg_files(args.directory)
    else:
        print("The specified directory does not exist.")
