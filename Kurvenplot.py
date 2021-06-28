import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib import patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

matplotlib.use('Qt5Agg')
import numpy as np

class Kurvenplot(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = plt.figure()

        self.g = 9.81
        self.axes = None

        super(Kurvenplot, self).__init__(self.fig)

    def updatePlots(self, angle, velocity, radius):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_aspect('equal', 'box')

        a_centrifugal = velocity * velocity / radius;

        a_radial = np.sin(angle) * a_centrifugal + np.cos(angle) * self.g
        a_tangential = np.cos(angle) * a_centrifugal - np.sin(angle) * self.g

        R = np.array(((np.cos(angle), -np.sin(angle)), (np.sin(angle), np.cos(angle))))

        # draw semicircle
        center_arc = (0, 5)
        radius_arc = 5
        circ = patches.Arc(center_arc, 2 * radius_arc, 2 * radius_arc,
                 angle=-90, linewidth=4, fill=False, theta2=180)
        self.axes.add_patch(circ)

        # draw simple sled
        center_bob = np.array(center_arc) + (radius_arc - 1) * np.array([np.sin(angle), -np.cos(angle)])
        size_bob = np.array([1.7, 1.3])
        bob = patches.Rectangle(center_bob - 0.5 * np.matmul(R, size_bob), size_bob[0], size_bob[1],
                 angle=angle*180/np.pi, linewidth=2, fill=True, facecolor='lightgrey', edgecolor='grey')
        self.axes.add_patch(bob)

        start_left_runner = center_bob - np.matmul(R, np.array([0.5 * size_bob[0], 0.5 * size_bob[1]]))
        start_right_runner = center_bob - np.matmul(R, np.array([-0.5 * size_bob[0], 0.5 * size_bob[1]]))
        runner_length = 0.2 # TODO calculate correct length
        end_left_runner = start_left_runner - np.matmul(R, np.array([0, runner_length]))
        end_right_runner = start_right_runner - np.matmul(R, np.array([0, runner_length]))
        self.axes.plot([start_left_runner[0], end_left_runner[0]], [start_left_runner[1], end_left_runner[1]], c='grey', linewidth=2)
        self.axes.plot([start_right_runner[0], end_right_runner[0]], [start_right_runner[1], end_right_runner[1]], c='grey', linewidth=2)

        # draw forces
        a_fg = self.axes.arrow(center_bob[0], center_bob[1], 0, -1, width=0.05, color='blue', length_includes_head=True, label='$F_g$')
        a_cf = self.axes.arrow(center_bob[0], center_bob[1], a_centrifugal / self.g, 0, width=0.05, color='violet', length_includes_head=True, label='$F_{cf}$')
        a_tot = self.axes.arrow(center_bob[0], center_bob[1], a_centrifugal / self.g, -1, width=0.05, color='gold', length_includes_head=True, label='$F_{tot}$')
        a_rad = self.axes.arrow(center_bob[0], center_bob[1], a_radial * np.sin(angle) / self.g, -a_radial * np.cos(angle) / self.g,
                                width=0.05, color='saddlebrown', length_includes_head=True, label='$F_{rad}$')
        start = [center_bob[0] + a_radial * np.sin(angle) / self.g, center_bob[1] - a_radial * np.cos(angle) / self.g]
        if a_tangential > 0.0:
            color = 'red'
        else:
            color = 'darkgreen'
        a_tan = lines.Line2D([start[0], start[0] + a_tangential * np.cos(angle) / self.g],
                               [start[1], start[1] + a_tangential * np.sin(angle) / self.g],
                                linewidth=4, color=color, solid_capstyle='butt', label='$F_{tan}$')
        self.axes.add_line(a_tan)
        self.axes.legend(handles = [a_fg, a_cf, a_tot, a_rad, a_tan], bbox_to_anchor=(1.05, 1.0), loc='upper left')
        self.axes.set_xlim(left=-1.0)
        self.fig.canvas.draw_idle()

    def redraw(self):
        if self.axes:
            self.fig.canvas.draw_idle()
