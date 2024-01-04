#!/bin/bash

#SBATCH --job-name=diff_leu
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=mobedia@stanford.edu
#SBATCH --output=./output/my_output_%A_%a.out
#SBATCH --error=./output/my_score_%A_%a.err
##SBATCH --array=1-50
#SBATCH --time=3:00:00
#SBATCH -p possu,owners
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH -p gpu
#SBATCH -G 1

# Load necessary modules if needed
# Set up your environment if needed
#source /home/groups/possu/miniconda/envs/SE3nv
source ~/.bashrc
conda activate SE3nv

# Replace the command below with your actual command
./scripts/run_inference.py inference.output_prefix=example_outputs/lz_100 inference.input_pdb=input_pdbs/2ZTA.pdb 'contigmap.contigs=[A1-31/0 20-40]' 'ppi.hotspot_res=[A2,A16,A27]' inference.num_designs=100 denoiser.noise_scale_ca=0 denoiser.noise_scale_frame=0
