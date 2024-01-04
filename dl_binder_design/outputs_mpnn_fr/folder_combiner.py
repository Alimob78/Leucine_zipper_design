import os
import shutil

def combine_folders(folder1, folder2, combined_folder):
    # Create the combined folder if it doesn't exist
    os.makedirs(combined_folder, exist_ok=True)

    # Loop through files in the first folder
    for filename in os.listdir(folder1):
        source_path = os.path.join(folder1, filename)
        destination_path = os.path.join(combined_folder, f"{os.path.basename(folder1)}_{filename}")
        shutil.copy(source_path, destination_path)

    # Loop through files in the second folder
    for filename in os.listdir(folder2):
        source_path = os.path.join(folder2, filename)
        destination_path = os.path.join(combined_folder, f"{os.path.basename(folder2)}_{filename}")
        shutil.copy(source_path, destination_path)

# Replace these paths with your actual folder paths
folder1_path = "mpnn_fr_1"
folder2_path = "mpnn_fr_2"
combined_folder_path = "combined_mpnn_fr"

combine_folders(folder1_path, folder2_path, combined_folder_path)