# from graphviz import Graph
from .templates import GRAPH_BEGINNING

def render(objects, output_path=None, format='png') -> str:
    e = '\n'.join(e.to_dot() for e in objects['entities'])
    r = '\n'.join(r.to_dot() for r in objects['relationships'])
    dot = f'{GRAPH_BEGINNING}\n{e}\n{r}\n}}\n'

    # g = Graph(comment='The Round Table', format=format)
    # # g.node('A', 'King Arthur')
    # # g.node('B', 'Sir Bedevere the Wise')
    # # g.node('L', 'Sir Lancelot the Brave')

    # # g.edges(['AB', 'AL'])
    # # g.edge('B', 'L', constraint='false')

    # render_nodes(objects, g)
    # render_edges(objects, g)



    if output_path:
        with open(output_path, 'w') as f:
            f.write(dot)
        return output_path
    else:
        return dot

