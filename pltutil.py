import matplotlib.pyplot as plt


def plot_rect_wh(ax, x0, y0, w, h, col):
    plot_rect(ax, x0, y0, x0+w, y0+h, col)


def plot_rect(ax, x0, y0, x1, y1, col):
    ax.plot([x0, x0, x1, x1, x0], [y0, y1, y1, y0, y0], col)


def plt_sca_cla(ax, title=None):
    plt.sca(ax)
    ax.cla()
    if title is not None:
        plt.title(title)

if __name__ == "__main__":
    print("start")

    plt.clf()
    ax = plt.gca()
    plot_rect(ax, 0, 0, 10, 10, 'r')
    plot_rect(ax, 5, 9.3, 32, 4, 'g--')
    plot_rect_wh(ax, 5, 9.3, 32, 4, 'b--')
    plt.show()

