from multiprocessing import Process
import sys

from pygraphviz import AGraph

from .templates import GRAPH_BEGINNING

def run_graph(dot, format, output_path='output.png'):
    graph = AGraph()
    graph = graph.from_string(dot)
    graph.draw(path=output_path, prog='dot', format=format)
    sys.exit(0)
    
def render(objects, output_path=None, format='png') -> str:
    e = '\n'.join(e.to_dot() for e in objects['entities'])
    r = ''
    for idx, rel in enumerate(objects['relationships'], start=1):
        r = r + rel.to_dot(flip=idx % 2 == 0) + '\n'
    # r = '\n'.join(rel.to_dot() for r in objects['relationships'])
    dot = f'{GRAPH_BEGINNING}\n{e}\n{r}\n}}\n'

    if format == 'png':
        p = Process(target=run_graph, args=(dot, format, output_path))
        p.start()
        p.join()
        assert p.exitcode == 0
        return output_path
    else:
        if output_path:
            with open(output_path, 'w') as f:
                f.write(dot)
            return output_path
        else:
            return dot



