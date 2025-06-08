import matplotlib.pyplot as plt
from pyavlib.pltutil import plt_clf_subplots, UpdatablePlot, plt_show_in_loop
from pyavlib.keyboard_util import ExitOnKey
import numpy as np
import time
from pyavlib.pltutil_slider import MatplotlibInteractiveFigureSlider

# this must be run in interactive python console. TODO: fix it so it works both ways.

def box_around(pos):
    return pos

class Simulation:
    def __init__(self):
        self.positions = np.array([[0,0], [1, 0.1], [2, 0.2], [3, 0.3]])
        self.box_idxs = [0, 0, 1, 3]
        self.i = 0
        self.x_list = [self.positions[0][0]]

    def get_state(self):
        i = (self.i % len(self.positions))
        return (self.positions[i], box_around(self.positions[self.box_idxs[i]]), self.x_list.copy())

    def step(self):
        self.i += 1
        self.x_list.append(self.positions[self.i % len(self.positions)][0])

        time.sleep(0.25)  # pretend doing work here


        # if self.i == len(self.positions):
        #     raise StopIteration

    def get_max_steps(self):
        return 10

class Visualizer:
    def __init__(self):
        self.ax = plt_clf_subplots(2, 2)
        self.ax = UpdatablePlot.convert_all_ax(self.ax)

    def visualize_state(self, state):
        e = 0.05
        position, box, x_list = state
        self.ax[0].plot_line('a', [box[0] + e, box[0] + e, box[0] - e, box[0] - e],
                     [box[1] + e, box[1] - e, box[1] - e, box[1] + e, ], 'r-')
        self.ax[0].plot_line('b', position[0], position[1], 'xb')

        self.ax[1].plot_line('c', None, x_list, 'go-')
        self.ax[1].relim()

    def after_first_visualization(self):
        self.ax[0].ax.set_xlim(-1, 4)
        self.ax[0].ax.set_ylim(-2, 3)
        self.ax[0].ax.legend()



def main():
    sim = Simulation()
    visualizer = Visualizer()
    mpl_slider = MatplotlibInteractiveFigureSlider()

    # Force to top once (but not during running, intentional).
    mpl_slider.force_figure_to_top()
    mpl_slider.insert_slider()

    states = [sim.get_state()]
    visualizer.visualize_state(states[-1])
    visualizer.after_first_visualization()
    plt_show_in_loop()

    is_exit = ExitOnKey()

    for i in range(sim.get_max_steps()):
        if is_exit:
            break

        sim.step()
        states.append(sim.get_state())
        visualizer.visualize_state(states[-1])
        mpl_slider.update_slider(len(states))
        plt_show_in_loop()

    # Intentionally enabling dragging only after simulation stopped.
    def on_changed(val):
        print(f'on_changed {val=}')
        visualizer.visualize_state(states[val])

    mpl_slider.enable_dragging(on_changed)


if __name__ == '__main__':
    main()