import argparse
import numpy as np
import scipy.signal
from PIL import Image

parser = argparse.ArgumentParser(description='')
parser.add_argument('source', type=str)
parser.add_argument('dest', type=str)
parser.add_argument('--smooth_radius', type=int, default=0)
args = parser.parse_args()
assert not args.dest.lower().endswith('.jpg'), 'JPG format does not support transparency'

img = Image.open(args.source)
img = img.convert('RGBA')
img_data = np.array(img)
data = img_data.reshape(-1, 4)

mask = (data[:, :3] == 255).all(axis=1)
if args.smooth_radius > 0:
    mask = mask.reshape(img_data.shape[:-1])
    width = args.smooth_radius * 2 + 1
    kernel = np.ones((width, width)) / (width * width)
    mask = np.isclose(scipy.signal.convolve2d(mask, kernel, mode='same', boundary='fill', fillvalue=1), 1)
    mask = mask.reshape(-1)
data[mask, 3] = 0

Image.fromarray(data.reshape(img_data.shape)).save(args.dest)