import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib
from enum import Enum
from pyavlib.pltutil import plt_clf_subplots

class OptVisCommands(Enum):
    InputPoll = 1

def inifinte_iterate(iter_fn):
    def looper():
        while True:
            yield iter_fn()
    return looper


def optimization_visualization_subplots(plot_rows, plot_cols, subplot_kws_map={}, rowspan_colspan_map={}):
    ax = plt_clf_subplots(plot_rows, plot_cols, subplot_kws_map, rowspan_colspan_map)

    # Force to top once (but not during running, intentional).
    matplotlib.rcParams['figure.raise_window'] = True
    plt.show()
    matplotlib.rcParams['figure.raise_window'] = False

    return plt.gcf(), ax


def optimization_visualization(fig, ax, compute_fn, draw_fn, count_hint=None):
    from pyavlib.optimization_visualization_session_store import optimization_visualization_session_store

    # Remove previous run's listeners. TODO: reuse?
    # (Not removing at the end of run to allow interactivity after the run is done).
    print(f'{optimization_visualization_session_store=}')
    for object in optimization_visualization_session_store:
        if isinstance(object, plt.Widget):
            object.disconnect_events()
        else:
            fig.canvas.mpl_disconnect(object)
    optimization_visualization_session_store.clear()

    keep_running = True
    frame_count = count_hint if count_hint is not None else 1

    fig.subplots_adjust(left=0.05, bottom=0.15, right=0.95, top=0.95)
    time_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    freq_slider = plt.Slider(
        ax=time_slider_ax,
        label='Starting up...',
        valmin=0,
        valmax=frame_count - 1,
        valinit=0,
        valstep=1
    )
    optimization_visualization_session_store.append(freq_slider)

    #pause_resume_button_axes = plt.axes([0.85, 0.05, 0.1, 0.03])
    #pause_resume_button = plt.Button(pause_resume_button_axes, 'todo Pause')
    #optimization_visualization_session_store.append(pause_resume_button)


    # Force to top once (but not during running, intentional).
    matplotlib.rcParams['figure.raise_window'] = True
    plt.show()
    matplotlib.rcParams['figure.raise_window'] = False

    def on_press(event):
        nonlocal keep_running
        print(f'on_press {event.key=} {event=}')
        if event.key == 'escape':
            keep_running = False

    cid = fig.canvas.mpl_connect('key_press_event', on_press)
    optimization_visualization_session_store.append(cid)

    current_frame = -1
    for state in compute_fn():
        # print(f'{keep_running=}')
        if not keep_running or not plt.fignum_exists(fig.number):
            break
        if state is OptVisCommands.InputPoll:
            pass # pass on drawing :) Still do events
        else:
            current_frame += 1
            if current_frame >= frame_count:
                frame_count = current_frame + 1
                freq_slider.label.set_text(f'Running ({frame_count})...')
                freq_slider.valmax = frame_count - 1
                time_slider_ax.set_xlim(0, freq_slider.valmax)
            freq_slider.set_val(current_frame)


            if state is None:
                draw_fn()
            else:
                # https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
                try:
                    draw_fn(*state)
                except TypeError:
                    draw_fn(state)
            plt.show()
            # thank you https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/
            fig.canvas.draw()
        fig.canvas.flush_events()

    freq_slider.label.set_text(f'Stopped ({frame_count})')
    plt.show()


def main1():
    fig, ax = optimization_visualization_subplots(2, 2)

    x = np.linspace(-2.0, 2.0, num=256)
    ax[0][0].plot(x, x * 0 + 1, 'k--')

    def draw(mu, sigma=0.2):
        """
        :type fig: plt.Figure
        :type ax: list[list[plt.Axes]]
        """
        plt.sca(ax[0][0])
        plt.plot(x, x * mu)
        plt.title(f'{mu=}')

        plt.sca(ax[1][0])
        plt.cla()
        plt.plot(x, x * mu)
        plt.gca().set_aspect('equal', adjustable='datalim')

    def compute():
        for mu in np.linspace(-1.0, 1.0, num=16):
            yield mu

    optimization_visualization(fig, ax, compute, draw, count_hint=16)


def main2():
    fig, ax = optimization_visualization_subplots(2, 2)

    # We can also not return state (pass it via scope globals), but then we can't seek.
    mu = 0

    def compute():
        nonlocal mu
        for i in range(16):
            for i in range(10):
                time.sleep(0.05)  # Pretend there's a lot of compute here.
                yield OptVisCommands.InputPoll # Cooperative multitasking :) Maybe not needed.
            yield None
            mu += 0.1

    x = np.linspace(-2.0, 2.0, num=256)

    def draw():
        """
        :type fig: plt.Figure
        :type ax: list[list[plt.Axes]]
        """
        plt.sca(ax[0][0])
        plt.plot(x, x * mu)
        plt.title(f'{mu=}')

        plt.sca(ax[1][0])
        plt.cla()
        plt.plot(x, x * mu)
        plt.gca().set_aspect('equal', adjustable='datalim')


    optimization_visualization(fig, ax, compute, draw, count_hint=16)





if __name__ == "__main__":
    main1()
    main2()