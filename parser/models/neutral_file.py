""" Neutral file model for representing a mesh structure. """


class NeutralFile:

    def __init__(self, title):
        self.title = title
        self.nodes = {}
        self.elements = {}
        self.dies = []
        self.t_time = None

    def add_node(self, node):
        self.nodes[node.get_id()] = node

    def add_element(self, element):
        self.elements[element.get_id()] = element

    def add_die(self, die):
        self.dies.append(die)

    def set_t_time(self, t_time):
        self.t_time = t_time

    def get_title(self):
        return self.title

    def get_nodes(self):
        return self.nodes.values()

    def get_elements(self):
        return self.elements.values()

    def get_t_time(self):
        return self.t_time

    def get_node_by_id(self, node_id):
        return self.nodes.get(node_id)

    def get_element_by_id(self, element_id):
        return self.elements.get(element_id)

    def get_nb_nodes(self):
        return len(self.nodes)

    def get_nb_elements(self):
        return len(self.elements)

    def get_nb_dies(self):
        return len(self.dies)

    def get_dies(self):
        return self.dies

    def is_complete(self):
        return len(self.nodes) > 0 and len(self.elements) > 0


class NeutralFile3D(NeutralFile):
    def __init__(self, title):
        super().__init__(title)
