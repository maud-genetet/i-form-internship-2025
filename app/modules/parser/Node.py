class Node:
    def __init__(self, id):
        self.id = id
        # Initialize other attributes to None
        self.x = None
        self.y = None
        self.vx = None
        self.vy = None
        self.fx = None
        self.fy = None
        self.dtemp = None
        self.temp = None
        self.n2met = None
        self.code = 0

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

    # ============== METHODS ==============        
    def __str__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}, fx={self.fx}, fy={self.fy}, dtemp={self.dtemp}, temp={self.temp}, n2met={self.n2met}, code={self.code})"
        