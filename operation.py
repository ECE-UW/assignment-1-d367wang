import streetlib
import graph


class Operation(object):
    def __init__(self, G, opr, street_name=None, points=None):
        self.opr = opr
        self.street_name = street_name
        if street_name and points:
            self.street = streetlib.Street(street_name, points)
        self.graph = G

    def run(self):
        if self.opr == 'a':
            add(self.street, self.graph)
        elif self.opr == 'c':
            change(self.street, self.graph)
        elif self.opr == 'r':
            remove(self.street_name, self.graph)
        else:
            show_graph(self.graph)


def add(street, G):
    if G.is_street_exist(street.name):
        raise Exception("street currently exists.")
    else:
        G.add_street(street)


def change(street, G):
    if not G.is_street_exist(street.name):
        raise Exception("'c' or 'r' specified for a street that does not exist.")
    else:
        G.change_street(street)


def remove(street_name, G):
    if not G.is_street_exist(street_name):
        raise Exception("'c' or 'r' specified for a street that does not exist.")
    G.remove_street(street_name)
    return


def show_graph(G):
    G.generate_VE()
    G.print_graph()
