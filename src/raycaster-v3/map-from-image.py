import numpy as np
from PIL import Image

img: Image.Image = Image.open('floor-plans/plan2.png')
img: Image.Image = img.convert('1')
img: np.ndarray = np.array(img.resize((30, 30)), dtype=int)
img: np.ndarray = np.abs(img - 1)
