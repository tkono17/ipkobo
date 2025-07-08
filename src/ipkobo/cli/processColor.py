#!/usr/bin/env python3
import logging
import typer
import matplotlib.pyplot as plt
import cv2

app = typer.Typer()


@app.command()
def run(image_path: str):
    logging.info(f"displayImage {image_path}")
    wname = "win1"

    img = cv2.imread(image_path)

    img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.namedWindow(wname, cv2.WINDOW_NORMAL)
    #cv2.imshow(wname, img_bw)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(img_bw, bins=256, range=(0, 256))
    fig.show()
    
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO, format="%(name)-20s %(levelname)-8s %(message)s"
    )
    app()


if __name__ == "__main__":
    main("")
