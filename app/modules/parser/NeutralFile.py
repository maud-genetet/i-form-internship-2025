class NeutralFile:
    
    def __init__(self, title):
        self.title = title
        self.nodes = []
        self.elements = []
        self.dies = []
        self.t_time = None

    def add_node(self, node):
        self.nodes.append(node)

    def add_element(self, element):
        self.elements.append(element)

    def add_die(self, die):
        self.dies.append(die)

    def set_t_time(self, t_time):
        self.t_time = t_time

    def get_title(self):
        return self.title
    
    def get_nodes(self):
        return self.nodes
    
    def get_elements(self):
        return self.elements
    
    def get_t_time(self):
        return self.t_time
    
    def get_node_by_id(self, node_id):
        for node in self.nodes:
            if node.get_id() == node_id:
                return node
        return None
    
    def get_element_by_id(self, element_id):
        for element in self.elements:
            if element.get_id() == element_id:
                return element
        return None
    
    def get_nb_nodes(self):
        return len(self.nodes)
    
    def get_nb_elements(self):
        return len(self.elements)
    
    def get_nb_dies(self):
        return len(self.dies)
    
    def get_dies(self):
        return self.dies
    
    def get_edges(self):
        edges = []
        for element in self.elements:
            nb_lnods = element.get_nb_lnods()
            for i in range(nb_lnods):
                node1 = element.get_lnods_by_index(i)
                node2 = element.get_lnods_by_index((i + 1) % nb_lnods)
                edge = (node1, node2)
                if edge not in edges and (node2, node1) not in edges:
                    edges.append(edge)
        return edges
