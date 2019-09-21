# -*- coding: utf-8 -*-

DESCRIPTION = """Test calculating shortest path distances using graph-tool. Calculate shortest paths between a small number of sociology papers"""

import sys, os, time
from datetime import datetime
from timeit import default_timer as timer
try:
    from humanfriendly import format_timespan
except ImportError:
    def format_timespan(seconds):
        return "{:.2f} seconds".format(seconds)

import logging
logging.basicConfig(format='%(asctime)s %(name)s.%(lineno)d %(levelname)s : %(message)s',
        datefmt="%H:%M:%S",
        level=logging.INFO)
# logger = logging.getLogger(__name__)
logger = logging.getLogger('__main__').getChild(__name__)

import graph_tool
from graph_tool.topology import shortest_distance
import pandas as pd
import numpy as np

WOS_IDS = [
    'WOS:000362448400007',
    'WOS:000294897600002',
    'WOS:000328713500013',
    'WOS:000300125300004',
    'WOS:000298005700005',
    'WOS:000290474700006'
]

def main(args):
    outdir = os.path.abspath(args.outdir)
    if not os.path.exists(outdir):
        logger.debug("creating output directory: {}".format(outdir))
        os.mkdir(outdir)
    else:
        logger.debug("using output directory: {}".format(outdir))

    start = timer()
    logger.debug("loading graph from {}. This will take a while...".format(args.edges))
    g = graph_tool.load_graph_from_csv(args.edges, directed=True, skip_first=True, csv_options={'delimiter': '\t'})
    logger.debug("done loading graph. Took {}".format(format_timespan(timer()-start)))

    start = timer()
    logger.debug("creating dictionary of name to vertices...")
    name_to_v = {g.vp.name[v]: v for v in g.vertices()}
    logger.debug("done loading dictionary. Took {}".format(format_timespan(timer()-start)))

    # get a unique filename
    i = 0
    while True:
        fname_calc_times = os.path.join(outdir, 'calc_times_{:03}.csv'.format(i))
        if not os.path.exists(fname_calc_times):
            break
    f_calc_times = open(fname_calc_times, 'w', buffering=1)

    sep = ','
    logger.debug("writing header to {}".format(fname_calc_times))
    f_calc_times.write("source_name{sep}calc_time{sep}distance_fname\n".format(sep=sep))

    start = timer()
    logger.debug("starting shortest path calculations...")
    if args.undirected is True:
        logger.debug("treating graph as undirected for shortest distance calculations")
        directed = False
    else:
        directed = None

    vertices_sample = [name_to_v[wos_id] for wos_id in WOS_IDS]
    logger.debug("number of sample vertices: {}".format(len(vertices_sample)))

    for i, source in enumerate(vertices_sample):
        this_start = timer()
        source_name = g.vp.name[source]
        # source_index = vertices_sample_indexes[i]
        outfname = "{:012d}.csv".format(i)  # filename corresponds to row number of calc_time.csv file
        outfname = os.path.join(outdir, outfname)
        if os.path.exists(outfname):
            logger.debug("filename {} already exists. skipping.".format(outfname))
            continue
        logger.debug("calculating shortest distance for vertex: name: {}".format(source_name))
        dist = shortest_distance(g, source=source, target=vertices_sample, directed=directed)
        this_time = timer() - this_start
        with open(outfname, 'w') as outf:
            for x in dist:
                outf.write("{}\n".format(x))
        f_calc_times.write("{source_name}{sep}{calc_time}{sep}{distance_fname}\n".format(sep=sep, source_name=source_name, calc_time=this_time, distance_fname=outfname))
    logger.debug("finished shortest path calculations. Took {}".format(format_timespan(timer()-start)))
    f_calc_times.close()



if __name__ == "__main__":
    total_start = timer()
    logger = logging.getLogger(__name__)
    logger.info(" ".join(sys.argv))
    logger.info( '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) )
    import argparse
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("edges", help="path to edges TSV (with header)")
    parser.add_argument("outdir", help="path to output directory (will be created)")
    parser.add_argument("--undirected", action='store_true', help="treat graph as undirected for shortest distance calculations")
    parser.add_argument("--debug", action='store_true', help="output debugging info")
    global args
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('debug mode is on')
    else:
        logger.setLevel(logging.INFO)
    main(args)
    total_end = timer()
    logger.info('all finished. total time: {}'.format(format_timespan(total_end-total_start)))
