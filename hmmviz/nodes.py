import matplotlib.pyplot as plt
import numpy as np


class GraphNode:
    def __init__(self, angle, r=1, nodecolor='k', nodesize=20, nodelabel=None, ax=None):
        self.angle = angle
        self.r = r
        self.nodecolor = nodecolor
        self.nodesize = nodesize
        self.nodelabel = nodelabel
        self.ax = ax

    def draw(self, ax=None):
        self.ax = ax or self.ax or plt.gca()
        x, y = np.cos(self.angle) * self.r, np.sin(self.angle) * self.r
        self.ax.scatter(
            [x], [y],
            s=[self.nodesize], c=[self.nodecolor],
            alpha=1 if not self.nodelabel else 0
        )

        if self.nodelabel:
            self.ax.text(x, y, self.nodelabel,
                    horizontalalignment='center',
                    verticalalignment='center',
                    color=self.nodecolor)