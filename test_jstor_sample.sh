#!/bin/bash
## Job Name
#SBATCH --job-name=jstor-samples-distance
## Allocation Definition
#SBATCH --account=stf
#SBATCH --partition=stf
## Resources
## Nodes
#SBATCH --nodes=1
## Tasks per node (Slurm assumes you want to run 28 tasks, remove 2x # and adjust parameter if needed)
###SBATCH --ntasks-per-node=28
## Walltime
#SBATCH --time=2:00:00
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
singularity exec graph-tool_latest.sif python test_graph_tool_sample.py data/mysql_jstor_eigen_citations_20190915.tsv data/jstor_sample_dist_20190920 --undirected --debug >& data/jstor_sample_dist_20190920.log
