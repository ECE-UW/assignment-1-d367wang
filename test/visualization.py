import numpy as np
import pylab as pl
from matplotlib import collections as mc
from matplotlib.patches import Circle
import cmdParser
import sys

s1_prefix = r'a "a" '
s2_prefix = r'a "b" '
s3_prefix = r'a "c" '
s1 = '(2, -1) (2, 2) (5, 5) (5, 6) (3, 8)'
s2 = '(4, 2) (4, 8)'
s3 = '(1, 4) (5, 8)'


def main():
    str1 = s1_prefix + s1
    str2 = s2_prefix + s2
    str3 = s3_prefix + s3

    while True:
        input = raw_input("\nyour command: ")
        if input == '':
            break

        try:
            cmdParser.operation_parse(input)
        except Exception as e:
            sys.stderr.write('Error: '+ e.message + '\n')
        # cmdParser.operation_parse(input)
    # cmdParser.operation_parse(str1)
    # cmdParser.operation_parse(str2)
    # cmdParser.operation_parse(str3)
    # cmdParser.operation_parse('g')
        if input == 'g':
            G = cmdParser.graph
            draw_graph(G)


def draw_graph(G):
    # lines = [[(2, -1), (2, 2), (5, 5), (5, 6), (3, 8)], [(4, 2), (4, 8)], [(1, 4), (5, 8)]]
    # c = np.array([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
    # lc = mc.LineCollection(lines, colors=c, linewidths=2)
    # fig, ax = pl.subplots()
    # ax.add_collection(lc)
    # ax.autoscale()
    # ax.margins(0.1)
    # pl.show()

    # lines = [[(2, -1), (2, 2), (5, 5), (5, 6), (3, 8)], [(4, 2), (4, 8)], [(1, 4), (5, 8)]]
    c = np.array([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])

    lines = []
    for key in G.graph_streets:
        lines.append(list(G.graph_streets[key].points))

    edges = []
    for pair in G.edge:
        src = pair[0]
        dst = pair[1]
        pt1 = (G.vertex[src].x, G.vertex[src].y)
        pt2 = (G.vertex[dst].x, G.vertex[dst].y)
        edges.append([pt1, pt2])

    patches = []
    for v in G.vertex:
        cir = Circle((v.x, v.y), 0.2)
        patches.append(cir)
    # colors = 100 * np.random.rand(len(patches))
    pc = mc.PatchCollection(patches, True)
    # pc.set_array(np.array(colors))

    intersects = []
    for key in G.graph_streets:
        for seg in G.graph_streets[key].segments:
            for item in seg.intersects:
                cir = Circle((item.x, item.y), 0.2, color='red')
                intersects.append(cir)
    pc_intersects = mc.PatchCollection(intersects, match_original=True)
    # pc_intersects.set_color('#FF00FF')


    # lines = [[(2.00, -1.00), (2.00, 2.00), (5.00, 5.00), (5.00, 6.00), (3.00, 8.00)], [(4.00, 2.00), (4.00, 8.00)]]
    lc = mc.LineCollection(lines, colors=c, linewidths=2)
    edge_lc = mc.LineCollection(edges, color=None, linewidths=2)
    fig, (ax1, ax2) = pl.subplots(1,2, sharey=True)
    ax1.add_collection(lc)
    ax2.add_collection(edge_lc)
    ax2.add_collection(pc)
    ax2.add_collection(pc_intersects)
    # ax1.autoscale()
    # ax2.autoscale()
    ax1.margins(0.1)
    ax2.margins(0.1)

    pl.show()

    # fig, ax = pl.subplots(1,2,1)
    # ax.margins(0.1)
    # t = np.arange(0.0, 2.0, 0.1)
    # s = np.sin(t * np.pi)
    # pl.subplot(2, 2, 1)
    # pl.plot(t, s, 'b--')
    # pl.ylabel('y1')
    # pl.subplot(2, 2, 2)
    # pl.plot(2 * t, s, 'r--')
    # pl.subplot(1,2,2)


if __name__ == '__main__':
    main()
