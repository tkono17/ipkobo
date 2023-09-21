#!/usr/bin/env python3
#------------------------------------------------------------------------
# Image Processing Application: ipapp.py
#------------------------------------------------------------------------
import argparse
import logging

import ipbox

logger = logging.getLogger(__name__)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batch-mode', dest='batchMode',
                        action='store_true', default=False,
                        help='Run in batch mode (no GUI)')
    return parser.parse_args()

def run(args):
    model = ipbox.AppData()
    app = None
    #
    if args.batchMode:
        view = None
        app = ipbox.App(model, view)
        logger.info('Running in batch mode')
        test = ipbox.BatchTest1('test1', app)
        test.run()
    else:
        view = ipbox.View(model)
        app = ipbox.App(model, view)
        view.mainloop()
    
if __name__ == '__main__':
    args = parseArgs()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)8s %(name)-20s: %(message)s')
    run(args)
    
