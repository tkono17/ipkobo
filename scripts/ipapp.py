#!/usr/bin/env python3
#------------------------------------------------------------------------
# ImageProcessingCircle: ipsquareApp.py
#------------------------------------------------------------------------
import argparse
import ipcat

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batch-mode', dest='batchMode',
                        action='store_false', default=False,
                        help='Run in batch mode (no GUI)')
    return parser.parse_args()

def run(args):
    window = ipcat.MainWindow()
    vm = ipcat.ViewModel(window)
    vm.initialize()
    window.mainloop()
    
if __name__ == '__main__':
    args = parseArgs()
    run(args)
    
