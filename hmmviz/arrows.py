from matplotlib.path import Path
from matplotlib.patches import FancyArrowPatch, ArrowStyle
import matplotlib.pyplot as plt
import numpy as np


class GraphArrow:
    def __init__(self, angleA, angleB, r=1, inner=False, outer=False, stretch_inner=0.8, stretch_outer=1.1, shrinkA=20, shrinkB=20,
                 arrowstyle='-|>', head_length=3, head_width=2, connectionstyle="arc3,rad=0.3",
                 outer_connectionstyle="arc3,rad=-0.3", edgewidth=1, edgecolor='k', ax=None, label=None,
                 labelpos=0.5, label_facecolor='white', label_edgecolor='white', label_color='k', alpha=0, xytext=None):
        self.angleA = angleA
        self.angleB = angleB
        self.r = r
        self.posA = np.array([np.cos(self.angleA), np.sin(self.angleA)])
        self.posB = np.array([np.cos(self.angleB), np.sin(self.angleB)])
        self.outer = outer
        self.stretch_outer = stretch_outer
        self.shrinkA = shrinkA
        self.shrinkB = shrinkB
        self.arrowstyle = arrowstyle
        self.head_length = head_length
        self.head_width = head_width
        self.connectionstyle = connectionstyle
        self.outer_connectionstyle = outer_connectionstyle
        self.edgewidth = edgewidth
        self.edgecolor = edgecolor
        self.ax = ax
        self.label = label
        self.labelpos = labelpos
        self.label_facecolor = label_facecolor
        self.label_edgecolor = label_edgecolor
        self.label_color = label_color
        self.alpha = alpha
        self.inner = inner
        self.stretch_inner = stretch_inner
        self.xytext = xytext

    def draw(self, ax=None):
        self.ax = ax or self.ax or plt.gca()
        self.arrow = FancyArrowPatch(
            posA=(self.posA if not self.outer else (self.posA * self.stretch_outer)) * self.r,
            posB=(self.posB if not self.outer else (self.posB * self.stretch_outer)) * self.r,
            arrowstyle=ArrowStyle(
                self.arrowstyle, head_length=self.head_length, head_width=self.head_width
            ),
            shrinkA=(self.shrinkA * (self.stretch_outer ** 2 if self.outer else 1)),
            shrinkB=(self.shrinkB * (self.stretch_outer ** 2 if self.outer else 1)),
            connectionstyle=self.connectionstyle if not self.outer else self.outer_connectionstyle,
            linewidth=self.edgewidth,
            color=self.edgecolor
        )
        self.ax.add_patch(self.arrow)

        if self.label:
            verts = self.arrow.get_path().vertices
            point = verts[1]
            norm = np.linalg.norm(point)
            self.ax.text(
                *((self.xytext if self.xytext is not None else point) * (self.stretch_inner if self.inner else 1.12)), self.label,
                horizontalalignment='center', verticalalignment='center',
                bbox=dict(facecolor=self.label_facecolor, edgecolor=self.label_edgecolor, alpha=self.alpha),
                color=self.label_color
            )

class SelfGraphArrow:
    def __init__(self, angle, r=1, circ_stretch=1.4, circ_rad=0.3, shrink=np.pi/4, arrowstyle='-|>',
                 head_length=3, head_width=2, edgecolor='k', edgewidth=1, ax=None,
                 label=None, labelpos=0.5, label_facecolor='white', label_edgecolor='white',
                 label_color='k', alpha=0):
        self.angle = angle
        self.r = r
        self.circ_stretch = circ_stretch
        self.circ_rad = circ_rad
        self.shrink = shrink
        self.arrowstyle = arrowstyle
        self.head_length = head_length
        self.head_width = head_width
        self.edgecolor = edgecolor
        self.edgewidth = edgewidth
        self.ax = ax
        self.label = label
        self.labelpos = labelpos
        self.label_facecolor = label_facecolor
        self.label_edgecolor = label_edgecolor
        self.label_color = label_color
        self.alpha = alpha

    def draw(self, ax=None):
        self.ax = ax or self.ax or plt.gca()

        x1, y1 = np.cos(self.angle) * self.circ_stretch * self.r, np.sin(self.angle) * self.circ_stretch * self.r
        theta1 = self.angle + np.pi - self.shrink
        theta2 = self.angle - np.pi + self.shrink
        rs = np.linspace(theta2, theta1)
        xs = np.cos(rs) * self.circ_rad * self.r + x1
        ys = np.sin(rs) * self.circ_rad * self.r + y1
        path = Path(np.stack((xs, ys)).T)

        self.arrow = FancyArrowPatch(
            path=path,
            arrowstyle=ArrowStyle(
                self.arrowstyle, head_length=self.head_length, head_width=self.head_width
            ),
            linewidth=self.edgewidth,
            color=self.edgecolor
        )

        self.ax.add_patch(self.arrow)

        if self.label is not None:
            self.ax.text(
                x1 * self.circ_stretch, y1 * self.circ_stretch, self.label,
                horizontalalignment='center', verticalalignment='center',
                bbox=dict(facecolor=self.label_facecolor, edgecolor=self.label_edgecolor, alpha=self.alpha),
                color=self.label_color
            )
