"""
PyVista Mesh Construction Module
"""

import numpy as np
import pyvista as pv

class MeshBuilder:
    """Responsible for creating PyVista meshes from neutral data"""
    
    def __init__(self):
        # Define distinct colors for different materials
        self.material_colors = [
            [1.0, 1.0, 0.0],    # Yellow
            [0.5, 0.0, 0.5],    # Purple
            [0.0, 0.0, 1.0],    # Blue
            [1.0, 0.0, 0.0],    # Red
            [1.0, 0.5, 0.0],    # Orange
            [0.0, 1.0, 0.0],    # Green
            [0.0, 1.0, 1.0],    # Cyan
            [0.5, 0.5, 0.5],    # Gray
            [1.0, 0.0, 1.0],    # Magenta
            [0.5, 1.0, 0.5],    # Light Green
            [0.5, 0.5, 1.0],    # Light Blue
            [1.0, 0.5, 1.0]    # Light Magenta
        ]
    
    def create_pyvista_mesh(self, neutral_data):
        """Create PyVista mesh from neutral data"""
        if not neutral_data:
            return None
        
        nodes = neutral_data.get_nodes()
        elements = neutral_data.get_elements()
        
        if not nodes or not elements:
            return None
        
        # Build points
        points, node_id_to_index = self._build_points(nodes)
        
        # Build cells
        cells = self._build_cells(elements, node_id_to_index)
        
        if not cells:
            return None
        
        # Create mesh
        cell_types = [5] * (len(cells) // 5)  #  9 for Quad, 5 for triangles ( 5 is better for mixed types )
        mesh = pv.UnstructuredGrid(cells, np.array(cell_types), points)
        
        # Add scalar data 
        self._add_scalar_data(mesh, elements, nodes)
        
        # Add material colors
        self._add_material_colors(mesh, elements)
        
        # Add node constraint codes as point data
        self._add_node_constraint_codes(mesh, nodes, node_id_to_index)
        
        # Store original data for vector calculations
        mesh._original_data = neutral_data
        mesh._node_id_to_index = node_id_to_index
        
        return mesh
    
    def _add_material_colors(self, mesh, elements):
        """Add RGB colors based on material numbers"""
        colors = []
        
        for element in elements:
            mat_num = element.get_matno()
            if mat_num is None or mat_num == 0:
                # Default gray color for unknown/zero material
                colors.append([0.7, 0.7, 0.7])
            else:
                color_index = (mat_num - 1) % len(self.material_colors)
                colors.append(self.material_colors[color_index])
        
        # Convert to numpy array and add to mesh
        mesh.cell_data['Material_Colors'] = np.array(colors)
        
    def _build_points(self, nodes):
        """Build points array and correspondence table"""
        points = []
        node_id_to_index = {}
        
        for i, node in enumerate(nodes):
            x = node.get_coordX() if node.get_coordX() is not None else 0.0
            y = node.get_coordY() if node.get_coordY() is not None else 0.0
            points.append([x, y, 0.0])
            node_id_to_index[node.get_id()] = i
        
        return np.array(points), node_id_to_index
    
    def _build_cells(self, elements, node_id_to_index):
        """Build cells array"""
        cells = []
        
        for element in elements:
            element_nodes = element.get_lnods()
            if len(element_nodes) >= 3:
                node_indices = []
                for node in element_nodes:
                    if node and node.get_id() in node_id_to_index:
                        node_indices.append(node_id_to_index[node.get_id()])
                
                if len(node_indices) >= 3:
                    if len(node_indices) == 3:
                        cells.extend([3] + node_indices)
                    elif len(node_indices) == 4:
                        cells.extend([4] + node_indices)
                    else:
                        cells.extend([len(node_indices)] + node_indices)
        
        return cells
    
    def _add_node_constraint_codes(self, mesh, nodes, node_id_to_index):
        """Add node constraint codes as point data for visualization"""
        # Create array for node codes (same length as mesh points)
        node_codes = np.zeros(len(mesh.points))
        
        # Store constraint information in a class attribute for external access
        constraint_info = {
            'node_ids': [],
            'positions_x': [],
            'positions_y': [],
            'codes': []
        }
        
        # Fill with actual node codes and store constraint information
        for node in nodes:
            if node.get_id() in node_id_to_index:
                index = node_id_to_index[node.get_id()]
                code = node.get_code()
                node_codes[index] = code
                
                # Store node information for ALL nodes with non-zero codes
                if code != 0:  # Store all constrained nodes (positive and negative codes)
                    constraint_info['node_ids'].append(node.get_id())
                    constraint_info['positions_x'].append(node.get_coordX())
                    constraint_info['positions_y'].append(node.get_coordY())
                    constraint_info['codes'].append(code)
        
        # Add node codes to mesh point data
        mesh.point_data['Node_Code'] = node_codes
        
        # Store constraint information as a mesh attribute
        if constraint_info['node_ids']:
            mesh._constraint_info = constraint_info
        
    def _add_scalar_data(self, mesh, elements, nodes):
        """Add all available scalar data to mesh including new variables"""
        element_data = {
            'Element_ID': [],

            'Velocity X(r)': [],
            'Velocity Y(z)': [],
            'Total Velocity': [],

            'Force X(r)': [],
            'Force Y(z)': [],
            'Total Force': [],

            'Temperature': [],
            'Temperature Rate': [],

            'Strain rate x(r)': [],
            'Strain rate y(z)': [],
            'Strain rate z(theta)': [],
            'Strain rate xy(rz)': [],
            'Effective strain rate': [],
            'Volumetric strain rate': [],

            'Strain x(r)': [],
            'Strain y(z)': [],
            'Strain z(theta)': [],
            'Strain xy(rz)': [],
            'Effective strain': [],
            'Volumetric Strain': [],
            'Strain 1': [],
            'Strain 2': [],
            'Strain 3': [],

            'Stress x(r)': [],
            'Stress y(z)': [],
            'Stress z(theta)': [],
            'Stress xy(rz)': [],
            'Effective stress': [],
            'Average stress': [],
            'Stress 1': [],
            'Stress 2': [],
            'Stress 3': [],

            'Thickness (Plane Stress)': [],
            'Relative Density': [],
            'Ductile Damage': [],

            'Electric Potential': [],
            'Electric Current Density': [],
            'Electric Resistivity': [],

            'Stress y(z)/Ef.Stress': [],
            'Stress xy(rz)/Ef.Stress': [],
            'Average Stress/Ef.Stress': [],
            'Pressure': [],
            'Pressure/Ef.Stress': [],
            'Surface Enlargement Ratio': [],

            'Element Quality': [],
        }
        
        for element in elements:

            element_data['Element_ID'].append(element.get_id())

            element_data['Strain rate x(r)'].append(element.get_strain_rate_Exx() or 0.0)
            element_data['Strain rate y(z)'].append(element.get_strain_rate_Eyy() or 0.0)
            element_data['Strain rate z(theta)'].append(element.get_strain_rate_Ezz() or 0.0)
            element_data['Strain rate xy(rz)'].append(element.get_strain_rate_Exy() or 0.0)
            element_data['Effective strain rate'].append(element.get_strain_rate_E() or 0.0)
            element_data['Volumetric strain rate'].append(element.get_strain_rate_Ev() or 0.0)

            element_data['Strain x(r)'].append(element.get_strain_Exx() or 0.0)
            element_data['Strain y(z)'].append(element.get_strain_Eyy() or 0.0)
            element_data['Strain z(theta)'].append(element.get_strain_Ezz() or 0.0)
            element_data['Strain xy(rz)'].append(element.get_strain_Exy() or 0.0)
            element_data['Effective strain'].append(element.get_strain_E() or 0.0)
            element_data['Volumetric Strain'].append(element.get_strain_volumetric() or 0.0)  # Fixed: matches key name
            element_data['Strain 1'].append(element.get_strain_E1() or 0.0)
            element_data['Strain 2'].append(element.get_strain_E2() or 0.0)
            element_data['Strain 3'].append(element.get_strain_E3() or 0.0)

            element_data['Stress x(r)'].append(element.get_stress_Oxx() or 0.0)
            element_data['Stress y(z)'].append(element.get_stress_Oyy() or 0.0)
            element_data['Stress z(theta)'].append(element.get_stress_Ozz() or 0.0)
            element_data['Stress xy(rz)'].append(element.get_stress_Oxy() or 0.0)
            element_data['Effective stress'].append(element.get_stress_O() or 0.0)
            element_data['Average stress'].append(element.get_stress_Orr() or 0.0)
            element_data['Thickness (Plane Stress)'].append(element.get_thickness_plane_stress() or 0.0)

            element_data['Stress 1'].append(element.get_stress_1() or 0.0)
            element_data['Stress 2'].append(element.get_stress_2() or 0.0)
            element_data['Stress 3'].append(element.get_stress_3() or 0.0)
            element_data['Relative Density'].append(element.get_densy() or 0.0)
            element_data['Ductile Damage'].append(element.get_fract() or 0.0)

            element_data['Stress y(z)/Ef.Stress'].append(element.get_stress_yy_on_effective_stress() or 0.0)
            element_data['Stress xy(rz)/Ef.Stress'].append(element.get_stress_xy_on_effective_stress() or 0.0)
            element_data['Average Stress/Ef.Stress'].append(element.get_average_stress_on_effective_stress() or 0.0)
            element_data['Pressure'].append(element.get_pressure() or 0.0)
            element_data['Pressure/Ef.Stress'].append(element.get_pressure_on_effective_stress() or 0.0)
            element_data['Surface Enlargement Ratio'].append(element.get_surface_enlargement_ratio() or 0.0)
            element_data['Element Quality'].append(element.get_rindx() or 0.0)

            nb_nodes = element.get_nb_lnods()        
            vx_sum = vy_sum = fx_sum = fy_sum = temp_sum = dtemp_sum = 0.0           
                
            for i in range(nb_nodes):
                node = element.get_lnods_by_index(i)
                        
                vx_sum += (node.get_Vx() or 0.0)
                vy_sum += (node.get_Vy() or 0.0)
                fx_sum += (node.get_Fx() or 0.0)
                fy_sum += (node.get_Fy() or 0.0)
                temp_sum += (node.get_Temp() or 0.0)
                dtemp_sum += (node.get_DTemp() or 0.0)
                    
            if nb_nodes > 0:
                avg_vx = vx_sum / nb_nodes
                avg_vy = vy_sum / nb_nodes
                avg_fx = fx_sum / nb_nodes
                avg_fy = fy_sum / nb_nodes
                avg_temp = temp_sum / nb_nodes
                avg_dtemp = dtemp_sum / nb_nodes
            else:
                avg_vx = avg_vy = avg_fx = avg_fy = avg_temp = avg_dtemp = 0.0

            element_data['Velocity X(r)'].append(avg_vx)
            element_data['Velocity Y(z)'].append(avg_vy)
            element_data['Total Velocity'].append(np.sqrt(avg_vx**2 + avg_vy**2))
            element_data['Force X(r)'].append(avg_fx)
            element_data['Force Y(z)'].append(avg_fy)
            element_data['Total Force'].append(np.sqrt(avg_fx**2 + avg_fy**2))
            element_data['Temperature'].append(avg_temp)
            element_data['Temperature Rate'].append(avg_dtemp)

        for key, values in element_data.items():
            if len(values) != 0:
                mesh.cell_data[key] = np.array(values)
    
    def create_die_mesh(self, die):
        """Create mesh for a die"""
        die_nodes = die.get_nodes()
        
        if not die_nodes or len(die_nodes) < 3:
            return None
        
        die_points = []
        for node in die_nodes:
            x = node.get_coordX() if node.get_coordX() is not None else 0.0
            y = node.get_coordY() if node.get_coordY() is not None else 0.0
            die_points.append([x, y, 0.0])
        
        if len(die_points) >= 3:
            die_points = np.array(die_points)
            
            if len(die_points) >= 3:
                cells = [len(die_points)] + list(range(len(die_points)))
                return pv.UnstructuredGrid(
                    cells,
                    [pv.CellType.POLYGON],
                    die_points
                )
        
        return None