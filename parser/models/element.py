import math

class element:
    def __init__(self, id):
        self.id = id
        # Initialize other attributes to 0
        self.matno = 0 # Material number
        self.lnods = [] # List of nodes
        self.rindx = 0 # Element quality
        self.densy = 0 # Relative density
        self.fract = 0 # Ductile damage
        
        # Strain rate attributes
        self.srnrt_exx = 0 # Strain rate x(r)
        self.srnrt_eyy = 0 # Strain rate y(z)
        self.srnrt_ezz = 0 # Strain rate z(theta)
        self.srnrt_exy = 0 # Strain rate xy(rz)
        self.srnrt_e = 0 # Effective strain rate
        self.srnrt_ev = 0 # Volumetric strain rate
        
        # Strain attributes
        self.strain_exx = 0 # Strain x(r)
        self.strain_eyy = 0 # Strain y(z)
        self.strain_ezz = 0 # Strain z(theta)
        self.strain_exy = 0 # Strain xy(rz)
        self.strain_e = 0 # Effective strain
        self.strain_e1 = 0 # Strain 1
        self.strain_e3 = 0 # Strain 3
        self.angle13 = 0 # Angle rad
        
        # Stress attributes
        self.stress_oxx = 0 # Stress x(r)
        self.stress_oyy = 0 # Stress y(z)
        self.stress_ozz = 0 # Stress z(theta)
        self.stress_oxy = 0 # Stress xy(rz)
        self.stress_o = 0 # Effective stress
        self.stress_orr = 0 # Average stress

    # ============== SETTERS ==============
    
    # Basic properties setters
    def set_matno(self, matno):
        self.matno = matno
        
    def set_lnods(self, lnod):
        self.lnods.append(lnod)
        
    def set_rindx(self, rindx):
        self.rindx = rindx
        
    def set_densy(self, densy):
        self.densy = densy
        
    def set_fract(self, fract):
        self.fract = fract

    # Strain rate setters
    def set_strain_rate_Exx(self, exx):
        self.srnrt_exx = exx
        
    def set_strain_rate_Eyy(self, eyy):
        self.srnrt_eyy = eyy
        
    def set_strain_rate_Ezz(self, ezz):
        self.srnrt_ezz = ezz
        
    def set_strain_rate_Exy(self, exy):
        self.srnrt_exy = exy
        
    def set_strain_rate_E(self, e):
        self.srnrt_e = e
        
    def set_strain_rate_Ev(self, ev):
        self.srnrt_ev = ev

    # Strain setters
    def set_strain_Exx(self, exx):
        self.strain_exx = exx
        
    def set_strain_Eyy(self, eyy):
        self.strain_eyy = eyy
        
    def set_strain_Ezz(self, ezz):
        self.strain_ezz = ezz
        
    def set_strain_Exy(self, exy):
        self.strain_exy = exy
        
    def set_strain_E(self, e):
        self.strain_e = e
        
    def set_strain_E1(self, e1):
        self.strain_e1 = e1
        
    def set_strain_E3(self, e3):
        self.strain_e3 = e3
        
    def set_angle_13(self, angle_13):
        self.angle13 = angle_13

    # Stress setters
    def set_stress_Oxx(self, oxx):
        self.stress_oxx = oxx
        
    def set_stress_Oyy(self, oyy):
        self.stress_oyy = oyy
        
    def set_stress_Ozz(self, ozz):
        self.stress_ozz = ozz
        
    def set_stress_Oxy(self, oxy):
        self.stress_oxy = oxy
        
    def set_stress_O(self, o):
        self.stress_o = o
        
    def set_stress_Orr(self, orr):
        self.stress_orr = orr

    # ============== GETTERS ==============
    
    # Basic properties getters
    def get_id(self):
        return self.id
        
    def get_matno(self):
        return self.matno
        
    def get_lnods_by_index(self, index):
        if index < len(self.lnods):
            return self.lnods[index]
        else:
            raise IndexError("Index out of range for lnods")
        
    def get_lnods(self):
        return self.lnods
    
    def get_nb_lnods(self):
        return len(self.lnods)
        
    def get_rindx(self):
        return self.rindx
        
    def get_densy(self):
        return self.densy
        
    def get_fract(self):
        return self.fract

    # Strain rate getters
    def get_strain_rate_Exx(self):
        return self.srnrt_exx
        
    def get_strain_rate_Eyy(self):
        return self.srnrt_eyy
        
    def get_strain_rate_Ezz(self):
        return self.srnrt_ezz
        
    def get_strain_rate_Exy(self):
        return self.srnrt_exy
        
    def get_strain_rate_E(self):
        return self.srnrt_e
        
    def get_strain_rate_Ev(self):
        return self.srnrt_ev

    # Strain getters
    def get_strain_Exx(self):
        return self.strain_exx
        
    def get_strain_Eyy(self):
        return self.strain_eyy
        
    def get_strain_Ezz(self):
        return self.strain_ezz
        
    def get_strain_Exy(self):
        return self.strain_exy
        
    def get_strain_E(self):
        return self.strain_e

    def get_strain_volumetric(self):
        return self.strain_exx + self.strain_eyy + self.strain_ezz
        
    def get_strain_E1(self):
        return self.strain_e1
    
    def get_strain_E2(self):
        return 0 - self.strain_e1 - self.strain_e3
        
    def get_strain_E3(self):
        return self.strain_e3
        
    def get_angle_13(self):
        return self.angle13

    # Stress getters
    def get_stress_Oxx(self):
        return self.stress_oxx
        
    def get_stress_Oyy(self):
        return self.stress_oyy
        
    def get_stress_Ozz(self):
        return self.stress_ozz
        
    def get_stress_Oxy(self):
        return self.stress_oxy
        
    def get_stress_O(self):
        return self.stress_o
        
    def get_stress_Orr(self):
        return self.stress_orr

    def calculate_stress(self):
        
        xgash = (self.stress_oxx + self.stress_oyy) * 0.5
        xgish = (self.stress_oxx - self.stress_oyy) * 0.5
        xgesh = self.stress_oxy
        xgosh = math.sqrt(xgish*xgish + xgesh*xgesh)
        
        sts1 = xgash + xgosh
        sts3 = xgash - xgosh
        sts2 = self.stress_ozz
        
        stresses = [sts1, sts2, sts3]
        stresses.sort(reverse=True)
        return stresses

    def get_stress_1(self):
        """Get the maximum principal stress"""
        stresses = self.calculate_stress()
        return stresses[0] if stresses else 0.0
    
    def get_stress_2(self):
        """Get the middle principal stress"""
        stresses = self.calculate_stress()
        return stresses[1] if len(stresses) > 1 else 0.0
    
    def get_stress_3(self):
        """Get the minimum principal stress"""
        stresses = self.calculate_stress()
        return stresses[2] if len(stresses) > 2 else 0.0

    # ============== CALCULATED GETTERS ==============
    
    def get_stress_yy_on_effective_stress(self):
        """Get stress_yy / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return (self.stress_oyy or 0.0) / self.stress_o
        return 0.0
    
    def get_stress_xy_on_effective_stress(self):
        """Get stress_xy / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return (self.stress_oxy or 0.0) / self.stress_o
        return 0.0
    
    def get_average_stress_on_effective_stress(self):
        """Get average_stress / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return (self.stress_orr or 0.0) / self.stress_o
        return 0.0
    
    def get_pressure(self):
        return 0.0
    
    def get_pressure_on_effective_stress(self):
        """Get pressure / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return self.get_pressure() / self.stress_o
        return 0.0

    def get_thickness_plane_stress(self):
        return 0.0 # Temporary value, because i have only 2D example
    
    def get_surface_enlargement_ratio(self):
        return 0.0
    
    # ============== CALCULATED PROPERTIES NODES ==============

    def get_velocity_x(self):
        if self.lnods:
            return sum(node.get_Vx() for node in self.lnods) / len(self.lnods)
        return 0.0
    
    def get_velocity_y(self):
        if self.lnods:
            return sum(node.get_Vy() for node in self.lnods) / len(self.lnods)
        return 0.0
    
    def get_total_velocity(self):
        return ( self.get_velocity_x()**2 + self.get_velocity_y()**2 ) 
    
    def get_force_x(self):
        if self.lnods:
            return sum(node.get_Fx() for node in self.lnods) / len(self.lnods)
        return 0.0
    
    def get_force_y(self):
        if self.lnods:
            return sum(node.get_Fy() for node in self.lnods) / len(self.lnods)
        return 0.0
    
    def get_total_force(self):
        return ( self.get_force_x()**2 + self.get_force_y()**2 )
    
    def get_temperature(self):
        if self.lnods:
            return sum(node.get_Temp() for node in self.lnods) / len(self.lnods)
        return 0.0
    
    def get_temperature_rate(self):
        if self.lnods:
            return sum(node.get_DTemp() for node in self.lnods) / len(self.lnods)
        return 0.0
    
    # ============== UTILITY METHODS ==============
    def get_info(self):
        return (
            f"\nMaterial number: {self.matno}\n"
            f"Quality: {self.rindx}\n"
            f"Density: {self.densy}\n"
            f"Fract: {self.fract}\n\n"

            f"--- Strain Rates ---\n"
            f"ε̇_xx (strain rate xx): {self.srnrt_exx}\n"
            f"ε̇_yy (strain rate yy): {self.srnrt_eyy}\n"
            f"ε̇_zz (strain rate zz): {self.srnrt_ezz}\n"
            f"ε̇_xy (strain rate xy): {self.srnrt_exy}\n"
            f"ε̇_eq (effective strain rate): {self.srnrt_e}\n"
            f"ε̇_vol (volumetric strain rate): {self.srnrt_ev}\n\n"

            f"--- Strains ---\n"
            f"ε_xx: {self.strain_exx}\n"
            f"ε_yy: {self.strain_eyy}\n"
            f"ε_zz: {self.strain_ezz}\n"
            f"ε_xy: {self.strain_exy}\n"
            f"ε_eq (effective strain): {self.strain_e}\n"
            f"ε₁ (principal strain 1): {self.strain_e1}\n"
            f"ε₃ (principal strain 3): {self.strain_e3}\n"
            f"Angle between ε₁ and ε₃: {self.angle13}°\n\n"

            f"--- Stress ---\n"
            f"σ_xx: {self.stress_oxx}\n"
            f"σ_yy: {self.stress_oyy}\n"
            f"σ_zz: {self.stress_ozz}\n"
            f"σ_xy: {self.stress_oxy}\n"
            f"σ_eq (effective stress): {self.stress_o}\n"
            f"Average stress (σ_res): {self.stress_orr}\n\n"
            
            f"--- Calculated Values ---\n"
            f"Pressure: {self.get_pressure():.6f}\n"
            f"σ_yy/σ_eq: {self.get_stress_yy_on_effective_stress():.6f}\n"
            f"σ_xy/σ_eq: {self.get_stress_xy_on_effective_stress():.6f}\n"
            f"Pressure/σ_eq: {self.get_pressure_on_effective_stress():.6f}\n"
        )
    
class element_3D(element):
    def __init__(self, id):
        super().__init__(id)
    
    def set_lnods(self, lnods):
        self.lnods = lnods 