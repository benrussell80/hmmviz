import hmmviz as hv
import pandas as pd
import matplotlib.pyplot as plt

sequence = ['sunny', 'sunny', 'rainy', 'rainy', 'sunny', 'sunny', 'sunny', 'rainy']

T = pd.crosstab(
    pd.Series(sequence[:-1], name='Today'),
    pd.Series(sequence[1:], name='Tomorrow'),
    normalize=0
)
# Tomorrow  rainy  sunny
# Today                 
# rainy       0.5    0.5
# sunny       0.4    0.6

graph = hv.TransGraph(T)

fig = plt.figure(figsize=(6, 6))

nodelabels = {'sunny':  '☁☀', 'rainy': '😊☂'}
colors = {'sunny': 'orange', 'rainy': 'blue'}

graph.draw(
    nodelabels=nodelabels, nodecolors=colors, edgecolors=colors, edgelabels=True,
    nodefontsize=16,
)

plt.show()