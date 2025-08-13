""" Die class for representing a die in a mesh structure."""


class Die:

    def __init__(self, id):
        self.id = id
        self.nb_nodes = 0
        self.nodes = []
        self.main_node = None
        self.m = 0
        self.temp = None

    # Setters

    def set_nb_nodes(self, nb_nodes):
        """Set the number of nodes"""
        self.nb_nodes = nb_nodes

    def set_main_node(self, main_node):
        """Set the main reference node for force calculation"""
        self.main_node = main_node

    def add_node(self, node):
        """Add a node to the die geometry"""
        self.nodes.append(node)

    def set_m(self, m):
        """Set die m parameter"""
        self.m = m

    def set_temp(self, temp):
        """Set die temperature"""
        self.temp = temp

    # Getters

    def get_id(self):
        """Get die id"""
        return self.id

    def get_nb_nodes(self):
        """Get number of nodes"""
        return self.nb_nodes

    def get_main_node(self):
        """Get main reference node"""
        return self.main_node

    def get_nodes(self):
        """Get all nodes"""
        return self.nodes

    def get_m(self):
        """Get die m parameter"""
        return self.m

    def get_temp(self):
        """Get die temperature"""
        return self.temp

    def __str__(self):
        return f"Die(ID: {self.id}, Main Node: {self.main_node}, M: {self.m}, \n{'Nodes: ' + ', '.join(str(node) for node in self.nodes)})"


class Die3D(Die):
    """3D die representation for 3D forming simulations"""

    def __init__(self, id):
        super().__init__(id)
