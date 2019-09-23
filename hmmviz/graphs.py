import pandas as pd 
import matplotlib.pyplot as plt
from itertools import product
from matplotlib.colors import to_rgba
import numpy as np


class BaseMatrixGraph:
    def __init__(self, dataframe: pd.DataFrame, ax=None):
        self.ax = ax
        self.states = dataframe.index.tolist()
        self.dataframe = dataframe
        
    @classmethod
    def from_array(cls, T, labels):
        pass

    @classmethod
    def from_dict(cls, d):
        pass

    @classmethod
    def from_sparse(cls, csr_matrix, labels):
        pass

    @classmethod
    def from_hmm(cls, model, labels):
        pass


class TransGraph(BaseMatrixGraph):
    def draw(self, ax=None, r=1, nodelabels=True, edgelabels=False, edgecolors=None,
             nodecolors=None, edgewidths=True, edgescale=4, nodesizes=2, edges=True, nodes=True, edgelabelpos=0.5,
             edgelabelformat='{2:.2f}', rot=0, selfloops=True):
        
        self.ax = ax or self.ax or plt.gca()
        
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
            node = GraphNode(a, ax=self.ax, r=r, nodecolor=nodecolors.get(n, 'k'),
                             nodelabel=nodelabels.get(n))
            node.draw()

        # draw edges
        for n1, n2 in edges:
            i = nodes.index(n1)
            j = nodes.index(n2)
            a1, a2 = edgeangles[(n1, n2)]
            value = self.dataframe.loc[n1, n2]

            params = {
                'ax': self.ax,
                'edgewidth': edgewidths[(n1, n2)],
                'edgecolor': edgecolors.get((n1, n2), 'k'),
                'label': edgelabels.get((n1, n2)),
                'label_color': edgecolors.get((n1, n2), 'k'),
                'r': r,
                'labelpos': edgelabelpos,
            }

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
                    xytext = np.array([0, i - j])
                else:
                    xytext = None

                arrow = GraphArrow(a1, a2, outer=outer, inner=inner, stretch_inner=0.6, xytext=xytext, **params)
            
            arrow.draw()

        lim = 1.4 ** 2 * r
        plt.xlim([-lim, lim])
        plt.ylim([-lim, lim])
        self.ax.axis('off')
