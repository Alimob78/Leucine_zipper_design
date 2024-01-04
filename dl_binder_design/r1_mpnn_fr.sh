#!/bin/bash

#SBATCH --job-name=diff_leu
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=mobedia@stanford.edu
#SBATCH --output=./logs/my_output_%A_%a.out
#SBATCH --error=./logs/my_score_%A_%a.err
##SBATCH --array=1-20
#SBATCH --time=30:00:00
#SBATCH -p owners,possu
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

rm check.point 2>/dev/null
./mpnn_fr/dl_interface_design.py -pdbdir ../RFdiffusion/outputs/r1_partial_diffusion/ -relax_cycles 2 -seqs_per_struct 1 -outpdbdir outputs/mpnn_fr_1/