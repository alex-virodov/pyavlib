import matplotlib.pyplot as plt
import itertools
import numpy as np


def plot_rect_wh(ax, x0, y0, w, h, col):
    plot_rect(ax, x0, y0, x0+w, y0+h, col)


def plot_rect(ax, x0, y0, x1, y1, col):
    ax.plot([x0, x0, x1, x1, x0], [y0, y1, y1, y0, y0], col)


def plt_sca_cla(ax, title=None):
    plt.sca(ax)
    ax.cla()
    if title is not None:
        plt.title(title)

def plt_clf_subplots(n, m, subplot_kws_map = {}, rowspan_colspan_map = {}):
    """Clears figure and returns a flat list of axes"""
    plt.clf()

    # Create array to hold all axes.
    # Copy of matplotlib/gridspec.py v3.4.3 subplots function, but with per-ax kwargs
    figure = plt.gcf()
    axarr = []
    spanned_indexes = [] # Todo: more efficient search? List is usually small, O(10)
    gs = figure.add_gridspec(n, m)
    for i in range(n * m):
        if i in rowspan_colspan_map:
            r = i // m
            c = i % m
            for j in range (rowspan_colspan_map[i][0]):
                for k in range(rowspan_colspan_map[i][1]):
                    idx = (r + j) * m + (c + k)
                    if idx in spanned_indexes:
                        raise ValueError(f'Index {idx} is spanned by some other axes.')
                    spanned_indexes.append(idx)
            axarr.append(figure.add_subplot(
                gs[r:r+rowspan_colspan_map[i][0], c:c+rowspan_colspan_map[i][1]],
                **subplot_kws_map.get(i, {})))
        else:
            if i not in spanned_indexes:
                # print(f'making subplot {i//m=} {i%m=} {spanned_indexes=}')
                axarr.append(figure.add_subplot(gs[i // m, i % m], **subplot_kws_map.get(i, {})))

    return axarr

def bgr2rgb(image):
    return image[:, :, (2, 1, 0)]

def rgb2bgr(image):
    return image[:, :, (2, 1, 0)]


if __name__ == "__main__":
    print("start")

    ax = plt_clf_subplots(4, 3,
                          subplot_kws_map={1:{'projection': '3d'}},
                          rowspan_colspan_map={1: (2, 2)})
    print(ax)
    plot_rect(ax[0], 0, 0, 10, 10, 'r')
    plot_rect(ax[0], 5, 9.3, 32, 4, 'g--')
    plot_rect_wh(ax[0], 5, 9.3, 32, 4, 'b--')

    plt.sca(ax[1])
    zdata = 15 * np.random.random(100)
    xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
    ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
    plt.scatter(xdata, ydata, zdata, c=zdata, cmap='Greens')


    plt.show()

