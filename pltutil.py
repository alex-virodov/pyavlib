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


def plt_force_show():
    plt.gcf().canvas.draw()
    plt.show()
    plt.gcf().canvas.flush_events()


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
    figure.tight_layout()
    return axarr

def bgr2rgb(image):
    return image[:, :, (2, 1, 0)]

def rgb2bgr(image):
    return image[:, :, (2, 1, 0)]

def plt_show_in_loop():
    plt.show()
    # thank you https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/
    plt.gcf().canvas.draw()
    plt.gcf().canvas.flush_events()

class UpdatablePlot:
    def __init__(self, ax, set_xdata=True, title=None):
        self.ax = ax
        self.plot_obj_ref = {}
        self.set_xdata = set_xdata
        if title is not None:
            ax.set_title(title)

    def plot_line(self, name, x, y, *args, **kwargs):
        x = x if x is not None else range(len(y))
        if name not in self.plot_obj_ref:
            if 'label' not in kwargs:
                kwargs['label'] = name
            self.plot_obj_ref[name] = self.ax.plot(x, y, *args, **kwargs)[0]
            print(f'{self.plot_obj_ref[name]=}')
        else:
            plot_obj = self.plot_obj_ref[name]
            if self.set_xdata:
                plot_obj.set_xdata(x)
            plot_obj.set_ydata(y)

    def relim(self):
        self.ax.relim()
        self.ax.autoscale_view()

class DoubleSidedUpdatablePlot:
    def __init__(self, ax):
        self.axs = [ax, ax.twinx()]
        self.plot_obj_ref = {}

    def foreach_ax(self, callback):
        for ax in self.axs:
            callback(ax)

    def plot_line(self, name, x, y, *args, **kwargs):
        x = x if x is not None else range(len(y))
        if name not in self.plot_obj_ref:
            self.plot_obj_ref[name] = self.axs[0].plot(x, y, *args, **kwargs)[0]
            print(f'{self.plot_obj_ref[name]=}')
        else:
            plot_obj = self.plot_obj_ref[name]
            plot_obj.set_xdata(x)
            plot_obj.set_ydata(y)

    def relim(self):
        self.axs[0].relim()
        self.axs[0].autoscale_view()
        self.axs[1].set_ylim(self.axs[0].get_ylim())
        self.axs[1].autoscale_view()

class ImageUpdatablePlot:
    def __init__(self, ax):
        self.ax = ax
        self.plot_obj_ref = None

    def imshow(self, image):
        if self.plot_obj_ref is None:
            self.plot_obj_ref = self.ax.imshow(image)
        else:
            self.plot_obj_ref.set_data(image)


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

