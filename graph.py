import streetlib
import geometry


class Vertex(geometry.Point):
    def __init__(self, pt, isIntersect, id=-1):
        super(Vertex, self).__init__(pt.x, pt.y)
        self.id = id
        self.isIntersect = isIntersect

    def set_id(self, id):
        self.id = id

    def __repr__(self):
        # return '({0:.2f}, {1:.2f})'.format(self.x, self.y)
        return str(self.id) + ' : ' + super(Vertex, self).__repr__()

    def __str__(self):
        return repr(self)


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
        if len(self.edge)>0:
            edge_list = list(self.edge)
            edge_num = len(edge_list)
            for i in range(edge_num-1):
                print ' <', edge_list[i][0], ',', edge_list[i][1], '>,'
            print ' <', edge_list[edge_num-1][0], ',', edge_list[edge_num-1][1], '>'
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
                    # if not geometry.isOverlap(seg_old, seg_new):
                    # zero or one intersect, if zero intersect, return none
                    # new_graph_street.intersects.append(intersect)
                    pts = geometry.intersect(seg_new, seg_old)
                    for pt in pts:
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
                if item.x == intersect.x and item.y == intersect.y:
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

            street.street_edge = []
            street.street_edge = self.get_edge_from_street_vertex(street.street_vertex)
            self.add_street_edge_to_graph(street.street_edge)
        # visited[street.name] = 1

    # return a list of vertex on a segment
    def get_vertex_from_segment(self, seg):
        seg_vertex = []
        if len(seg.intersects) > 0:
            # endpoint of segment is a vertex
            temp = seg.intersects[0]
            if temp.x != seg.src.x or temp.y != seg.src.y:
                seg_vertex.append(Vertex(seg.src, False))

            # intersects are vertex
            for i in range(0, len(seg.intersects)):
                seg_vertex.append(Vertex(seg.intersects[i], True))

            # endpoint of segment is a vertex
            temp = seg.intersects[len(seg.intersects) - 1]
            if temp.x != seg.dst.x or temp.y != seg.dst.y:
                seg_vertex.append(Vertex(seg.dst, False))

        return seg_vertex

    # if already exists in the graph vertex list, do nothing but updating its id in segment vertex list
    # otherwise, append it to the graph vertex list, and update its id
    def add_to_graph_vertex(self, v):
        for item in self.vertex:
            if item.x == v.x and item.y == v.y:
                # update its own id, since it'll be insert into street vertex with its id afterwards
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
            temp = street_vertex[num - 1]
            if temp.x != v.x or temp.y != v.y:
                street_vertex.append(v)

            # !!! just for endpoint !!!
            # already exist in the vertex list,
            # but the endpoint is not intersect in last segment,
            # while the endpoint is an intersect in next segment
            # important when generating edge
            else:
                if v.isIntersect:
                    temp.isIntersect = True

    # a street does not intersect itself, just add each edge between two adjacent vertex
    def get_edge_from_street_vertex(self, street_vertex):
        street_edge = []
        if len(street_vertex) > 1:
            for i in range(len(street_vertex) - 1):
                # avoid situation when a edge is shared by two street, e.g. <a,b> and <b,a>
                if street_vertex[i].isIntersect or street_vertex[i + 1].isIntersect:
                    min_id = min(street_vertex[i].id, street_vertex[i + 1].id)
                    max_id = max(street_vertex[i].id, street_vertex[i + 1].id)
                    street_edge.append((min_id, max_id))
        return street_edge

    def add_street_edge_to_graph(self, street_edge):
        for e in street_edge:
            self.edge.add(e)
