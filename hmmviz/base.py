from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba
from matplotlib.patches import ArrowStyle, FancyArrowPatch
from matplotlib.path import Path


class GraphArrow:
    def __init__(self, angleA, angleB, r=1, inner=False, outer=False, stretch_inner=0.8, stretch_outer=1.1, shrinkA=20, shrinkB=20,
                 arrowstyle='-|>', head_length=3, head_width=2, connectionstyle="arc3,rad=0.3",
                 outer_connectionstyle="arc3,rad=-0.3", edgewidth=1, edgecolor='k', ax=None, label=None,
                 labelpos=0.5, label_facecolor='white', label_edgecolor='white', label_color='k', xytext=None, fontname='DejaVu Sans',
                 fontsize=10):
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
        self.inner = inner
        self.stretch_inner = stretch_inner
        self.xytext = xytext
        self.fontname = fontname
        self.fontsize = fontsize

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
                bbox=dict(facecolor=self.label_facecolor, edgecolor=self.label_edgecolor, alpha=0),
                color=self.label_color, fontname=self.fontname, fontsize=self.fontsize
            )

class SelfGraphArrow:
    def __init__(self, angle, r=1, circ_stretch=1.4, circ_rad=0.3, shrink=np.pi/4, arrowstyle='-|>',
                 head_length=3, head_width=2, edgecolor='k', edgewidth=1, ax=None,
                 label=None, labelpos=0.5, label_facecolor='white', label_edgecolor='white',
                 label_color='k', fontname='DejaVu Sans', fontsize=10):
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
        self.fontname = fontname
        self.fontsize = fontsize

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
                bbox=dict(facecolor=self.label_facecolor, edgecolor=self.label_edgecolor, alpha=0),
                color=self.label_color, fontname=self.fontname, fontsize=self.fontsize
            )


class GraphNode:
    def __init__(self, angle, r=1, nodecolor='k', nodesize=20, nodelabel=None, ax=None,
                 fontname='DejaVu Sans', fontsize=10):
        self.angle = angle
        self.r = r
        self.nodecolor = nodecolor
        self.nodesize = nodesize
        self.nodelabel = nodelabel
        self.ax = ax
        self.fontname = fontname
        self.fontsize = fontsize

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
                    color=self.nodecolor,
                    fontdict={
                        'fontname': self.fontname,
                        'fontsize': self.fontsize
                    })


class BaseMatrixGraph:
    def __init__(self, dataframe: pd.DataFrame):
        self.states = dataframe.index.tolist()
        self.dataframe = dataframe

    def __str__(self):
        return str(self.dataframe)
        
    @classmethod
    def from_array(cls, T, labels, **kwargs):
        dataframe = pd.DataFrame(T, columns=labels, index=labels)
        return cls(dataframe, **kwargs)

    @classmethod
    def from_dict(cls, d, labels):
        dataframe = pd.DataFrame(columns=labels)
        for i, j in product(labels, repeat=2):
            dataframe.loc[i, j] = d.get((i, j), 0)

        return cls(dataframe)

    # @classmethod
    # def from_sparse(cls, csr_matrix, labels):
    #     pass

    @classmethod
    def from_hmm(cls, model, labels, **kwargs):
        dataframe = pd.DataFrame(model.transmat_, columns=labels, index=labels)
        return cls(dataframe, **kwargs)

    @classmethod
    def from_networkx(cls, graph, edge_param='weight', **kwargs):
        labels = graph.nodes
        dataframe = pd.DataFrame(columns=labels)
        for u, v, d in graph.edges(data=True):
            dataframe.loc[u, v] = d[edge_param]

        dataframe.fillna(0, inplace=True)
        return cls(dataframe, **kwargs)


