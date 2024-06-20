#!/usr/bin/env python3
#------------------------------------------------------------------------
# Image Processing Workshop: ipkobo.py
#------------------------------------------------------------------------
import argparse
import logging

import ipcat

logger = logging.getLogger(__name__)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batch-mode', dest='batchMode',
                        action='store_true', default=False,
                        help='Run in batch mode (no GUI)')
    parser.add_argument('-l', '--log-level', dest='logLevel',
                        type=str, default='INFO',
                        help='Logging level DEBUG|INFO|WARNING|ERROR')
    return parser.parse_args()

def run(args):
    app = ipcat.App(useGUI=not args.batchMode)
    if args.batchMode:
        logger.info('Run ipkobo in batch mode')
    else:
        app.mainloop()


def loggingLevel(levelstring):
    level = logging.INFO
    if levelstring == 'DEBUG':
        level = logging.DEBUG
    elif levelstring == 'INFO':
        level = logging.INFO
    elif levelstring == 'WARNING':
        level = logging.WARNING
    elif levelstring == 'ERROR':
        level = logging.ERROR
    return level

if __name__ == '__main__':
    args = parseArgs()
    logging.basicConfig(level=loggingLevel(args.logLevel),
                        format='%(levelname)8s %(name)-20s: %(message)s')
    run(args)
    
