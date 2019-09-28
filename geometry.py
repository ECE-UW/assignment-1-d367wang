class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return '({0:.2f}, {1:.2f})'.format(self.x, self.y)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return repr(self.src) + ' --> ' + repr(self.dst)


def isVertical(l):
    x1 = l.src.x
    x2 = l.dst.x
    if x1 == x2:
        return True


def isHorizontal(l):
    y1 = l.src.y
    y2 = l.dst.y
    if y1 == y2:
        return True


# def isIntersect(l1, l2):
#     # l1 l2 neither overlap or parialize
#     if not isOverlap(l1, l2):
#         if isVertical(l1):
#             return not isVertical(l2)
#         else:
#             if isVertical(l2):
#                 return True
#             else:
#                 x1, y1 = l1.src.x, l1.src.y
#                 x2, y2 = l1.dst.x, l1.dst.y
#                 x3, y3 = l2.src.x, l2.src.y
#                 x4, y4 = l2.dst.x, l2.dst.y
#                 k1 = (y2 - y1) / (x2 - x1)
#                 k2 = (y4 - y3) / (x4 - x3)
#                 return k1 != k2
#     return False


# check isIntersect before this
def intersect(l1, l2):
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y

    # l1 or l2 is vertical
    # if isVertical(l1):
    #     xcoor = x1
    #     ycoor = (y4 - y3) * (x1 - x3) / (x4 - x3) + y3
    #     return Point(xcoor, ycoor)
    #
    # if isVertical(l2):
    #     xcoor = x3
    #     ycoor = (y2 - y1) * (x3 - x1) / (x2 - x1) + y1
    #     return Point(xcoor, ycoor)
    #
    # if isHorizontal(l1):
    #     ycoor = y1
    #     xcoor = (x4 - x3) * (y1 - y3) / (y4 - y3) + x3
    #     return Point(xcoor, ycoor)
    # if isHorizontal(l2):
    #     ycoor = y3
    #     xcoor = (x2 - x1) * (y3 - y1) / (y2 - y1) + x1
    #     return Point(xcoor, ycoor)

    # special situation:
    # intersect() is only called when calculating intersect of two segment. all of the coordinate is interger
    # so the method isOnLine() is useful
    if l1.src == l2.src and \
            not isOnLine(l1.dst, l2) and \
            not isOnLine(l2.dst, l1):
        return l1.src
    if l1.src == l2.dst and \
            not isOnLine(l1.dst, l2) and \
            not isOnLine(l2.src, l1):
        return l1.src
    if l1.dst == l2.src and \
            not isOnLine(l1.src, l2) and \
            not isOnLine(l2.dst, l1):
        return l1.dst
    if l1.dst == l2.dst and \
            not isOnLine(l1.src, l2) and \
            not isOnLine(l2.src, l1):
        return l1.dst

    # overlap or parallel
    if (x1 - x2) * (y3 - y4) == (y1 - y2) * (x3 - x4):
        return None

    xnum = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4))
    xden = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    xcoor = xnum / xden

    ynum = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    yden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    ycoor = ynum / yden

    pt = Point(xcoor, ycoor)

    # pt not between two endpoints
    if (xcoor - x1) * (xcoor - x2) > 0 or (ycoor - y1) * (ycoor - y2) > 0 or \
                (xcoor - x3) * (xcoor - x4) > 0 or (ycoor - y3) * (ycoor - y4) > 0:
        return None
    return pt


def isOnLine(pt, l):
    if pt == l.src or pt == l.dst:
        return True
    x1, y1 = l.src.x, l.src.y
    x2, y2 = l.dst.x, l.dst.y
    x, y = pt.x, pt.y

    # vertical line
    if isVertical(l):
        if x == x1 and y < max(y1, y2) and pt.y > min(y1, y2):
            return True
        else:
            return False

    # gradient of line
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    # 1. line y = kx + b
    # flag1 = ((k * x + b) == y)
    # 2. between the endpoint
    # flag2 = ((x - x1) * (x - x2) < 0)
    return ((k * x + b) == y) and ((x - x1) * (x - x2) < 0)
    # return flag1 and flag2


# l1 new line, l2 already exist
# if overlap,
# def isOverlap(l1, l2):
#     if isOnLine(l1.src, l2):
#         if isOnLine(l1.dst, l2):
#             return True
#         elif isOnLine(l2.src, l1) and isOnLine(l2.dst, l1):
#             return True
#         return False
#     else:
#         if isOnLine(l1.dst, l2) and \
#                 (isOnLine(l2.src, l1) or isOnLine(l2.dst, l1)):
#             return True
#         return False


if __name__ == '__main__':
    x1 = int(input('point 1 x: '))
    y1 = int(input('point 1 y: '))

    x2 = int(input('point 2 x: '))
    y2 = int(input('point 2 y: '))

    pt1 = Point(x1, y1)
    pt2 = Point(x2, y2)

    x3 = int(input('point 3 x: '))
    y3 = int(input('point 3 y: '))

    x4 = int(input('point 4 x: '))
    y4 = int(input('point 4 y: '))

    pt3 = Point(x3, y3)
    pt4 = Point(x4, y4)
