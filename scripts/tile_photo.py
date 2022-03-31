import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='')
parser.add_argument('source', type=str)
parser.add_argument('dest', type=str)
parser.add_argument('--n_rows', type=int, default=2)
parser.add_argument('--n_cols', type=int, default=3)
parser.add_argument('--border', action='store_true')
parser.add_argument('--img_width', type=str, default='2in')
parser.add_argument('--img_height', type=str, default='2in')
parser.add_argument('--total_width', type=int, default=6)
parser.add_argument('--total_height', type=int, default=4)
parser.add_argument('--x_offset', type=str, default='0.1in')
parser.add_argument('--y_offset', type=str, default='0.1in')
args = parser.parse_args()

img = plt.imread(sys.argv[1])
if np.issubdtype(img.dtype, np.integer):
    img = img.astype(np.float32) / 255
assert args.img_width[-2:] in ['in', 'mm']
H_img_in = float(args.img_height[:-2])
W_img_in = float(args.img_width[:-2])
if args.img_width[-2:] == 'mm':
    H_img_in /= 25.4
    W_img_in /= 25.4
x_offset_in = float(args.x_offset[:-2])
y_offset_in = float(args.y_offset[:-2])
if args.x_offset[-2:] == 'mm':
    x_offset_in /= 25.4
    y_offset_in /= 25.4
H_img_pix, W_img_pix, _ = img.shape
pix_per_in = H_img_pix / H_img_in
if args.border:
    new_img = np.zeros((img.shape[0] + 2, img.shape[1] + 2, img.shape[2]), dtype=np.float32)
    if img.shape[2] == 4: # RGBA
        new_img[:, :, -1] = 1.0
    new_img[1:-1, 1:-1] = img
    img = new_img
    H_img_pix, W_img_pix, _ = img.shape
H_total_pix, W_total_pix = round(pix_per_in * args.total_height), round(pix_per_in * args.total_width)
x_offset_pix = x_offset_in * pix_per_in
y_offset_pix = y_offset_in * pix_per_in

new_img = np.zeros((H_total_pix, W_total_pix, img.shape[2]), dtype=np.float32)
new_img[:, :, :] = 1.0
for j in range(args.n_rows):
    for i in range(args.n_cols):
        y_offset = int(y_offset_pix + (H_total_pix - y_offset_pix) / args.n_rows * j)
        x_offset = int(x_offset_pix + (W_total_pix - x_offset_pix) / args.n_cols * i)
        new_img[y_offset: y_offset + H_img_pix, x_offset: x_offset + W_img_pix] = img
img = new_img

fig = plt.figure(frameon=False)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
plt.imshow(img, aspect='auto')
fig.set_size_inches(6, 4)
plt.savefig(args.dest, dpi=300)
