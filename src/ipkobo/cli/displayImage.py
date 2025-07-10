#!/usr/bin/env python3
import logging
import typer
import cv2

app = typer.Typer()


@app.command()
def run(image_path: str):
    logging.info(f"displayImage {image_path}")
    wname = "win1"
    cv2.namedWindow(wname, cv2.WINDOW_NORMAL)
    img = cv2.imread(image_path)
    cv2.imshow(wname, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO, format="%(name)-20s %(levelname)-8s %(message)s"
    )
    app()


if __name__ == "__main__":
    main("")
