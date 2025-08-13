""" Neutral file model for representing a mesh structure. """


class NeutralFile:

    def __init__(self, title):
        self.title = title
        self.nodes = {}
        self.elements = {}
        self.dies = []
        self.t_time = None

    def add_node(self, node):
        """Add node to mesh data"""
        self.nodes[node.get_id()] = node

    def add_element(self, element):
        """Add element to mesh data"""
        self.elements[element.get_id()] = element

    def add_die(self, die):
        """Add die to mesh data"""
        self.dies.append(die)

    def set_t_time(self, t_time):
        """Set simulation time"""
        self.t_time = t_time

    def get_title(self):
        """Get mesh title"""
        return self.title

    def get_nodes(self):
        """Get all nodes in mesh"""
        return self.nodes.values()

    def get_elements(self):
        """Get all elements in mesh"""
        return self.elements.values()

    def get_t_time(self):
        """Get simulation time"""
        return self.t_time

    def get_node_by_id(self, node_id):
        """Find node by identifier"""
        return self.nodes.get(node_id)

    def get_element_by_id(self, element_id):
        """Find element by identifier"""
        return self.elements.get(element_id)

    def get_nb_nodes(self):
        """Get total number of nodes"""
        return len(self.nodes)

    def get_nb_elements(self):
        """Get total number of elements"""
        return len(self.elements)

    def get_nb_dies(self):
        """Get total number of dies"""
        return len(self.dies)

    def get_dies(self):
        """Get all dies in mesh"""
        return self.dies

    def is_complete(self):
        """Check if mesh has minimum required data"""
        return len(self.nodes) > 0 and len(self.elements) > 0


class NeutralFile3D(NeutralFile):
    """Container for 3D mesh data"""

    def __init__(self, title):
        super().__init__(title)
