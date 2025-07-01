
from Element import Element
from Node import Node
from NeutralFile import NeutralFile
from Die import Die
import time

class ParserNeutralFile:

    @staticmethod
    def fortran_float(value_str):
        """
        Convertit une chaîne au format Fortran (avec 'D') en float Python.
        Par exemple: '0.0000000D+00' -> 0.0
        """
        return float(value_str.replace('D', 'E').replace('d', 'e'))

    @staticmethod
    def parser_file(nom_fichier):
        t1 = time.time()
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as fichier:


                lignes = fichier.readlines()
                if not lignes:
                    print("Le fichier est vide.")
                    return
                
                # Vérification du titre
                neu = NeutralFile(lignes[0].strip())

                nb_nodes = int(lignes[1].strip())
                print(f"Nombre de noeuds : {nb_nodes}")

                # Traitement des noeuds
                for i in range(2, 2 + nb_nodes):
                    ligne = lignes[i].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 7:
                            print(f"Erreur de format pour le noeud à la ligne {i + 1}.")
                            continue

                        node_id = int(parts[0])
                        node = Node(node_id)

                        cx = ParserNeutralFile.fortran_float(parts[1])
                        cy = ParserNeutralFile.fortran_float(parts[2])
                        vx = ParserNeutralFile.fortran_float(parts[3])
                        vy = ParserNeutralFile.fortran_float(parts[4])
                        fx = ParserNeutralFile.fortran_float(parts[5])
                        fy = ParserNeutralFile.fortran_float(parts[6])

                        node.set_coordX(cx)
                        node.set_coordY(cy)
                        node.set_Vx(vx)
                        node.set_Vy(vy)
                        node.set_Fx(fx)
                        node.set_Fy(fy)

                        neu.add_node(node)

                actual_ligne = 2 + nb_nodes

                nb_elements = int(lignes[actual_ligne].strip())
                print(f"Nombre d'éléments : {nb_elements}")

                actual_ligne += 1

                # Traitement des éléments
                for i in range(nb_elements):
                    base_line = actual_ligne + i
                    
                    ligne = lignes[base_line].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) >= 9:
                            element_id = int(parts[0])
                            element = Element(element_id)

                            matno = int(parts[1])
                            lnods1 = int(parts[2])
                            lnods2 = int(parts[3])
                            lnods3 = int(parts[4])
                            lnods4 = int(parts[5])
                            rindx = ParserNeutralFile.fortran_float(parts[6])
                            densy = ParserNeutralFile.fortran_float(parts[7])
                            fract = ParserNeutralFile.fortran_float(parts[8])

                            element.set_matno(matno)
                            element.set_lnods(neu.get_node_by_id(lnods1))
                            element.set_lnods(neu.get_node_by_id(lnods2))
                            element.set_lnods(neu.get_node_by_id(lnods3))
                            element.set_lnods(neu.get_node_by_id(lnods4))
                            element.set_rindx(rindx)
                            element.set_densy(densy)
                            element.set_fract(fract)

                            neu.add_element(element)
                        else:
                            print(f"Erreur de format pour l'élément à la ligne {base_line + 1}.")

                    strain_rate_line = actual_ligne + nb_elements + i
                    ligne = lignes[strain_rate_line].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) >= 6:
                            element_id = int(parts[0])
                            element = neu.get_element_by_id(element_id)

                            if element:
                                strnrt_exx = ParserNeutralFile.fortran_float(parts[1])
                                strnrt_eyy = ParserNeutralFile.fortran_float(parts[2])
                                strnrt_ezz = ParserNeutralFile.fortran_float(parts[3])
                                strnrt_exy = ParserNeutralFile.fortran_float(parts[4])
                                strnrt_e = ParserNeutralFile.fortran_float(parts[5])
                                strnrt_ev = ParserNeutralFile.fortran_float(parts[6])

                                element.set_strain_rate_Exx(strnrt_exx)
                                element.set_strain_rate_Eyy(strnrt_eyy)
                                element.set_strain_rate_Ezz(strnrt_ezz)
                                element.set_strain_rate_Exy(strnrt_exy)
                                element.set_strain_rate_E(strnrt_e)
                                element.set_strain_rate_Ev(strnrt_ev)
                        else:
                            print(f"Erreur de format pour l'élément de taux de déformation à la ligne {strain_rate_line + 1}.")

                    strain_line = actual_ligne + 2 * nb_elements + i
                    ligne = lignes[strain_line].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) >= 8:
                            element_id = int(parts[0])
                            element = neu.get_element_by_id(element_id)

                            if element:
                                strain_exx = ParserNeutralFile.fortran_float(parts[1])
                                strain_eyy = ParserNeutralFile.fortran_float(parts[2])
                                strain_ezz = ParserNeutralFile.fortran_float(parts[3])
                                strain_exy = ParserNeutralFile.fortran_float(parts[4])
                                strain_e = ParserNeutralFile.fortran_float(parts[5])
                                strain_e1 = ParserNeutralFile.fortran_float(parts[6])
                                strain_e3 = ParserNeutralFile.fortran_float(parts[7])
                                angle_13 = ParserNeutralFile.fortran_float(parts[8])

                                element.set_strain_Exx(strain_exx)
                                element.set_strain_Eyy(strain_eyy)
                                element.set_strain_Ezz(strain_ezz)
                                element.set_strain_Exy(strain_exy)
                                element.set_strain_E(strain_e)
                                element.set_strain_E1(strain_e1)
                                element.set_strain_E3(strain_e3)
                                element.set_angle_13(angle_13)
                        else:
                            print(f"Erreur de format pour l'élément de déformation à la ligne {strain_line + 1}.")

                    stress_line = actual_ligne + 3 * nb_elements + i
                    ligne = lignes[stress_line].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) >= 7:
                            element_id = int(parts[0])
                            element = neu.get_element_by_id(element_id)

                            if element:
                                stress_oxx = ParserNeutralFile.fortran_float(parts[1])
                                stress_oyy = ParserNeutralFile.fortran_float(parts[2])
                                stress_ozz = ParserNeutralFile.fortran_float(parts[3])
                                stress_oxy = ParserNeutralFile.fortran_float(parts[4])
                                stress_o = ParserNeutralFile.fortran_float(parts[5])
                                stress_orr = ParserNeutralFile.fortran_float(parts[6])

                                element.set_stress_Oxx(stress_oxx)
                                element.set_stress_Oyy(stress_oyy)
                                element.set_stress_Ozz(stress_ozz)
                                element.set_stress_Oxy(stress_oxy)
                                element.set_stress_O(stress_o)
                                element.set_stress_Orr(stress_orr)
                        else:
                            print(f"Erreur de format pour l'élément de contrainte à la ligne {stress_line + 1}.")

                actual_ligne += 4 * nb_elements

                # Temperature nodes

                for i in range(actual_ligne, actual_ligne + nb_nodes):
                    ligne = lignes[i].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 3:
                            print(f"Erreur de format pour le noeud de température à la ligne {i + 1}.")
                            continue

                        node_id = int(parts[0])
                        node = neu.get_node_by_id(node_id)

                        if node:
                            dtemp = ParserNeutralFile.fortran_float(parts[1])
                            temp = ParserNeutralFile.fortran_float(parts[2])

                            node.set_DTemp(dtemp)
                            node.set_Temp(temp)
                actual_ligne += nb_nodes

                # Die elements
                nb_dies = int(lignes[actual_ligne].strip())
                actual_ligne += 2
                print(f"Nombre de dies : {nb_dies}")
                
                for die_index in range(actual_ligne, actual_ligne + nb_dies):

                    ligne = lignes[actual_ligne].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 3:
                            print(f"Erreur de format pour le die à la ligne {actual_ligne + 1}.")
                        else:
                            die_id = int(parts[0])
                            nb_nodes_die = int(parts[1])
                            t_die = ParserNeutralFile.fortran_float(parts[2])

                            die = Die(die_id)
                            neu.add_die(die)

                            actual_ligne += 1

                            ligne_die = lignes[actual_ligne].strip()
                            if ligne_die:
                                parts_die = ligne_die.split()
                                if len(parts_die) < 7:
                                    print(f"Erreur de format pour le die à la ligne {actual_ligne + 1}.")
                                
                                cx_die = ParserNeutralFile.fortran_float(parts_die[0])
                                cy_die = ParserNeutralFile.fortran_float(parts_die[1])
                                vx_die = ParserNeutralFile.fortran_float(parts_die[2])
                                vy_die = ParserNeutralFile.fortran_float(parts_die[3])
                                m = ParserNeutralFile.fortran_float(parts_die[4])
                                fx_die = ParserNeutralFile.fortran_float(parts_die[5])
                                fy_die = ParserNeutralFile.fortran_float(parts_die[6])

                                main_node = Node(-1) # ID temporaire
                                main_node.set_coordX(cx_die)
                                main_node.set_coordY(cy_die)
                                main_node.set_Vx(vx_die)
                                main_node.set_Vy(vy_die)
                                main_node.set_Fx(fx_die)
                                main_node.set_Fy(fy_die)
                                die.set_main_node(main_node)
                                die.set_m(m)

                                actual_ligne += 1

                            for j in range(actual_ligne, actual_ligne + nb_nodes_die):
                                ligne_node = lignes[j].strip()
                                if ligne_node:
                                    node_parts = ligne_node.split()
                                    if len(node_parts) < 2:
                                        print(f"Erreur de format pour le noeud du die à la ligne {j + 1}.")
                                        continue

                                    node = Node(-1) # ID temporaire
                                    cx = ParserNeutralFile.fortran_float(node_parts[0])
                                    cy = ParserNeutralFile.fortran_float(node_parts[1])
                                    node.set_coordX(cx)
                                    node.set_coordY(cy)
                                    die.add_node(node)
                            
                            actual_ligne += nb_nodes_die

                # Contact nodes
                nb_contact_elements = int(lignes[actual_ligne].strip())
                actual_ligne += 1

                # put the node n in contact with set_contact 
                for i in range(actual_ligne, actual_ligne + nb_contact_elements):
                    ligne = lignes[i].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 1:
                            print(f"Erreur de format pour l'élément de contact à la ligne {i + 1}.")
                            continue

                        node_id = int(parts[0])
                        node = neu.get_node_by_id(node_id)
                        node.set_is_contact(True)

                actual_ligne += nb_contact_elements

                print(f"Nombre d'éléments de contact : {nb_contact_elements}")     

                nb_code_elements = int(lignes[actual_ligne].strip())
                actual_ligne += 1

                print(f"Nombre de node avec code : {nb_code_elements}") 

                for i in range(actual_ligne, actual_ligne + nb_code_elements):
                    ligne = lignes[i].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 2:
                            print(f"Erreur de format pour le noeud de code à la ligne {i + 1}.")
                            continue

                        node_id = int(parts[0])
                        code = float(parts[1])
                        node = neu.get_node_by_id(node_id)
                        if node:
                            node.set_code(code)
                            #print(f"Noeud {node_id} mis à jour avec le code {code}.")

                actual_ligne += nb_code_elements
                # Temps
                ligne_temps = lignes[actual_ligne].strip()
                if ligne_temps:
                    try:
                        t_time = ParserNeutralFile.fortran_float(ligne_temps)
                        neu.set_t_time(t_time)
                        print(f"Temps : {t_time}")
                    except ValueError:
                        print(f"Erreur de format pour le temps à la ligne {actual_ligne + 1}.")
                else:
                    print(f"Aucune donnée de temps trouvée à la ligne {actual_ligne + 1}.")

                t2 = time.time()
                print(f"Temps de traitement du fichier : {t2 - t1:.2f} secondes")
                return neu


                #print nodes and elements
                """
                print("Noeuds :")
                for node in neu.get_nodes():
                    print(node)
                print("\nÉléments :")
                for element in neu.get_elements():
                    print(element)
                print("\nDies :")
                for die in neu.get_dies():
                    print(die)
                """


        except FileNotFoundError:
            print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

