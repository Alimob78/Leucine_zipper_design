import os
import pandas as pd
from pyrosetta import pose_from_file, init
from shutil import copyfile

# Specify the directory containing the .sc files
directory_path = "./pae_interaction_results"
dataframes_all = []  # For all designs
dataframes_top = []  # For top designs

# Specify the output directory for all designs
output_directory_all = "./all_designs"
if not os.path.exists(output_directory_all):
    os.makedirs(output_directory_all)

# Specify the output directory for top designs
output_directory_top = "./top_designs"
if not os.path.exists(output_directory_top):
    os.makedirs(output_directory_top)

# Initialize PyRosetta
init()

# Function to extract sequence from a PDB file
def sequence_extractor(pdb_file):
    # Load the PDB file into a Pose object
    pose = pose_from_file(pdb_file)

    # Extract the sequence of the specified chain
    chain_1_sequence = ''
    chain_2_sequence = ''

    for i in range(1, pose.total_residue() + 1):
        if pose.pdb_info().chain(i) == 'A':
            chain_1_sequence += pose.residue(i).name1()
        if pose.pdb_info().chain(i) == 'B':
            chain_2_sequence += pose.residue(i).name1()

    return chain_1_sequence, chain_2_sequence

# Loop through all .sc files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".sc"):
        file_path = os.path.join(directory_path, filename)

        # Read the data from the .sc file into a DataFrame, skipping the first row
        data = pd.read_csv(file_path, delim_whitespace=True, skiprows=0, header=None)

        # Set the column names based on the first row
        data.columns = data.iloc[0]

        # Extract the PDB filename from the last column
        pdb_filename = data.iloc[1, -1]
        # Create the af2 prediction structures directory 
        pdb_filename_directory = "./output_af2_predictions/" + pdb_filename + ".pdb"
        seq1 = sequence_extractor(pdb_filename_directory)[0]
        seq2 = sequence_extractor(pdb_filename_directory)[1]

        # Add seq1 and seq2 columns to the DataFrame
        data["seq1"] = seq1
        data["seq2"] = seq2

        # Convert the "pae_interaction" column to numeric
        data["pae_interaction"] = pd.to_numeric(data["pae_interaction"], errors="coerce")

        # Append the data to the list for all designs
        dataframes_all.append(data.iloc[1:])

        # Check if pae_interaction is less than 10 for top designs
        if data.loc[1, "pae_interaction"] < 10:
            # Move the corresponding PDB file to the "top_designs" directory
            source_pdb_path = pdb_filename_directory
            destination_pdb_path = os.path.join(output_directory_top, pdb_filename + ".pdb")
            copyfile(source_pdb_path, destination_pdb_path)

            # Append the data to the list for top designs
            dataframes_top.append(data.iloc[1:])

            # Print a message indicating the file is processed
            print(filename, "is processed")

# Concatenate all DataFrames into a single DataFrame for all designs
merged_data_all = pd.concat(dataframes_all, ignore_index=True)

# Sort the merged DataFrame based on the appropriate column
sort_column_all = "pae_interaction"  # Replace with the correct column name
sorted_data_all = merged_data_all.sort_values(by=sort_column_all, ascending=True)

# Save the sorted data to a new .sc file for all designs
sorted_data_all.to_csv(os.path.join(output_directory_all, "final_scoring_file.sc"), sep='\t', index=False)

# Concatenate all DataFrames into a single DataFrame for top designs
merged_data_top = pd.concat(dataframes_top, ignore_index=True)

# Sort the merged DataFrame based on the appropriate column for top designs
sort_column_top = "pae_interaction"  # Replace with the correct column name
sorted_data_top = merged_data_top.sort_values(by=sort_column_top, ascending=True)

# Save the sorted data to a new .sc file for top designs
sorted_data_top.to_csv(os.path.join(output_directory_top, "top_designs_scoring.sc"), sep='\t', index=False)

# Print a message indicating the completion
print("All files processed. Top designs saved to", os.path.join(output_directory_top, "top_designs_scoring.sc"))
print("All designs saved to", os.path.join(output_directory_all, "final_scoring_file.sc"))