class TransGraph(BaseMatrixGraph):
    def draw(self, ax=None, r=1, nodelabels=True, edgelabels=False, edgecolors=None,
             nodecolors=None, edgewidths=True, edgescale=4, nodesizes=2, edges=True, nodes=True, edgelabelpos=0.5,
             edgelabelformat='{2:.2f}', rot=0, selfloops=True, fontname='DejaVu Sans', edgefontsize=10,
             nodefontsize=10):
        
        ax = ax or plt.gca()
        
        if nodes is True:
            nodes = self.dataframe.index.tolist() + [col for col in self.dataframe.columns if col not in self.dataframe.index]
        
        if edges is True:
            edges = list(product(nodes, repeat=2))

        angles = np.linspace(0 + rot, 2 * np.pi + rot, num=len(nodes) + 1)[:-1]

        edgeangles = {
            (n1, n2): (
                angles[nodes.index(n1)],
                angles[nodes.index(n2)],
            ) for n1, n2 in edges
        }

        if nodelabels is True:
            nodelabels = {node: node for node in nodes}
        elif nodelabels is False:
            nodelabels = {}

        if edgelabels is True:
            edgelabels = {(n1, n2): edgelabelformat.format(n1, n2, self.dataframe.loc[n1, n2]) for n1, n2 in edges}
        elif bool(edgelabels) is False:
            edgelabels = {}

        if nodecolors is None:
            nodecolors = {node: 'k' for node in nodes}
        elif not isinstance(nodecolors, dict):
            nodecolors = {node: to_rgba(nodecolors) for node in nodes}

        if edgecolors is None:
            edgecolors = {(n1, n2): 'k' for n1, n2 in edges}
        elif not isinstance(edgecolors, dict):
            edgecolors = {(n1, n2): to_rgba(edgecolors) for n1, n2 in edges}
        else:
            edgecolors = {(n1, n2): edgecolors.get((n1, n2), edgecolors.get(n1, 'k')) for n1, n2 in edges}

        if nodesizes is True:
            nodesizes = {node: self.dataframe.loc[node, node] for node in nodes}
        elif not isinstance(nodesizes, dict):
            nodesizes = {node: nodesizes for node in nodes}
        
        if edgewidths is True:
            edgewidths = {(n1, n2): self.dataframe.loc[n1, n2] * edgescale for n1, n2 in edges}
        elif not isinstance(edgewidths, dict):
            edgewidths = {(n1, n2): edgewidths for n1, n2 in edges}

        # draw nodes
        for n, a in zip(nodes, angles):
            node = GraphNode(a, ax=ax, r=r, nodecolor=nodecolors.get(n, 'k'),
                             nodelabel=nodelabels.get(n), fontname=fontname, fontsize=nodefontsize)
            node.draw()

        # draw edges
        for n1, n2 in edges:
            i = nodes.index(n1)
            j = nodes.index(n2)
            a1, a2 = edgeangles[(n1, n2)]
            value = self.dataframe.loc[n1, n2]

            params = {
                'ax': ax,
                'edgewidth': edgewidths[(n1, n2)],
                'edgecolor': edgecolors.get((n1, n2), 'k'),
                'label': edgelabels.get((n1, n2)),
                'label_color': edgecolors.get((n1, n2), 'k'),
                'r': r,
                'labelpos': edgelabelpos,
                'fontname': fontname,
                'fontsize': edgefontsize,
            }

            if params['edgewidth'] == 0:
                continue

            if i == j:
                if not selfloops:
                    continue
                arrow = SelfGraphArrow(a1, **params)
            else:
                if (i - j) % len(nodes) == 1:
                    outer = True
                else:
                    outer = False

                if (j - i) % len(nodes) == 1:
                    inner = True
                else:
                    inner = False
                
                if len(nodes) == 2:
                    xytext = r * np.array([np.cos(rot - np.pi/2 * (-1) ** i),  + np.sin(rot - np.pi/2 * (-1) ** i)])
                else:
                    xytext = None

                arrow = GraphArrow(a1, a2, outer=outer, inner=inner, stretch_inner=0.6, xytext=xytext, **params)
            
            arrow.draw()

        lim = 1.4 ** 2 * r
        ax.set_xlim([-lim, lim])
        ax.set_ylim([-lim, lim])
        ax.axis('off')
