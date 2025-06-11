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

    # ============== UTILITY METHODS ==============
    
    def __str__(self):
        return f"Element(id={self.id}, matno={self.matno}, \nlnods1={self.lnods1}, \nlnods2={self.lnods2}, \nlnods3={self.lnods3}, \nlnods4={self.lnods4}, \nrindx={self.rindx}, densy={self.densy}, fract={self.fract},\
                \nstrain_rate_exx={self.srnrt_exx}, strain_rate_eyy={self.srnrt_eyy}, strain_rate_ezz={self.srnrt_ezz}, strain_rate_exy={self.srnrt_exy}, strain_rate_e={self.srnrt_e}, strain_rate_ev={self.srnrt_ev},\
                \nstrain_exx={self.strain_exx}, strain_eyy={self.strain_eyy}, strain_ezz={self.strain_ezz}, strain_exy={self.strain_exy}, strain_e={self.strain_e}, strain_e1={self.strain_e1}, strain_e3={self.strain_e3}, angle13={self.angle13},\
                \nstress_oxx={self.stress_oxx}, stress_oyy={self.stress_oyy}, stress_ozz={self.stress_ozz}, stress_oxy={self.stress_oxy}, stress_o={self.stress_o}, stress_orr={self.stress_orr})\n"
        
    def get_info(self):
        return {
            'id': self.id,
            'matno': self.matno,
            'lnods': self.lnods,
            'rindx': self.rindx,
            'densy': self.densy,
            'fract': self.fract,
            'strain_rate_exx': self.srnrt_exx,
            'strain_rate_eyy': self.srnrt_eyy,
            'strain_rate_ezz': self.srnrt_ezz,
            'strain_rate_exy': self.srnrt_exy,
            'strain_rate_e': self.srnrt_e,
            'strain_rate_ev': self.srnrt_ev,
            'strain_exx': self.strain_exx,
            'strain_eyy': self.strain_eyy,
            'strain_ezz': self.strain_ezz,
            'strain_exy': self.strain_exy,
            'strain_e': self.strain_e,
            'strain_e1': self.strain_e1,
            'strain_e3': self.strain_e3,
            'angle13': self.angle13,
            'stress_oxx': self.stress_oxx,
            'stress_oyy': self.stress_oyy,
            'stress_ozz': self.stress_ozz,
            'stress_oxy': self.stress_oxy,
            'stress_o': self.stress_o,
            'stress_orr': self.stress_orr
        }