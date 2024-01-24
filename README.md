This code generates two anti-parallel alpha helices (similar to leucine zipper structure) using the Rosetta diffusion model. Then it optimizes the sequence design through rounds of deep learning proteinMPNN model and Rosetta fastrelax. 

You can design your own anti-parallel alpha helices by following the below instructions.

I. Setting up:
* Clone the leucine zipper design file:`clone repo git@github.com:Alimob78/Leucine_zipper_design.git`
* Follow the README instructions for both RFdiffusion and dl_binder_design to clone required dependencies.
* Create appropriate environments by following individual models' README files.

II. Running the code:

* Creating backbones with RFdiffusion:
  1. You first need to create 100 initial designs of two alpha helices. We will then pick the anti-parallel conformations from the designs. To do this, you can run the `initial_100design.sh` or the following command: `./scripts/run_inference.py inference.output_prefix=example_outputs/lz_100 inference.input_pdb=input_pdbs/2ZTA.pdb 'contigmap.contigs=[A1-31/0 20-40]' 'ppi.hotspot_res=[A2,A16,A27]' inference.num_designs=100 denoiser.noise_scale_ca=0 denoiser.noise_scale_frame=0`.
  This command would design a 20-40 AA long binder to one chain of the leucine zipper (pdb: 2ZTA). Three hot spots were also selected to place the binder in the correct orientation. 
  2. Manually, select your top 20 designs based on anti-parallel orientation from the `example_outputs` directory. Save them in `input_pdbs/selected_10_designs_lz`.
  3. Run `**to be added` PyRosetta file which would extract the length of each binder from the `selected_10_designs_lz` directory for partial diffusion. 
  4. Run `partial_diffusion_parallel.sh`. This file would add partial diffusions to the selected designs to increase the structural diversity for sequence design. 


