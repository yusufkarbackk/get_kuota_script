import os
import shutil


# List of folders to delete
folders_to_delete = [
    "ShaderCache",
    "GrShaderCache",
    "Crashpad",
    "BrowserMetrics",
    "Safe Browsing",
    "component_crx_cache",
]

def remove_folders(profile_path):
    # Loop through the folders and delete them
    for folder in folders_to_delete:
        folder_path = os.path.join(profile_path, folder)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)  # Recursively delete the folder and its contents
                print(f"Deleted: {folder_path}")
            except Exception as e:
                print(f"Failed to delete {folder_path}: {e}")
        else:
            print(f"Folder not found: {folder_path}")

    print("Cleanup complete.")