# hmmviz
A package for visualizing state transition graphs from hidden Markov models or other models.

This package is meant to serve as an out-of-the-box means of plotting small graphs (less than 10 nodes).

## Installation
    pip install hmmviz

## Usage
### Plotting a Transition Matrix from a Markov Process
The `TransGraph` takes a pandas DataFrame with states indices and columns and transition probabilities (from index to column)
as values.

```python
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

# looks best on square figures/axes
fig = plt.figure(figsize=(6, 6))

graph.draw()

plt.show()
```

This will make an all black graph with labels on the nodes but none on the edges.

If we want to make the graph more colorful and informative we can pass some parameters into the graph's draw method.

```python
# same T as before
graph = hv.TransGraph(T)

fig = plt.figure(figsize=(6, 6))

nodelabels = {'sunny':  '☁☀', 'rainy': '😊☂'}
colors = {'sunny': 'orange', 'rainy': 'blue'}

graph.draw(
    nodelabels=nodelabels, nodecolors=colors, edgecolors=colors, edgelabels=True,
    nodefontsize=16,
)

plt.show()
```