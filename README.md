This code generates two anti-parallel alpha helices (similar to leucine zipper structure) using the Rosetta diffusion model. Then it optimizes the sequence design through rounds of deep learning proteinMPNN model and Rosetta fastrelax. 

You can design your own anti-parallel alpha helices by following the below instructions.

I. Setting up:
* Clone the leucine zipper design file:`clone repo git@github.com:Alimob78/Leucine_zipper_design.git`
* Follow the README instructions for both RFdiffusion and dl_binder_design to clone required dependencies.
* Create appropriate environments by following individual models' README files.

II. Running the code:

* Creating backbones with RFdiffusion:
  1. You first need to create 100 initial designs of two alpha helices. We will then pick the anti-parallel conformations from the designs. 


