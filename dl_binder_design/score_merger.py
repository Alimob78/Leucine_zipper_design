import os
import pandas as pd
from pyrosetta import pose_from_file, init

# Specify the directory containing the .sc files
directory_path = "./pae_interaction_results"
dataframes =[]


# Function to extract sequence from a PDB files
# Initialize PyRosetta
init()
def sequence_extratctor(pdb_file):
    # Load the PDB file into a Pose object
    pose = pose_from_file(pdb_file)
    #whole_sequence = pose.sequence()

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
        # create the af2 prediction structures directory 
        pdb_filename_directory = "./output_af2_predictions/" + pdb_filename + ".pdb"
        seq1 = sequence_extratctor(pdb_filename_directory)[0]
        seq2 = sequence_extratctor(pdb_filename_directory)[1]

        # Add seq1 and seq2 columns to the DataFrame
        data["seq1"] = seq1
        data["seq2"] = seq2


        # Append the data to the list
        dataframes.append(data.iloc[1:])

        # Print a message indicating the file is processed
        print(filename, "is processed")

# Concatenate all DataFrames into a single DataFrame
merged_data = pd.concat(dataframes, ignore_index=True)

# Convert the "pae_interaction" column to numeric
merged_data["pae_interaction"] = pd.to_numeric(merged_data["pae_interaction"], errors="coerce")


# Print the updated column names
print("Column names:", merged_data.columns)

# Sort the merged DataFrame based on the appropriate column
sort_column = "pae_interaction"  # Replace with the correct column name
sorted_data = merged_data.sort_values(by=sort_column, ascending=True)

# Save the sorted data to a new .sc file
sorted_data.to_csv("./pae_interaction_results/final_scoring_file.sc", sep='\t', index=False)

