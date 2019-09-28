import string
import geometry


class Intersect(geometry.Point):
    def __init__(self, x, y, isEndpoint):
        super(Intersect, self).__init__(x, y)
        self.other_owners = []
        self.isEndpoint = isEndpoint

    def add_owner(self, street_name):
        self.other_owners.append(street_name)

    def remove_owner(self, street_name):
        id = self.other_owners.index(street_name)
        for i in range(len(self.other_owners)):
            if self.other_owners[i] == street_name:
                self.other_owners.pop(i)


class Segment(geometry.Line):
    def __init__(self, src, dst):
        super(Segment, self).__init__(src, dst)
        self.intersects = []

    def add_intersect(self, intersect, other_owner_name):
        # if the intersect already exist, do nothing
        for i in self.intersects:
            # if i == intersect:
            if i.x == intersect.x and i.y == intersect.y:
                i.add_owner(other_owner_name)
                return

        intersect.add_owner(other_owner_name)
        intersect_num = len(self.intersects)
        if intersect_num == 0:
            self.intersects.append(intersect)
            return

        # otherwise insert the intersect in the right position of intersect list
        if self.src.x < self.dst.x:
            for i in range(len(self.intersects)):
                if intersect.x < self.intersects[i].x:
                    self.intersects.insert(i, intersect)
                    return
            self.intersects.append(intersect)
        elif self.src.x > self.dst.x:
            for i in range(len(self.intersects)):
                if intersect.x > self.intersects[i].x:
                    self.intersects.insert(i, intersect)
                    return
            self.intersects.append(intersect)
        else:
            if self.src.y < self.dst.y:
                for i in range(len(self.intersects)):
                    if intersect.y < self.intersects[i].y:
                        self.intersects.insert(i, intersect)
                        return
            if self.src.y > self.dst.y:
                for i in range(len(self.intersects)):
                    if intersect.y > self.intersects[i].y:
                        self.intersects.insert(i, intersect)
                        return

class Street(object):
    def __init__(self, name, points):
        self.name = string.lower(name)
        if points and len(points) >= 2:
            # nodes - tuple, can't be modified after init
            self.points = points
            self.nodes = self.get_nodes(points)
            self.num = len(points)
            self.segments = []
            # self.get_segments(self.nodes)
            self.get_segments(self.nodes)
            self.street_vertex = []
            self.street_edge = []

    # input arg points is a list of 2-tuple, convert tuple to Point object
    def get_nodes(self, points):
        node_list = []
        for pt in points:
            node_list.append(geometry.Point(pt[0], pt[1]))
        return tuple(node_list)

    def get_segments(self, nodes):
        for i in range(len(nodes) - 1):
            self.segments.append(Segment(nodes[i], nodes[i + 1]))
