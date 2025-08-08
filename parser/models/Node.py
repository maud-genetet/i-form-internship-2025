""" Node class for representing a node in a mesh structure. """


class Node:
    def __init__(self, id):
        self.id = id
        # Initialize other attributes to 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.fx = 0
        self.fy = 0
        self.dtemp = 0
        self.temp = 0
        self.n2met = 0
        self.code = 0
        self.is_contact = False

    # ============== SETTERS ==============

    def set_coordX(self, x):
        self.x = x

    def set_coordY(self, y):
        self.y = y

    def set_Vx(self, vx):
        self.vx = vx

    def set_Vy(self, vy):
        self.vy = vy

    def set_Fx(self, fx):
        self.fx = fx

    def set_Fy(self, fy):
        self.fy = fy

    def set_DTemp(self, dtemp):
        self.dtemp = dtemp

    def set_Temp(self, temp):
        self.temp = temp

    def set_n2met(self, n2met):
        self.n2met = n2met

    def set_code(self, code):
        self.code = code

    def set_is_contact(self, is_contact):
        self.is_contact = is_contact

    # ============== GETTERS ==============

    def get_id(self):
        return self.id

    def get_coordX(self):
        return self.x

    def get_coordY(self):
        return self.y

    def get_Vx(self):
        return self.vx

    def get_Vy(self):
        return self.vy

    def get_Fx(self):
        return self.fx

    def get_Fy(self):
        return self.fy

    def get_DTemp(self):
        return self.dtemp

    def get_Temp(self):
        return self.temp

    def get_n2met(self):
        return self.n2met

    def get_code(self):
        return self.code

    def is_contact_node(self):
        return self.is_contact

    # ============== METHODS ==============
    def __str__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}, fx={self.fx}, fy={self.fy}, dtemp={self.dtemp}, temp={self.temp}, n2met={self.n2met}, code={self.code})"

    def get_info(self):
        return (
            f"=== Node Information (ID: {self.id}) ===\n"
            f"Coordinates: {self.x}, {self.y}\n"
            f"Velocity: {self.vx}, {self.vy}\n"
            f"Force: {self.fx}, {self.fy}\n"
            f"Temperature: {self.temp} (Rate: {self.dtemp})\n"
            f"Code: {self.code}\n"
            f"Is Contact Node: {'Yes' if self.is_contact else 'No'}\n"
        )


class Node3D(Node):
    def __init__(self, id):
        super().__init__(id)
        self.z = 0

    # Z coordinate
    def set_coordZ(self, z):
        self.z = z

    def get_coordZ(self):
        return self.z

    def __str__(self):
        base_str = super().__str__()
        return base_str.replace(")", f", z={self.z})")

    def get_info(self):
        base_info = super().get_info()
        return base_info + f"Z Coordinate: {self.z}\n"
