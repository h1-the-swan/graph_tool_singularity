2019-09-20

```
# on mox
# in interactive build node
module load singularity
[jporteno@n2233 graph_tool_singularity]$ singularity pull docker://tiagopeixoto/graph-tool

```

This created `graph-tool_latest.sif` (975M) (took a little while. 10mins?)

The following worked to run a python script in the container, with graph-tool loaded. It also worked to write a file in the working directory (`graph_tool_singularity`).

```
[jporteno@n2233 graph_tool_singularity]$ singularity exec graph-tool_latest.sif python test_graph_tool.py --debug

```

Running this (from login node) worked. Runs `test_graph_tool_sample.py` with WoS citations data.

```
[jporteno@mox1 graph_tool_singularity]$ sbatch -p ckpt -A stf-ckpt --mail-user $EMAIL test_wos_sample.sh 
```

Running the other scripts (`test_jstor_sample.sh`, `test_wos_soc_smallsample.sh`, `test_wos_largersample.sh`) also seems to work.
