#!/usr/bin/env python3
import logging
import typer
import cv2

app = typer.Typer()


@app.command()
def main(imagePath: str):
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO, format="%(name)-20s %(levelname)-8s %(message)s"
    )
    logging.info(f"displayImage {imagePath}")


if __name__ == "__main__":
    main()
