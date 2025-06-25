#!/usr/bin/env python3
# ------------------------------------------------------------------------
# Image Processing Workshop: ipkobo.py
# ------------------------------------------------------------------------
import argparse
import logging
import pathlib

from ..app import App

logger = logging.getLogger(__name__)


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--batch-mode",
        dest="batchMode",
        action="store_true",
        default=False,
        help="Run in batch mode (no GUI)",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="logLevel",
        type=str,
        default="INFO",
        help="Logging level DEBUG|INFO|WARNING|ERROR",
    )
    parser.add_argument(
        "-m",
        "--macroFile",
        dest="macroFile",
        type=str,
        default="",
        help="Macr to run at start",
    )
    return parser.parse_args()


def run(args):
    app = App(runMode=App.kBatch)
    if args.batchMode:
        logger.info("Run ipkobo in batch mode")
        if pathlib.Path(args.macroFile).exists():
            app.commandProcessor.processFile(args.macroFile)
    else:
        if pathlib.Path(args.macroFile).exists():
            app.commandProcessor.processFile(args.macroFile)
        app.view.mainloop()


def loggingLevel(levelstring):
    level = logging.INFO
    match levelstring:
        case "DEBUG":
            level = logging.DEBUG
        case "INFO":
            level = logging.INFO
        case "WARNING":
            level = logging.WARNING
        case "ERROR":
            level = logging.ERROR
    return level


def main():
    args = parseArgs()
    logging.basicConfig(
        level=loggingLevel(args.logLevel),
        format="%(levelname)8s %(name)-30s: %(message)s",
    )
    run(args)


if __name__ == "__main__":
    main()
