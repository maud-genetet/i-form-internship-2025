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
        self.code = 0
        self.is_contact = False

    # Coordinate setters

    def set_coordX(self, x):
        """Set X coordinate"""
        self.x = x

    def set_coordY(self, y):
        """Set Y coordinate"""
        self.y = y

    # Velocity setters

    def set_Vx(self, vx):
        """Set X velocity"""
        self.vx = vx

    def set_Vy(self, vy):
        """Set Y velocity"""
        self.vy = vy

    # Force setters

    def set_Fx(self, fx):
        """Set X force"""
        self.fx = fx

    def set_Fy(self, fy):
        """Set Y force"""
        self.fy = fy

    # Temperature setters

    def set_DTemp(self, dtemp):
        """Set temperature rate"""
        self.dtemp = dtemp

    def set_Temp(self, temp):
        """Set temperature"""
        self.temp = temp

    # Constraint setters

    def set_code(self, code):
        """Set constraint code"""
        self.code = code

    def set_is_contact(self, is_contact):
        """Set contact node flag"""
        self.is_contact = is_contact

    # Getters

    def get_id(self):
        """Get node identifier"""
        return self.id

    def get_coordX(self):
        """Get X coordinate"""
        return self.x

    def get_coordY(self):
        """Get Y coordinate"""
        return self.y

    def get_Vx(self):
        """Get X velocity"""
        return self.vx

    def get_Vy(self):
        """Get Y velocity"""
        return self.vy

    def get_Fx(self):
        """Get X force"""
        return self.fx

    def get_Fy(self):
        """Get Y force"""
        return self.fy

    def get_DTemp(self):
        """Get temperature rate"""
        return self.dtemp

    def get_Temp(self):
        """Get temperature"""
        return self.temp

    def get_code(self):
        """Get constraint code"""
        return self.code

    def is_contact_node(self):
        """Check if node is in contact"""
        return self.is_contact

    # Utility methods

    def __str__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}, fx={self.fx}, fy={self.fy}, dtemp={self.dtemp}, temp={self.temp}, code={self.code})"

    def get_info(self):
        """Get formatted node information"""
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
    """3D node with additional Z coordinate and Z-direction properties"""

    def __init__(self, id):
        super().__init__(id)
        self.z = 0

    # Z coordinate methods

    def set_coordZ(self, z):
        """Set Z coordinate"""
        self.z = z

    def get_coordZ(self):
        """Get Z coordinate"""
        return self.z

    def __str__(self):
        base_str = super().__str__()
        return base_str.replace(")", f", z={self.z})")

    def get_info(self):
        """Get formatted 3D node information"""
        base_info = super().get_info()
        return base_info + f"Z Coordinate: {self.z}\n"
