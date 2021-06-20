import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib import patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

matplotlib.use('Qt5Agg')
import numpy as np

class Kurvenplot2(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = plt.figure()

        self.g = 9.81
        self.axes = None

        super(Kurvenplot2, self).__init__(self.fig)

    def updatePlots(self, angle, velocity, radius, angle_sled, g_difference):
        self.fig.clear()
        self.axes = []
        self.axes.append(self.fig.add_subplot(121))
        self.axes.append(self.fig.add_subplot(122))

        a_centrifugal = velocity * velocity / radius;

        a_radial = np.sin(angle) * a_centrifugal + np.cos(angle) * self.g
        a_tangential = np.cos(angle) * a_centrifugal - np.sin(angle) * self.g

        R = np.array(((np.cos(angle), -np.sin(angle)), (np.sin(angle), np.cos(angle))))

        # draw semicircle
        center_arc = (0, 5)
        radius_arc = 5
        circ = patches.Arc(center_arc, 2 * radius_arc, 2 * radius_arc,
                 angle=-90, linewidth=4, fill=False, theta2=180)
        self.axes[0].add_patch(circ)

        # draw simple sled
        center_bob = np.array(center_arc) + (radius_arc - 1) * np.array([np.sin(angle), -np.cos(angle)])
        size_bob = np.array([1.7, 1.3])
        bob = patches.Rectangle(center_bob - 0.5 * np.matmul(R, size_bob), size_bob[0], size_bob[1],
                 angle=angle*180/np.pi, linewidth=2, fill=True, facecolor='lightgrey', edgecolor='grey')
        self.axes[0].add_patch(bob)

        start_left_runner = center_bob - np.matmul(R, np.array([0.5 * size_bob[0], 0.5 * size_bob[1]]))
        start_right_runner = center_bob - np.matmul(R, np.array([-0.5 * size_bob[0], 0.5 * size_bob[1]]))
        runner_length = 0.2 # TODO calculate correct length
        end_left_runner = start_left_runner - np.matmul(R, np.array([0, runner_length]))
        end_right_runner = start_right_runner - np.matmul(R, np.array([0, runner_length]))
        self.axes[0].plot([start_left_runner[0], end_left_runner[0]], [start_left_runner[1], end_left_runner[1]], c='grey', linewidth=2)
        self.axes[0].plot([start_right_runner[0], end_right_runner[0]], [start_right_runner[1], end_right_runner[1]], c='grey', linewidth=2)

        # draw forces
        a_fg = self.axes[0].arrow(center_bob[0], center_bob[1], 0, -1, width=0.05, color='blue', length_includes_head=True, label='$F_g$')
        a_cf = self.axes[0].arrow(center_bob[0], center_bob[1], a_centrifugal / self.g, 0, width=0.05, color='violet', length_includes_head=True, label='$F_{cf}$')
        a_tot = self.axes[0].arrow(center_bob[0], center_bob[1], a_centrifugal / self.g, -1, width=0.05, color='gold', length_includes_head=True, label='$F_{tot}$')
        a_rad = self.axes[0].arrow(center_bob[0], center_bob[1], a_radial * np.sin(angle) / self.g, -a_radial * np.cos(angle) / self.g,
                                width=0.05, color='saddlebrown', length_includes_head=True, label='$F_{rad}$')
        start = [center_bob[0] + a_radial * np.sin(angle) / self.g, center_bob[1] - a_radial * np.cos(angle) / self.g]
        if a_tangential > 0.0:
            color = 'red'
        else:
            color = 'darkgreen'
        a_tan = lines.Line2D([start[0], start[0] + a_tangential * np.cos(angle) / self.g],
                               [start[1], start[1] + a_tangential * np.sin(angle) / self.g],
                                linewidth=4, color=color, solid_capstyle='butt', label='$F_{tan}$')
        self.axes[0].add_line(a_tan)
        self.axes[0].legend(handles = [a_fg, a_cf, a_tot, a_rad, a_tan])
        
        # draw sled top - down (Achsabstand: 2.13 m, Spurbreite: 0.67 m, pro achse + 0.6 m
        size_bob_td = (3.33, 0.60)
        R_td = np.array(((np.cos(angle_sled), -np.sin(angle_sled)), (np.sin(angle_sled), np.cos(angle_sled))))

        bob_td = patches.Rectangle((0,0) - 0.5 * np.matmul(R_td, size_bob_td), size_bob_td[0], size_bob_td[1],
                 angle=angle_sled*180/np.pi, linewidth=2, fill=True, facecolor='lightgrey', edgecolor='grey')
        self.axes[1].add_patch(bob_td)

        runner_length_front_td = 0.75
        runner_length_back_td = 1.0
        start_left_fr_runner_td = np.matmul(R_td, np.array([-1.065 + 0.5*runner_length_front_td, -0.335]))
        start_right_fr_runner_td = np.matmul(R_td, np.array([-1.065 + 0.5*runner_length_front_td, 0.335]))
        start_left_br_runner_td = np.matmul(R_td, np.array([1.065 + 0.5*runner_length_back_td, -0.335]))
        start_right_br_runner_td = np.matmul(R_td, np.array([1.065 + 0.5*runner_length_back_td, 0.335]))
        end_left_fr_runner_td = start_left_fr_runner_td - np.matmul(R_td, np.array([runner_length_front_td, 0]))
        end_left_br_runner_td = start_left_br_runner_td - np.matmul(R_td, np.array([runner_length_back_td, 0]))
        end_right_fr_runner_td = start_right_fr_runner_td - np.matmul(R_td, np.array([runner_length_front_td, 0]))
        end_right_br_runner_td = start_right_br_runner_td - np.matmul(R_td, np.array([runner_length_back_td, 0]))
        self.axes[1].plot([start_left_fr_runner_td[0], end_left_fr_runner_td[0]], [start_left_fr_runner_td[1], end_left_fr_runner_td[1]], c='grey', linewidth=2)
        self.axes[1].plot([start_left_br_runner_td[0], end_left_br_runner_td[0]], [start_left_br_runner_td[1], end_left_br_runner_td[1]], c='grey', linewidth=2)
        self.axes[1].plot([start_right_fr_runner_td[0], end_right_fr_runner_td[0]], [start_right_fr_runner_td[1], end_right_fr_runner_td[1]], c='grey', linewidth=2)
        self.axes[1].plot([start_right_br_runner_td[0], end_right_br_runner_td[0]], [start_right_br_runner_td[1], end_right_br_runner_td[1]], c='grey', linewidth=2)

        # forces top down
        b = np.sin(angle_sled) * 1.065
        angle_diff = 2 * np.arcsin(0.5*b/radius_arc)
        a_tan_front = np.cos(angle-angle_diff) * a_centrifugal * (1.0 - g_difference) - np.sin(angle-angle_diff) * self.g
        a_tan_back = np.cos(angle+angle_diff) * a_centrifugal * (1.0 + g_difference) - np.sin(angle+angle_diff) * self.g
        a_forward = (a_tan_front + a_tan_back) * np.sin(angle_sled)

        center_front_axle = np.matmul(R_td, np.array([-1.065, 0]))
        center_back_axle = np.matmul(R_td, np.array([1.065, 0]))
        arrow_tan_front = self.axes[1].arrow(center_front_axle[0], center_front_axle[1], 0, a_tan_front / self.g, width=0.05, color='blue', length_includes_head=True, label='$F_{tan front}$')
        arrow_tan_back = self.axes[1].arrow(center_back_axle[0], center_back_axle[1], 0, a_tan_back / self.g, width=0.05, color='cyan', length_includes_head=True, label='$F_{tan back}$')
        arrow_combined = self.axes[1].arrow(0, 0, 0, (a_tan_back + a_tan_front), width=0.05, color='gold', length_includes_head=True, label='$F_{tan tot} \cdot 10$')
        arrow_forward = self.axes[1].arrow(0, 0, 4*a_forward*np.cos(angle_sled), 4*a_forward*np.sin(angle_sled), width=0.05, color='green', length_includes_head=True, label='$F_{forward} \cdot 40$')

        self.axes[1].legend(handles = [arrow_tan_front, arrow_tan_back, arrow_combined, arrow_forward])
        self.axes[1].set_ylim([-1.5, 1.5])

        self.axes[0].set_aspect('equal', 'box')
        self.axes[1].set_aspect('equal', 'box')
        self.fig.canvas.draw_idle()

    def redraw(self):
        if self.axes:
            self.fig.canvas.draw_idle()
