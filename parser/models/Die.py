class die:

    def __init__(self, id):
        self.id = id
        self.nb_nodes = 0
        self.nodes = []
        self.main_node = None
        self.m = 0
        self.temp = None

    # ============== SETTERS ==============

    def set_nb_nodes(self, nb_nodes):
        self.nb_nodes = nb_nodes

    def set_main_node(self, main_node):
        self.main_node = main_node

    def add_node(self, node):
        self.nodes.append(node)

    def set_m(self, m):
        self.m = m

    def set_temp(self, temp):
        self.temp = temp

    # ============== GETTERS ==============

    def get_id(self):
        return self.id

    def get_nb_nodes(self):
        return self.nb_nodes

    def get_main_node(self):
        return self.main_node

    def get_nodes(self):
        return self.nodes

    def get_m(self):
        return self.m

    def get_temp(self):
        return self.temp

    def __str__(self):
        return f"Die(ID: {self.id}, Main Node: {self.main_node}, M: {self.m}, \n{'Nodes: ' + ', '.join(str(node) for node in self.nodes)})"


class die_3D(die):
    def __init__(self, id):
        super().__init__(id)
