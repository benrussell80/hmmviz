from .arrows import GraphArrow, SelfGraphArrow
from .graphs import BaseMatrixGraph, TransGraph
from .nodes import GraphNode


# if __name__ == "__main__":
#     sequence = np.random.choice(['cloudy', 'foggy'], size=100)

#     dataframe = pd.crosstab(pd.Series(sequence[:-1], name='Today'),
#                             pd.Series(sequence[1:], name='Tomorrow'), normalize=0)
    
#     fig = plt.figure(figsize=(6, 6))
#     ax = plt.gca()
#     print(dataframe)

#     colors = ['lightblue', 'darkred', 'darkgreen', 'orange', 'yellow', 'navy']
#     colormap = {a: b for a, b in zip(dataframe.columns.tolist(), colors)}
#     TransGraph(dataframe).draw(ax=ax, r=1, edgecolors=colormap, nodecolors=colormap, edgelabels=True)
    
#     plt.show()

    