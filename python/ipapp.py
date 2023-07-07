#!/usr/bin/env python3
#------------------------------------------------------------------------
# Image Processing Application: ipapp.py
#------------------------------------------------------------------------
import argparse
import logging

import ipcat

log = logging.getLogger(__name__)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batch-mode', dest='batchMode',
                        action='store_false', default=False,
                        help='Run in batch mode (no GUI)')
    return parser.parse_args()

def run(args):
    model = ipcat.AppData()
    gui = ipcat.MainWindow(model)
    app = ipcat.App(model, gui)
    #
    gui.mainloop()
    
if __name__ == '__main__':
    args = parseArgs()
    logging.basicConfig(level=logging.DEBUG)
    run(args)
    
