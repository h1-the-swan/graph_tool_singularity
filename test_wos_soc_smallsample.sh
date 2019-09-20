#!/bin/bash
## Job Name
#SBATCH --job-name=wos-soc-smallsamples-distance
## Allocation Definition
#SBATCH --account=stf
#SBATCH --partition=stf
## Resources
## Nodes
#SBATCH --nodes=1
## Tasks per node (Slurm assumes you want to run 28 tasks, remove 2x # and adjust parameter if needed)
###SBATCH --ntasks-per-node=28
## Walltime
#SBATCH --time=4:00:00
# E-mail Notification, see man sbatch for options
 

##turn on e-mail notification

#SBATCH --mail-type=ALL

# set --mail-user on command line with $EMAIL
###SBATCH --mail-user=$EMAIL


## Memory per node
#SBATCH --mem=200G
## Specify the working directory for this job
#SBATCH --chdir=/gscratch/stf/jporteno/graph_tool_singularity

module load singularity
singularity exec graph-tool_latest.sif python wos_soc_smallsample.py data/wos_dedup_coalesce_tsv/part-00000-3a9f3768-74d7-46f7-83b6-da30b9f63c90-c000.csv data/wos_soc_smallsample_20190920 --undirected --debug >& data/wos_soc_smallsample_20190920.log
