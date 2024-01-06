#!/bin/bash

#SBATCH --job-name=af2_lz
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=mobedia@stanford.edu
#SBATCH --output=./logs/my_output_%A_%a.out
#SBATCH --error=./logs/my_score_%A_%a.err
#SBATCH --array=1-984
#SBATCH --time=01:00:00
#SBATCH -p owners,possu
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=8000
##SBATCH -p gpu
##SBATCH -G 1

# Load necessary modules if needed
# Set up your environment if needed
#source /home/groups/possu/miniconda/envs/SE3nv
source ~/.bashrc
conda activate dl_binder_design_py38

if [ ! -d "pae_interaction_results" ]; then
    mkdir pae_interaction_results
fi

# NOTE: I woulld suggest to set the array # to 1-[number of structures] but since since sherlock has a limit of 1000 arrays jobs, we will use the following foramt
eval "af2_initial_guess/A_predict.py -pdbdir ./outputs_mpnn_fr/combined_mpnn_fr/ -outpdbdir ./output_af2_predictions -scorefilename pae_interaction_results/af2_prediction_pae_results_${SLURM_ARRAY_TASK_ID}.sc -runlist ${SLURM_ARRAY_TASK_ID}"
eval "af2_initial_guess/A_predict.py -pdbdir ./outputs_mpnn_fr/combined_mpnn_fr/ -outpdbdir ./output_af2_predictions -scorefilename pae_interaction_results/af2_prediction_pae_results_$(( ${SLURM_ARRAY_TASK_ID} + 1000 )).sc -runlist $(( ${SLURM_ARRAY_TASK_ID} + 1000 ))"

if [ ${SLURM_ARRAY_TASK_ID} -eq 984 ]; then
    python top_design.py
fi
