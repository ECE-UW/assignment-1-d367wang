import streetlib
import geometry


# class GraphNode(object):
#     def __init__(self, original_node):
#         self.original_node = original_node
#         self.isShared = False
#

class Vertex(geometry.Point):
    def __init__(self, pt, isIntersect, id=-1):
        super(Vertex, self).__init__(pt.x, pt.y)
        self.id = id
        self.isIntersect = isIntersect

    def set_id(self, id):
        self.id = id


    def __repr__(self):
        # return '({0:.2f}, {1:.2f})'.format(self.x, self.y)
        return str(self.id) + ':    ' + super(Vertex, self).__repr__()

    def __str__(self):
        return repr(self)


#
# class GraphStreet(object):
#     def __init__(self, original_street):
#         # init vertex with all the nodes on the street, update later
#         self.original_street = original_street
#         self.path = list(original_street.nodes)
#         self.vertex = list(original_street.nodes)
#         self.intersects = []
#
#     def add_intersect_to_path(self, seg, intersect_list):
#         # look for where the first endpoint of segment located in the path
#         for intersect in intersect_list:
#             for i in range(len(path) - 1):
#                 if seg.src == path[i]:
#                     j = i
#                     while True:
#                         if geometry.isOnLine(intersect, geometry.isOnLine(path[j], path[j+1])):
#                             break
#                         j += 1
#                 return
#
#     def delet_intersect_from_path(self):
#         for node in
#
#     def get_complex_street(self, original_street):
#         for node in original_street.nodes:
#             graph_node = GraphNode(node)


# class Edge(street.Segment):
#     def __eq__(self, other):
#         if (self.src == other.src and self.src == other.src) or \
#             (self.src == other.dst and self.dst == other.src):
#             return True
#         else:
#             return False


