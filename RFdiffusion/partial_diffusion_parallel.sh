#!/bin/bash

#SBATCH --job-name=mpnn_fr
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=mobedia@stanford.edu
#SBATCH --output=./logs/my_output_%A_%a.out
#SBATCH --error=./logs/my_score_%A_%a.err
##SBATCH --array=1-20
#SBATCH --time=24:00:00
#SBATCH -p owners, possu
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
##SBATCH -p gpu
##SBATCH -G 1

# Load necessary modules if needed
# Set up your environment if needed
#source /home/groups/possu/miniconda/envs/SE3nv
source ~/.bashrc
conda activate dl_binder_design_py38

# Directory containing input files
input_dir="./input_pdbs/selected_10_designs_lz"

# List of input files with "pdb" in the file name
input_files=("$input_dir"/*pdb)

# File containing parameters for each structure
params_file="./params.txt"

# Get the current input file based on the array index
current_input="${input_files[$SLURM_ARRAY_TASK_ID - 1]}"

# Get the parameters corresponding to the current task
current_params=$(grep "$(basename "$current_input")" "$params_file" | awk '{$1=""; print $0}')

# Check if the current input file exists
if [ -e "$current_input" ]; then
    # Create a string to store command arguments
    cmd_args="${current_params} inference.output_prefix="outputs/r1_partial_diffusion/design_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}" inference.input_pdb=$current_input diffuser.partial_T=30 inference.num_designs=50"

    # Replace the command below with your actual command
    eval "./scripts/run_inference.py $cmd_args"
fi
