#!/usr/bin/env dls-python
from adPythonPlugin import AdPythonPlugin
import cv2

# These are the operation types
MORPH_ERODE=0
MORPH_DILATE=1
MORPH_OPEN=2
MORPH_CLOSE=3
MORPH_GRADIENT=4
MORPH_TOPHAT=5
MORPH_BLACKHAT=6
MORPH_BLUR=7
MORPH_GAUSSIAN_BLUR=8
MORPH_MEDIAN_BLUR=9
MORPH_ADAPT_THRESH=10


class Morph(AdPythonPlugin):
    def __init__(self):
        params = dict(ksize = 3, operation = 1, iters = 1, on=1)
        AdPythonPlugin.__init__(self, params)

    def processArray(self, arr, attr={}):
        # skip this image?
        if not self["on"]: return
        # got a new image to process
        operation = self["operation"]
        ksize = self["ksize"]
        self.log.debug("ksize=%s, operation=%s", ksize, operation)
        if operation < MORPH_BLUR:
            # Morphological filter
            element = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
            dest = cv2.morphologyEx(arr, operation, element, iterations=self["iters"])
        elif operation == MORPH_BLUR:
            dest = cv2.blur(arr, (ksize, ksize))
        elif operation == MORPH_GAUSSIAN_BLUR:
            dest = cv2.GaussianBlur(arr, (ksize, ksize), 0)
        elif operation == MORPH_MEDIAN_BLUR:
            dest = cv2.medianBlur(arr, ksize)
        elif operation == MORPH_ADAPT_THRESH:
            dest = cv2.adaptiveThreshold(arr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ksize*2+1, ksize)
        return dest

if __name__=="__main__":
    Morph().runOffline(operation=11, ksize=30, iters=30, on=2)
