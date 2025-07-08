#!/usr/bin/env python3
import logging
import typer
import cv2

app = typer.Typer()


@app.command()
def run(image_path: str,
        thr_value: int = 150):
    logging.info(f"displayImage {image_path}")
    wname1 = "win1"
    wname2 = "win2"
    cv2.namedWindow(wname1, cv2.WINDOW_NORMAL)
    cv2.namedWindow(wname2, cv2.WINDOW_NORMAL)
    img = cv2.imread(image_path)

    img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thr1, img_high = cv2.threshold(img_bw, thr_value, 255, cv2.THRESH_BINARY)

    cv2.imshow(wname1, img_bw)
    cv2.imshow(wname2, img_high)
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
