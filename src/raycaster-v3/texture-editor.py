import PIL
import numpy as np
from PIL import Image

img: Image.Image = Image.open("images/bricks.jpg")
array1: np.ndarray = np.array(img.resize((100, 100), PIL.Image.ANTIALIAS))
img: Image.Image = Image.open("images/pascal.png")
array2: np.ndarray = np.array(img.resize((100, 100), PIL.Image.ANTIALIAS))
img: Image.Image = Image.open("images/mario.png")
array3: np.ndarray = np.array(img.resize((100, 100), PIL.Image.ANTIALIAS))

a: np.ndarray = np.array([[array1, array1 / 2], [array3, array3 / 2], [array2, array2 / 2]])
