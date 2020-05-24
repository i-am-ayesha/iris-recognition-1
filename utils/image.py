import cv2
import numpy as np
import matplotlib.pyplot as plt
from circle import Circle


class Image:
    def __init__(self, img: np.ndarray = None, image_path: str = None):
        self.img = img
        if image_path is not None:
            self.read(image_path)
        else:
            if img is not None:
                self._update_shape()
            else:
                self.height = None
                self.width = None
                self.num_channels = None

    def _update_shape(self):
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]
        if len(self.img.shape) == 3:
            self.num_channels = self.img.shape[2]
        else:
            self.num_channels = 1

    def read(self, input_image_path: str):
        self.img = cv2.imread(filename=input_image_path)
        self._update_shape()

    def save(self, output_image_path: str):
        assert self.img is not None, "Trying to write an empty binarized_image"
        cv2.imwrite(filename=output_image_path, img=self.img)

    def show(self, title=None, fontsize=15, cmap="gray"):
        plt.imshow(self.img, cmap=cmap)
        if title is not None:
            plt.title(title, fontsize=fontsize)
        plt.show()

    def binarize(self, threshold_factor: float):
        p = np.sum(self.img) / (self.height * self.width)
        p = p / threshold_factor

        # Use binary thresholding
        _, thresholded = cv2.threshold(self.img, p, np.max(self.img),
                                       cv2.THRESH_BINARY)

        return Image(thresholded)

    def erode(self, kernel, iterations=1):
        return Image(cv2.erode(self.img, kernel, iterations=iterations))

    def close(self, kernel):
        return Image(cv2.morphologyEx(self.img, cv2.MORPH_CLOSE, kernel))

    def open(self, kernel):
        return Image(cv2.morphologyEx(self.img, cv2.MORPH_OPEN, kernel))

    def to_bw(self):
        return Image(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY))

    def draw_circle(self, circle: Circle, color=(0, 0, 0), thickness=5):
        return Image(cv2.circle(self.img, (circle.center_x, circle.center_y),
                                circle.radius, color, thickness=thickness))

    def enhance_contrast(self):
        return Image(cv2.equalizeHist(self.img))

    def apply_clahe(self, **kwargs):
        return Image(cv2.createCLAHE(**kwargs).apply(self.img))