class Graph(object):
    def __init__(self):
        self.vertex = []
        self.edge = set()
        self.graph_streets = dict()

    def print_graph(self):
        # element of self.vertex is vertex object
        print 'V = {'
        for v in self.vertex:
            print v
        print '}'

        # element of self.edge is 2-tuple
        print 'E = {'
        for e in self.edge:
            print '<',e[0],',',e[1],'>'
        print '}'


    def is_street_exist(self, street_name):
        for key in self.graph_streets:
            if street_name == key:
                return True
        return False

    def add_street(self, street):
        # 1. add its own nodes to the path
        # new_graph_street = GraphStreet(street)

        # 2. calculate intersect and add to the path
        for seg_new in street.segments:
            for key in self.graph_streets:
                for seg_old in self.graph_streets[key].segments:
                    # do not consider times when segments are overlapped
                    if not geometry.isOverlap(seg_old, seg_new):
                        # zero or one intersect, if zero intersect, return none
                        # new_graph_street.intersects.append(intersect)
                        pt = geometry.intersect(seg_new, seg_old)
                        if pt:
                            isEndpoint = (pt == seg_new.src or pt == seg_new.dst)
                            intersect = streetlib.Intersect(pt.x, pt.y, True)
                            seg_new.add_intersect(intersect, key)

                            isEndpoint = (pt == seg_old.src or pt == seg_old.dst)
                            intersect = streetlib.Intersect(pt.x, pt.y, True)
                            seg_old.add_intersect(intersect, street.name)

        # self.graph_streets.append(street)
        self.graph_streets[street.name] = street

    def change_street(self, street):
        self.remove_street(street.name)
        self.add_street(street)

    def remove_street(self, name):
        street = self.graph_streets.pop(name)
        for seg in street.segments:
            for intersect in seg.intersects:
                for owner in intersect.other_owners:
                    self.search_and_delete_intersect(intersect, owner, street.name)

    def search_and_delete_intersect(self, intersect, street_name, remove_street_name):
        street = self.graph_streets[street_name]
        for seg in street.segments:
            for i in range(len(seg.intersects)):
                item = seg.intersects[i]
                if item == intersect:
                    other_owner_count = len(item.other_owners)
                    for j in range(other_owner_count):
                        if item.other_owners[j] == remove_street_name:
                            item.other_owners.pop(j)
                            break
                    # if no other street segment has this intersect, delete it from the intersect list
                    if len(item.other_owners) == 0:
                        # delete when the intersect is not an original endpoint
                        # if not item.isEndpoint:
                        #     seg.intersects.pop(i)
                        seg.intersects.pop(i)
                    return

    def generate_VE(self):
        self.vertex = []
        self.edge = set()
        for key in self.graph_streets:
            street = self.graph_streets[key]
            street.street_vertex = []
            for seg in street.segments:
                seg_vertex = []
                seg_vertex = self.get_vertex_from_segment(seg)
                if len(seg_vertex) > 0:
                    for item in seg_vertex:
                        # first add vertex to graph vertex to identify its final id
                        self.add_to_graph_vertex(item)
                        # then add it to the street vertex to generate every edge
                        self.add_to_street_vertex(item, street.street_vertex)

                # seg_edge = []
                # seg_edge = self.get_edge_from_segment_vertex(seg_vertex)
                # self.get_edge_from_segment_vertex(seg_vertex)
                # self.edge.append(seg_edge)
            street.street_edge = []
            street.street_edge = self.get_edge_from_street_vertex(street.street_vertex)
            self.add_street_edge_to_graph(street.street_edge)
        # visited[street.name] = 1

    # return a list of vertex on a segment
    def get_vertex_from_segment(self, seg):
        seg_vertex = []
        if len(seg.intersects) > 0:
            # segment src is a intersect
            # if seg.src not in seg.intersects and not self.vertex_already_exist(seg.src):
            #     vertex.append(seg.src)
            # for intersect in seg.intersects:
            #     if not self.vertex_already_exist(intersect):
            #         vertex.append(intersect)
            # if seg.dst not in seg.intersects and not self.vertex_already_exist(seg.dst):
            #     vertex.append(seg.dst)
            if seg.intersects[0] != seg.src:
                seg_vertex.append(Vertex(seg.src, False))

            for i in range(0, len(seg.intersects)):
                seg_vertex.append(Vertex(seg.intersects[i], True))

            if seg.intersects[len(seg.intersects) - 1] != seg.dst:
                seg_vertex.append(Vertex(seg.dst, False))

        return seg_vertex

    # if already exists in the graph vertex list, do nothing but updating its id in segment vertex list
    # otherwise, append it to the graph vertex list, and update its id
    def add_to_graph_vertex(self, v):
        for item in self.vertex:
            if item == v:
                v.id = item.id
                return
        v.id = len(self.vertex)
        self.vertex.append(v)

    # a street does not intersect itself, so just check if the vertex is the same to the one right before it
    def add_to_street_vertex(self, v, street_vertex):
        num = len(street_vertex)
        if len(street_vertex) <= 0:
            street_vertex.append(v)
        else:
            if street_vertex[num - 1] != v:
                street_vertex.append(v)

    # def get_edge_from_segment_vertex(self, seg_vertex):
    #     seg_edge = []
    #     for i in range(len(seg_vertex) - 1):
    #         # seg_edge.append((seg_vertex[i].id, seg_vertex[i+1].id))
    #         self.edge.append((seg_vertex[i].id, seg_vertex[i + 1].id))

         # return seg_edge

    # a street does not intersect itself, just add each edge between two adjacent vertex
    def get_edge_from_street_vertex(self, street_vertex):
        street_edge = []
        if len(street_vertex) > 1:
            for i in range(len(street_vertex) - 1):
                if street_vertex[i].isIntersect or street_vertex[i + 1].isIntersect:
                    street_edge.append((street_vertex[i].id, street_vertex[i + 1].id))
        return street_edge

    def add_street_edge_to_graph(self, street_edge):
        for e in street_edge:
            self.edge.add(e)
