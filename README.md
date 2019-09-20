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
