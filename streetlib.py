import numpy as np
import string
import geometry


# class Node(geometry.Point):
#     def __init__(self, x, y, street_name):
#         super(Node, self).__init__(x, y)
#         self.street_name = street_name
#         self.id = hash(street_name + str(x) + str(y))
#
#     def __hash__(self):
#         return self.id


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
        point_list = []
        temp = self.intersects[0]
        if self.src.x != temp.x or self.src.y != temp.y:
            point_list.append(self.src)

        point_list += self.intersects

        temp = self.intersects[intersect_num - 1]
        if self.dst.x != temp.x or self.dst.y != temp.y:
            point_list.append(self.dst)
        for i in range(len(point_list) - 1):
            # check each fragment of segment, on which fragment the intersect located
            if geometry.isOnLine(intersect, geometry.Line(point_list[i], point_list[i+1])):
                self.intersects.insert(i, intersect)
                return


class Street(object):
    def __init__(self, name, points):
        self.name = string.lower(name)
        if points and len(points) >= 2:
            # nodes - tuple, can't be modified after init
            self.nodes = self.get_nodes(points)
            self.num = len(points)
            self.segments = []
            # self.get_segments(self.nodes)
            self.get_segments(self.nodes)
            self.street_vertex = []
            self.street_edge = []

    # def __eq__(self, other):
    #     return other.name == self.name

    # input arg points is a list of 2-tuple, convert tuple to Point object
    def get_nodes(self, points):
        node_list = []
        for pt in points:
            node_list.append(geometry.Point(pt[0], pt[1]))
        return tuple(node_list)

    def get_segments(self, nodes):
        for i in range(len(nodes) - 1):
            self.segments.append(Segment(nodes[i], nodes[i + 1]))
