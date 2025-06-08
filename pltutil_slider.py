from pyavlib.optimization_visualization_session_store import optimization_visualization_session_store
import matplotlib
import matplotlib.pyplot as plt


class MatplotlibInteractiveFigureSlider:
    def __init__(self):
        # Call insert_slider() after figure was initialized/laid out
        self.time_slider_ax = None
        self.freq_slider = None

        # Remove previous run's listeners. TODO: reuse?
        # (Not removing at the end of run to allow interactivity after the run is done).
        print(f'{optimization_visualization_session_store=}')
        for object in optimization_visualization_session_store:
            if isinstance(object, plt.Widget):
                object.disconnect_events()
            else:
                plt.gcf().canvas.mpl_disconnect(object)
        optimization_visualization_session_store.clear()

    def force_figure_to_top(self):
        matplotlib.rcParams['figure.raise_window'] = True
        plt.show()
        matplotlib.rcParams['figure.raise_window'] = False

    def insert_slider(self):
        plt.gcf().subplots_adjust(left=0.05, bottom=0.15, right=0.95, top=0.95)
        self.time_slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='lightgoldenrodyellow')
        self.freq_slider = plt.Slider(
            ax=self.time_slider_ax,
            label='Starting up...',
            valmin=0,
            valmax=1,
            valinit=0,
            valstep=1,
            handle_style={'size': 20}
        )
        self.freq_slider.dragging = False
        optimization_visualization_session_store.append(self.freq_slider)

    def update_slider(self, len_states):
        self.freq_slider.label.set_text(f'Running ({len_states})...')
        self.freq_slider.valmax = len_states - 1
        self.time_slider_ax.set_xlim(0, self.freq_slider.valmax)
        self.freq_slider.set_val(self.freq_slider.valmax)

    def enable_dragging(self, callback):
        self.freq_slider.on_changed(callback)
        self.freq_slider.dragging = True
        self.freq_slider.label.set_text(f'Stopped ({self.freq_slider.valmax + 1})')
