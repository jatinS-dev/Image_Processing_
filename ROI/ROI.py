from PIL import Image
import numpy as np


def create_circular_mask(h, w, center=[964, 1110], radius=80):
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((Y - center[0]) ** 2 + (X - center[1]) ** 2)
    res = dist <= radius
    return res


def convolve3d(image, kernel):
    output = np.zeros_like(image)
    padding = np.zeros(
        (image.shape[0] + kernel.shape[0] - 1, image.shape[1] + kernel.shape[1] - 1, image.shape[2]))
    padding[kernel.shape[0] - 2:-1:, kernel.shape[1] - 2:-1:, :] = image
    padding[0, 0, :] = image[0, 0, :]
    padding[-1, -1, :] = image[-1, -1, :]
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            for z in range(image.shape[2]):
                result = (kernel * padding[y: y + kernel.shape[0], x: x + kernel.shape[1], z]).sum()
                output[y, x, z] = result
    if image.shape[2] == 4:
        output[:, :, 3] = image[:, :, 3]
    return output


gauss = np.array([[1, 4, 6, 4, 1],
                           [4, 16, 24, 16, 4],
                           [6, 24, 36, 24, 6],
                           [4, 16, 24, 16, 4],
                           [1, 4, 6, 4, 1]]) / 256

img = "roi.jpeg"
roiImg = "logo.png"

im = np.array(Image.open(img))
im = convolve3d(im, gauss)
mask = create_circular_mask(im.shape[0], im.shape[1])
masked = im.copy()
masked[~mask] = 0
row_shift = -25
column_shift = -670
for i in range(im.shape[0]):
    for j in range(im.shape[1]):
        if masked[i, j, :].all() != 0:
            masked[i + row_shift, j + column_shift, :] = masked[i, j, :]
            masked[i, j, :] = 0
            im[i + row_shift, j + column_shift, :] = 0

im = np.bitwise_or(im, masked)
roi = Image.fromarray(im.astype(np.uint8))
# roi.save('moved.jpeg')
roi.show()
