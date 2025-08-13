""" Element class for representing a finite element in a mesh structure. """

import math


class Element:
    def __init__(self, id):
        self.id = id
        # Initialize other attributes to 0
        self.matno = 0  # Material number
        self.lnods = []  # List of nodes
        self.rindx = 0  # Element quality
        self.densy = 0  # Relative density
        self.fract = 0  # Ductile damage

        # Strain rate components
        self.srnrt_exx = 0  # Strain rate x(r)
        self.srnrt_eyy = 0  # Strain rate y(z)
        self.srnrt_ezz = 0  # Strain rate z(theta)
        self.srnrt_exy = 0  # Strain rate xy(rz)
        self.srnrt_e = 0  # Effective strain rate
        self.srnrt_ev = 0  # Volumetric strain rate

        # Strain components
        self.strain_exx = 0  # Strain x(r)
        self.strain_eyy = 0  # Strain y(z)
        self.strain_ezz = 0  # Strain z(theta)
        self.strain_exy = 0  # Strain xy(rz)
        self.strain_e = 0  # Effective strain
        self.strain_e1 = 0  # Strain 1
        self.strain_e3 = 0  # Strain 3
        self.angle13 = 0  # Angle rad

        # Stress components
        self.stress_oxx = 0  # Stress x(r)
        self.stress_oyy = 0  # Stress y(z)
        self.stress_ozz = 0  # Stress z(theta)
        self.stress_oxy = 0  # Stress xy(rz)
        self.stress_o = 0  # Effective stress
        self.stress_orr = 0  # Average stress

    # Basic property setters

    def set_matno(self, matno):
        """Set material number"""
        self.matno = matno

    def set_lnods(self, lnod):
        """Add connected node"""
        self.lnods.append(lnod)

    def set_rindx(self, rindx):
        """Set element quality"""
        self.rindx = rindx

    def set_densy(self, densy):
        """Set density"""
        self.densy = densy

    def set_fract(self, fract):
        """Set ductile damage fract"""
        self.fract = fract

    # Strain rate setters

    def set_strain_rate_Exx(self, exx):
        """Set x-direction strain rate"""
        self.srnrt_exx = exx

    def set_strain_rate_Eyy(self, eyy):
        """Set y-direction strain rate"""
        self.srnrt_eyy = eyy

    def set_strain_rate_Ezz(self, ezz):
        """Set z-direction strain rate"""
        self.srnrt_ezz = ezz

    def set_strain_rate_Exy(self, exy):
        """Set shear strain rate"""
        self.srnrt_exy = exy

    def set_strain_rate_E(self, e):
        """Set effective strain rate"""
        self.srnrt_e = e

    def set_strain_rate_Ev(self, ev):
        """Set volumetric strain rate"""
        self.srnrt_ev = ev

    # Strain setters

    def set_strain_Exx(self, exx):
        """Set x-direction strain"""
        self.strain_exx = exx

    def set_strain_Eyy(self, eyy):
        """Set y-direction strain"""
        self.strain_eyy = eyy

    def set_strain_Ezz(self, ezz):
        """Set z-direction strain"""
        self.strain_ezz = ezz

    def set_strain_Exy(self, exy):
        """Set shear strain"""
        self.strain_exy = exy

    def set_strain_E(self, e):
        """Set effective strain"""
        self.strain_e = e

    def set_strain_E1(self, e1):
        """Set firs strain"""
        self.strain_e1 = e1

    def set_strain_E3(self, e3):
        """Set third principal strain"""
        self.strain_e3 = e3

    def set_angle_13(self, angle_13):
        """Se strain angle"""
        self.angle13 = angle_13

    # Stress setters

    def set_stress_Oxx(self, oxx):
        """Set x-direction stress"""
        self.stress_oxx = oxx

    def set_stress_Oyy(self, oyy):
        """Set y-direction stress"""
        self.stress_oyy = oyy

    def set_stress_Ozz(self, ozz):
        """Set z-direction stress"""
        self.stress_ozz = ozz

    def set_stress_Oxy(self, oxy):
        """Set shear stress"""
        self.stress_oxy = oxy

    def set_stress_O(self, o):
        """Set effective stress"""
        self.stress_o = o

    def set_stress_Orr(self, orr):
        """Set average stress"""
        self.stress_orr = orr

    # Basic property getters

    def get_id(self):
        """Get element identifier"""
        return self.id

    def get_matno(self):
        """Get material number"""
        return self.matno

    def get_lnods_by_index(self, index):
        """Get node by index"""
        if index < len(self.lnods):
            return self.lnods[index]
        else:
            raise IndexError("Index out of range for lnods")

    def get_lnods(self):
        """Get all connected nodes"""
        return self.lnods

    def get_nb_lnods(self):
        """Get number of connected nodes"""
        return len(self.lnods)

    def get_rindx(self):
        """Get element quality index"""
        return self.rindx

    def get_densy(self):
        """Get relative density"""
        return self.densy

    def get_fract(self):
        """Get ductile damage fraction"""
        return self.fract

    # Strain rate getters

    def get_strain_rate_Exx(self):
        """Get x-direction strain rate"""
        return self.srnrt_exx

    def get_strain_rate_Eyy(self):
        """Get y-direction strain rate"""
        return self.srnrt_eyy

    def get_strain_rate_Ezz(self):
        """Get z-direction strain rate"""
        return self.srnrt_ezz

    def get_strain_rate_Exy(self):
        """Get shear strain rate"""
        return self.srnrt_exy

    def get_strain_rate_E(self):
        """Get effective strain rate"""
        return self.srnrt_e

    def get_strain_rate_Ev(self):
        """Get volumetric strain rate"""
        return self.srnrt_ev

    # Strain getters

    def get_strain_Exx(self):
        """Get x-direction strain"""
        return self.strain_exx

    def get_strain_Eyy(self):
        """Get y-direction strain"""
        return self.strain_eyy

    def get_strain_Ezz(self):
        """Get z-direction strain"""
        return self.strain_ezz

    def get_strain_Exy(self):
        """Get shear strain"""
        return self.strain_exy

    def get_strain_E(self):
        """Get effective strain"""
        return self.strain_e

    def get_strain_volumetric(self):
        """Calculate volumetric strain from components"""
        return self.strain_exx + self.strain_eyy + self.strain_ezz

    def get_strain_E1(self):
        """Get firs strain"""
        return self.strain_e1

    def get_strain_E2(self):
        """Calculate second principal strain"""
        return 0 - self.strain_e1 - self.strain_e3

    def get_strain_E3(self):
        """Get third principal strain"""
        return self.strain_e3

    def get_angle_13(self):
        """Ge strain angle"""
        return self.angle13

    # Stress getters

    def get_stress_Oxx(self):
        """Get x-direction stress"""
        return self.stress_oxx

    def get_stress_Oyy(self):
        """Get y-direction stress"""
        return self.stress_oyy

    def get_stress_Ozz(self):
        """Get z-direction stress"""
        return self.stress_ozz

    def get_stress_Oxy(self):
        """Get shear stress"""
        return self.stress_oxy

    def get_stress_O(self):
        """Get effective stress"""
        return self.stress_o

    def get_stress_Orr(self):
        """Get average stress"""
        return self.stress_orr

    def calculate_stress(self):
        """Calculate principal stresses from stress 1 2 3"""
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
        """Get maximum principal stress"""
        stresses = self.calculate_stress()
        return stresses[0] if stresses else 0.0

    def get_stress_2(self):
        """Get intermediate principal stress"""
        stresses = self.calculate_stress()
        return stresses[1] if len(stresses) > 1 else 0.0

    def get_stress_3(self):
        """Get minimum principal stress"""
        stresses = self.calculate_stress()
        return stresses[2] if len(stresses) > 2 else 0.0

    # Derived stress calculations

    def get_stress_yy_on_effective_stress(self):
        """Calculate stress_yy / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return (self.stress_oyy or 0.0) / self.stress_o
        return 0.0

    def get_stress_xy_on_effective_stress(self):
        """Calculate stress_xy / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return (self.stress_oxy or 0.0) / self.stress_o
        return 0.0

    def get_average_stress_on_effective_stress(self):
        """Calculate average_stress / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return (self.stress_orr or 0.0) / self.stress_o
        return 0.0

    def get_pressure(self):
        """Calculate hydrostatic pressure"""
        return 0.0

    def get_pressure_on_effective_stress(self):
        """Calculate pressure / effective_stress ratio"""
        if self.stress_o and self.stress_o != 0:
            return self.get_pressure() / self.stress_o
        return 0.0

    def get_thickness_plane_stress(self):
        """Get thickness for plane stress elements"""
        return 0.0  # Placeholder for 2D cases

    def get_surface_enlargement_ratio(self):
        """Calculate surface area change ratio"""
        return 0.0

    # Node-averaged calculations

    def get_velocity_x(self):
        """Calculate average x-velocity from connected nodes"""
        if self.lnods:
            return sum(node.get_Vx() for node in self.lnods) / len(self.lnods)
        return 0.0

    def get_velocity_y(self):
        """Calculate average y-velocity from connected nodes"""
        if self.lnods:
            return sum(node.get_Vy() for node in self.lnods) / len(self.lnods)
        return 0.0

    def get_total_velocity(self):
        """Calculate total velocity magnitude"""
        return (self.get_velocity_x()**2 + self.get_velocity_y()**2)

    def get_force_x(self):
        """Calculate average x-force from connected nodes"""
        if self.lnods:
            return sum(node.get_Fx() for node in self.lnods) / len(self.lnods)
        return 0.0

    def get_force_y(self):
        """Calculate average y-force from connected nodes"""
        if self.lnods:
            return sum(node.get_Fy() for node in self.lnods) / len(self.lnods)
        return 0.0

    def get_total_force(self):
        """Calculate total force magnitude"""
        return (self.get_force_x()**2 + self.get_force_y()**2)

    def get_temperature(self):
        """Calculate average temperature from connected nodes"""
        if self.lnods:
            return sum(node.get_Temp() for node in self.lnods) / len(self.lnods)
        return 0.0

    def get_temperature_rate(self):
        """Calculate average temperature rate from connected nodes"""
        if self.lnods:
            return sum(node.get_DTemp() for node in self.lnods) / len(self.lnods)
        return 0.0

    # Information display

    def get_info(self):
        """Get formatted element information string"""
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


class Element3D(Element):
    """3D hexahedral element for 3D forming simulations"""

    def __init__(self, id):
        super().__init__(id)

    def set_lnods(self, lnods):
        """Set all connected nodes for 3D element"""
        self.lnods = lnods
