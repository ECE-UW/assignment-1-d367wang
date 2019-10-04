import re
import string

import operation
import streetlib
import graph

re_cmd = r'^[acr][\ ]+'
re_street_name = r'"[a-zA-Z\ ]+"'
re_graph = r'^\ *g\ *$'
re_remove = r'^\ *r\ +"[a-zA-Z\ ]+"\ *$'
re_add_change = r'^\ *[ac]\ +"[a-zA-Z\ ]+"\ +(\(\ *\-?[0-9]+\ *,\ *\-?[0-9]+\ *\)\ *)+$'
re_point = r'\(\ *\-?[0-9]+\ *,\ *\-?[0-9]+\ *\)'
re_int = r'\-?[0-9]+'

graph_pattern = re.compile(re_graph)
remove_pattern = re.compile(re_remove)
add_change_pattern = re.compile(re_add_change)

cmd_pattern = re.compile(re_cmd)
street_name_pattern = re.compile(re_street_name)
point_pattern = re.compile(re_point)
int_pattern = re.compile(re_int)

graph = graph.Graph()

def operation_parse(input):
    # 'g' command
    if graph_pattern.match(input):
        opr = operation.Operation(graph, 'g')
    # 'r' command
    elif remove_pattern.match(input):
        street_name = street_name_pattern.findall(input).pop()
        street_name = string.lower(street_name)
        opr = operation.Operation(graph, 'r', street_name)
    # 'ac' command    
    elif add_change_pattern.match(input):
        cmd = input[0]
        street_name = street_name_pattern.findall(input).pop()
        street_name = string.lower(street_name)
        points = []
        get_points(input, points)
        validate(points)
        opr = operation.Operation(graph, cmd, street_name, points)
    # invalid command
    else:
        raise Exception('Incorrect input format')

    opr.run()

# get point from input
def get_points(input, points):
    result = point_pattern.findall(input)
    for s in result:
        xy = int_pattern.findall(s)
        points.append((int(xy[0]), int(xy[1])))

# validate points
# street can't intersect itself
# any adjacent vertex can't be the same
def validate(points):
    if len(points) < 2:
        raise Exception("too few points, at least two different points")
    for i in range(len(points) - 1):
        if points[i] == points[i+1]:
            raise Exception("adjacent points can't be same")

if __name__ == '__main__':
    # input = raw_input("input command:")
    s1 = r'a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)'
    s2 = r'a "King Street S" (4,2) (4,8)'
    s3 = r'a "Davenport Road" (1,4) (5,8)'
    s4 = 'g'
    s5 = r'  r  "Davenport Road" '
    s6 = r'  r "King Street S"  '
    s7 = r'c "Weber Street" (2,1) (2,2)'

    operation_parse(s1)
    operation_parse(s2)
    operation_parse(s3)
    operation_parse(s4)
    operation_parse(s7)
    operation_parse(s4)