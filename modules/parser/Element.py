class Element:
    def __init__(self, id):
        self.id = id
        # Initialize other attributes to None
        self.matno = None
        self.lnods = []
        self.rindx = None
        self.densy = None
        self.fract = None
        
        # Strain rate attributes
        self.srnrt_exx = None
        self.srnrt_eyy = None
        self.srnrt_ezz = None
        self.srnrt_exy = None
        self.srnrt_e = None
        self.srnrt_ev = None
        
        # Strain attributes
        self.strain_exx = None
        self.strain_eyy = None
        self.strain_ezz = None
        self.strain_exy = None
        self.strain_e = None
        self.strain_e1 = None
        self.strain_e3 = None
        self.angle13 = None
        
        # Stress attributes
        self.stress_oxx = None
        self.stress_oyy = None
        self.stress_ozz = None
        self.stress_oxy = None
        self.stress_o = None
        self.stress_orr = None

    # ============== SETTERS ==============
    
    # Basic properties setters
    def set_matno(self, matno):
        self.matno = matno
        
    def set_lnods(self, lnods):
        self.lnods.append(lnods)
        
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
        
    def get_strain_E1(self):
        return self.strain_e1
        
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
        """Calculate pressure as negative of average normal stress"""
        oxx = self.stress_oxx or 0.0
        oyy = self.stress_oyy or 0.0
        ozz = self.stress_ozz or 0.0
        return -(oxx + oyy + ozz) / 3.0
    
    def get_pressure_on_effective_stress(self):
        """Get pressure / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return self.get_pressure() / self.stress_o
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